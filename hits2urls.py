#!/usr/bin/python
#
# Old:
# application/assets/img/social/designfloat_16.png https://api.github.com/repos/bartsitek/ci.boilerplate/git/blobs/80e356efdcc76431344d38182e1db9ce16b0c1c8
# New:
# https://raw.githubusercontent.com/bartsitek/ci.boilerplate/master/application/assets/img/social/designfloat_16.png

import json
import os.path

start = "https://raw.githubusercontent.com/"

def obtain_branch(username, repo):
    """
    """
    filepath = "cpu03/default/" + username + ":" + repo + ".json"
    if os.path.isfile(filepath):
        with open(filepath) as data_file:
            data = json.load(data_file)
            try:
                return data["default_branch"]
            except KeyError:
                print "ERROR:", filepath
                return 0

    return "master"

with open('hits.txt', 'r') as file:
    linelist = file.readlines()

for line in linelist:
    if "KeyError" in line:
        continue
#    print "*", line[:-1]
    try:
        path, blob = line[:-1].split(" https://api.github.com/")
    except ValueError:
        continue
    blobList = blob.split('/')
    username = blobList[1]
    repo = blobList[2]
    branch = obtain_branch(username, repo)
    if not branch:
        continue
    total = start + username + "/" + repo + "/" + branch + "/" + path
    print total
