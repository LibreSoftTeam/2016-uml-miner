#!/usr/bin/python3

from collections import namedtuple
import csv
import os

command = "cvsanaly2 -u operator -p operator -d uml_github"

already = []

current = os.getcwd()
repos_dir = "uml_repos"
line = 0
with open('updated.csv', 'r') as csvfile:
    for updatedCSV in csv.reader(csvfile):
        if updatedCSV[3] == "UML":
            list_url = updatedCSV[2].split('/')
            user = list_url[3]
            repo = list_url[4]
            branch = list_url[5]
            repo_url = ''.join(['https://github.com/', user, '/', repo])
            if (user, repo, branch) not in already:
                if not os.path.exists(user):
                    os.makedirs(user)
                os.chdir(user)
                cloning = ' '.join(['git clone', repo_url, '--branch', branch])
                print(cloning)
                os.system(cloning)
                already.append((user, repo, branch))
                # CVSAnalY in action!
                print("Running CVSAnaly on " + repo)
                try:
                    os.chdir(repo)
                except OSError:
                    print("ERROR: Could not find directory", repo)
                    continue
                os.system(command)
                os.chdir(current)
