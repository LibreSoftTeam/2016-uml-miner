#!/usr/bin/python3

from collections import namedtuple
import csv
import os
import time
import urllib.request


github_api = "https://api.github.com/repos/"
github_key = "client_id="

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

        print("Retrieve: ", url)
        try:
            urllib.request.urlretrieve(url, directory + "/" + repo[0] + ":" + repo[1] + ".json")
        except IOError:
            print("IOERROR: " + url)
            return 0
        return 1


already = []

with open('updated.csv', 'r') as csvfile:
    for updatedCSV in csv.reader(csvfile):
        repo = updatedCSV[0].strip()
        print(repo)
        if repo not in already and 'https://git.eclipse.org' not in repo:
            already.append(repo)
            get_json(repo.split('/'), "github_langs", "/languages")
            time.sleep(0.72)
