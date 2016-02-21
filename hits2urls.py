#!/usr/bin/python
#
# Old:
# application/assets/img/social/designfloat_16.png https://api.github.com/repos/bartsitek/ci.boilerplate/git/blobs/80e356efdcc76431344d38182e1db9ce16b0c1c8
# New:
# https://raw.githubusercontent.com/bartsitek/ci.boilerplate/master/application/assets/img/social/designfloat_16.png

import json
import os
import os.path
import csv
import sys
from collections import namedtuple

if len(sys.argv) != 2:
    print "Usage: $python hits2urls.py <projects csv>"

start = "https://raw.githubusercontent.com/"
init_path = os.path.abspath(os.curdir)
ProjectRecord = namedtuple('ProjectRecord', 'id, url, owner_id, name, descriptor, language, created_at, forked_from, deleted, updated_at')
owners_dict = {}
projects_dict = {}

def obtain_branch(username, repo):
    """
    """
    filepath = init_path + "/default/" + username + ":" + repo + ".json"
    if os.path.isfile(filepath):
        with open(filepath) as data_file:
            data = json.load(data_file)
            try:
                return data["default_branch"]
            except KeyError:
                print "ERROR:", filepath
                return 0

    return "master"

with open(sys.argv[1], "r") as csvfile: # CSV file name here!
    for contents in csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC):
        contents[0] = int(contents[0])
        contents[2] = int(contents[2])
        row = ProjectRecord(*contents)
        owner_name = row.url.split('/')[4]
        projects_dict[row.name] = row.id
        owners_dict[owner_name] = row.owner_id

with open('hits.txt', 'r') as file:
    linelist = file.readlines()

for line in linelist:
    if "KeyError" in line:
        continue
#    print "*", line[:-1]
    try:
        print line
        path, blob = line[:-1].split(" https://api.github.com/")
    except ValueError:
        continue
    blobList = blob.split('/')
    username = blobList[1]
    repo = blobList[2]
    username_id = str(owners_dict[username])
    repo_id = str(projects_dict[repo])
    branch = obtain_branch(username_id, repo_id)
    if not branch:
        continue
    total = start + username + "/" + repo + "/" + branch + "/" + path
    print total
