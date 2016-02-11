#!/usr/bin/python
import MySQLdb
import urllib
import json
import time
import os

db = MySQLdb.connect("localhost", "operator", "operator", "ghtorrent")
cursor = db.cursor()
query = "SELECT users.login, projects.name FROM projects, users WHERE projects.forked_from IS NULL AND projects.owner_id=users.id;"
cursor.execute(query)
# repo_list is a list of (username, repository_name) tuples
repo_list = cursor.fetchall()
db.close()


github_api = "https://api.github.com/repos/"
github_api = "https://192.30.252.137/repos/"
github_key = "client_id=" # Your GitHub API client id here!

#os.mkdir("master")
#os.mkdir("default")
#os.mkdir("trees")

def lookup(dic, key, *keys):
    """
    Given the dictionary dic, it provides the value with the given key(s)
    From StackOverflow: http://stackoverflow.com/a/11701539

    For instance, to obtain data["commit"]["commit"]["tree",]["sha"]
    you should call:
    lookup(data, ["commit", "commit", "tree", "sha"])
    """
    if keys:
        return lookup(dic.get(key, {}), *keys)
    return dic.get(key)

def get_json(repo, directory, url_append = ""):
    """
    Given the repo tuple (username, repository_name)
    and the directory to store the json
    it performs a query to the repos GitHub v3 API

    url_append offers the possibility to append something to the call
    """
    url = github_api + repo[0] + "/" + repo[1] + url_append
    if "?" in url_append:
        url = url + "&" + github_key
    else:
        url = url + "?" + github_key

    print "Retrieve: ", url
    try:
        urllib.urlretrieve(url, directory + "/" + repo[0] + ":" + repo[1] + ".json")
    except IOError:
        print "IOERROR: " + url
        return 0
    return 1

def read_json(repo, directory, lookup_list):
    """
    Given the repo tuple (username, repository_name)
    the directory where the json has been stored
    it looks up for a given value in the JSON (given as a list)
    and returns its value
    """
    with open(directory + "/" + repo[0] + ":" + repo[1] + ".json") as data_file:
        data = json.load(data_file)

    try:
        return lookup(data, *lookup_list)
    except KeyError:
        return 0

alreadyList = os.listdir("master")

for repo in repo_list:
    if repo[0] + ":" + repo[1]+ ".json" in alreadyList:
        continue
    print
    if not get_json(repo, "master", "/branches/master"):
        continue
    sha_hash = read_json(repo, "master", ["commit", "commit", "tree", "sha"])

    if not sha_hash:
        print "Master branch not found: " + repo[0] + " " + repo[1]
        if not get_json(repo, "default"):
            continue
        default = read_json(repo, "default", ["default_branch"])

        if not default:
            print "No default branch found: " + repo[0] + " " + repo[1]
            time.sleep(1.40)
            continue
        if not get_json(repo, "master", "/branches/" + default):
            continue
        sha_hash = read_json(repo, "master", ["commit", "commit", "tree", "sha"])

        if not sha_hash:
            print "Default branch not found: " + repo[0] + " " + repo[1]
            time.sleep(2.10)
            continue
    if not get_json(repo, "trees", "/git/trees/" + sha_hash + "?recursive=1"):
        continue
    time.sleep(1.40)
