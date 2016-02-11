#!/usr/bin/python3

from collections import namedtuple
import os
import csv
import time
import urllib.request


github_api = "https://api.github.com/users/"
github_key = "client_id="

def get_json(username, directory, url_append = ""):
    """
    Given the repo tuple (username, repository_name)
    and the directory to store the json
    it performs a query to the repos GitHub v3 API

    url_append offers the possibility to append something to the call
    """
    url = github_api + username
    if "?" in url_append:
        url = url + "&" + github_key
    else:
        url = url + "?" + github_key

        print("Retrieve: ", url)
        try:
            urllib.request.urlretrieve(url, directory + "/" + username + ".json")
        except IOError:
            print("IOERROR: " + url)
            return 0
        return 1

already = []

with open('updated.csv', 'r') as csvfile:
    for updatedCSV in csv.reader(csvfile):
        repo = updatedCSV[0].strip()
        repoT = repo.split('/')
        username = repoT[0]
        repository = repoT[1]
        print(username)
        if username not in already and 'https://git.eclipse.org' not in repo:
            already.append(username)
            get_json(username, "github_users", "")
            time.sleep(0.72)
