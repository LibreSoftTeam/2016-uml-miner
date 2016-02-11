#!/usr/bin/python3

import json
import os
import pymysql

json_dir = 'github_langs'
jsonfiles = os.listdir(json_dir)

languageDict = {}
languagesInRepos = []

# Connect to the database
connection = pymysql.connect(
                host='localhost',
                user='operator',
                passwd='operator',
                db='uml_github',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

for jsonfile in jsonfiles:
    github_repo = jsonfile.replace('.json', '')
    username, repo = github_repo.split(':')

    # Get repo id from database
    cursor = connection.cursor()
    sql = 'SELECT id from repositories WHERE uri="'
    sql += 'https://github.com/' + username + '/' + repo + '"'
    cursor.execute(sql)
    result = cursor.fetchone()
    try:
        repo_id = result['id']
    except:
        print("# Error", result, username, repo)
        continue

    # Get data from json files and store it into dict and tuple
    with open(json_dir + '/' + jsonfile) as data_file:
        data = json.load(data_file)
#        print(data)
        for language in data:
            if language not in languageDict:
                languageDict[language] = len(languageDict) + 1
            languagesInRepos.append((repo_id, languageDict[language], data[language]))

connection.close()

# Write data into database

create = """
USE uml_github;

CREATE TABLE languages (
   id int,
   language varchar(255)
);

CREATE TABLE repo_langs (
   repo_id int,
   lang_id int,
   bytes int
);
"""

print(create)

#
for language in languageDict:
    print("INSERT INTO languages (id, language) VALUES ({0}, '{1}');".format(languageDict[language], language))

#
for values in languagesInRepos:
    print("INSERT INTO repo_langs (repo_id, lang_id, bytes) VALUES ({}, {}, {});".format(*values))
