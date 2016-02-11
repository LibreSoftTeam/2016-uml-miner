#!/usr/bin/python3
"""
"""

import csv
import pymysql
from collections import defaultdict, Counter

# Connect to the database
connection = pymysql.connect(
host='localhost',
user='operator',
passwd='operator',
db='uml_github',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)

# Let's look for the first and last commit of a repo
startingDict = {}
finishingDict = {}

sql = "SELECT repository_id, MIN(date) AS start, MAX(date) AS finish FROM scmlog GROUP BY repository_id"
cursor = connection.cursor()
print(sql)
cursor.execute(sql)
while 1:
    result = cursor.fetchone()
    if not result:
        break
    startingDict[result["repository_id"]] = result["start"]
    finishingDict[result["repository_id"]] = result["finish"]

#print(startingDict)
#print(len(startingDict))

#

sql = "SELECT uml_files.repository_id AS repo_id, file_id, type, author_id, date, commit_id FROM actions_file_names, uml_files, scmlog WHERE actions_file_names.file_id=uml_files.id AND scmlog.id=actions_file_names.commit_id AND (type='A' or type='M') ORDER BY uml_files.repository_id, file_id, date"

umlfile_dict = defaultdict(list)
umlfile_repo_dict = {}
umlfile_dates_dict = defaultdict(list)

cursor = connection.cursor()
print(sql)
cursor.execute(sql)
while 1:
    result = cursor.fetchone()
    if not result:
        break
#    print(result)
    umlfile_repo_dict[result['file_id']] = result['repo_id']
    age = result['date'] - startingDict[result['repo_id']]
    umlfile_dict[result['file_id']].append(result['author_id'])
    umlfile_dict[result['file_id']].append(age.days)
    umlfile_dict[result['file_id']].append('before') # empty space for commits before
    umlfile_dict[result['file_id']].append('after') # empty space for commits after
    umlfile_dates_dict[result['file_id']].append(result['commit_id'])
#    print(umlfile_dict[result['file_id']])

#

markList = ['<', '>']

for sign in markList:
    for file_id in range(1, 6222034):
        if file_id in umlfile_dict:
            repo_id = umlfile_repo_dict[file_id]
            for commit_id in umlfile_dates_dict[file_id]:
                sql = "SELECT COUNT(*) AS count FROM scmlog WHERE repository_id=" + str(repo_id) + " AND date " + sign + " (SELECT date FROM scmlog WHERE id=" + str(commit_id) + ")"
                cursor = connection.cursor()
                print(sql)
                cursor.execute(sql)
                result = cursor.fetchone()
                print(result['count'])
                if sign == '<':
                    umlfile_dict[file_id][umlfile_dict[file_id].index('before')] = result['count']
                if sign == '>':
                    umlfile_dict[file_id][umlfile_dict[file_id].index('after')] = result['count']


# Send all to a CSV file
with open('umlfiles_changes2.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["#repo_id", "file_id", "total_days", "author_id", "uml_added_days", "commits_before", "commits_after", "author_id2", "uml_changed_days", "commits_before2", "commits_after2", "author_id3", "uml_changed_days", "commits_before3", "commits_after3", "author_id4", "uml_changed_days", "commits_before4", "commits_after4"])
    for file_id in range(1, 6222034):
        if file_id in umlfile_dict:
            total_days = finishingDict[umlfile_repo_dict[file_id]] - startingDict[umlfile_repo_dict[file_id]]
            writer.writerow([umlfile_repo_dict[file_id], file_id, total_days.days] + umlfile_dict[file_id])
