#!/usr/bin/python3
"""
repo_id, main_developer, repo_name, commits, files, committers, authors, age_days, main_lang

"""

import csv
import pymysql
from collections import defaultdict

# Connect to the database
connection = pymysql.connect(
host='localhost',
user='operator',
passwd='operator',
db='uml_github',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)

def days_since(date):
    """
    Given a date

    returns the number of days since then
    """
    import time
    days = (time.time() - time.mktime(date.timetuple()))/(3600*24)
    return int(days)

def repostats(select, table, group):
    """
    Given a

    Returns a dictionary with the repo_id as key
    And the number as value
    """
    dictionary = {}
    maxDict = {}

    cursor = connection.cursor()
    sql = "SELECT " + select + " FROM " + table + " GROUP BY " + group
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        if not result:
            return dictionary
        (repo_id, count) = select.split(', ')
        dictionary[result[repo_id]] = result[count]


def langstats(sql):
    """
    Given a query

    Returns a dictionary with the repo_id as key
    And the number as value
    """
    dictionary = {}
    max_dict = defaultdict(int)

    cursor = connection.cursor()
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        if not result:
            return dictionary
        if result['bytes'] > max_dict[result['repo_id']]:
            max_dict[result['repo_id']] = result['bytes']
            dictionary[result['repo_id']] = result['language']

# GET name of repo
a = repostats('id, uri', 'repositories', 'id')

# SELECT committers for each repo
b = repostats('repository_id, count(distinct(committer_id))', 'scmlog', 'repository_id')

# SELECT authors for each repo
c = repostats('repository_id, count(distinct(author_id))', 'scmlog', 'repository_id')

# Start date of the repo
# select repository_id, min(date) from scmlog group by repository_id;
d = repostats('repository_id, min(date)', 'scmlog', 'repository_id')

# Number of commits per repo
# select repository_id, count(*) from scmlog group by repository_id;
e = repostats('repository_id, count(*)', 'scmlog', 'repository_id')

# Number of files per repo
# select repository_id, count(*) from files group by repository_id;
f = repostats('repository_id, count(*)', 'files', 'repository_id')

# Get main repo lang from database
# 1. Programming languages in repo (multiple results per repo possible)
# SELECT repo_id, language, bytes FROM repo_langs, languages WHERE repo_langs.lang_id=languages.id ORDER BY repo_id;
g = langstats('SELECT repo_id, language, bytes FROM repo_langs, languages WHERE repo_langs.lang_id=languages.id ORDER BY repo_id;')

with open('repo_stats.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["#id", "username", "repository", "committers", "authors", "age_days", "commits", "files", "main_lang"])
    for i in range(1, 950):
        username, repo = a[i].replace("https://github.com/", '').split('/')
        days = days_since(d[i])
        try:
            writer.writerow([i, username, repo, b[i], c[i], days, e[i], f[i], g[i]])
        except KeyError: # basically when no languages were found
            writer.writerow([i, username, repo, b[i], c[i], days, e[i], f[i],  "None"])
