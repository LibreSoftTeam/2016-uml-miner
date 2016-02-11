#!/usr/bin/python3
"""
repo_id, main_developer, repo_name, commits, files, committers, authors, age_days, main_lang

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

    Returns following dictionaries with the repo_id as key
         1. main language
         2. number of languages
         3. bytes main language
         4. bytes total (in repo)
    """
    main_dict = {}
    number_dict = defaultdict(int)
    max_dict = defaultdict(int)
    total_dict = defaultdict(int)

    cursor = connection.cursor()
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        if not result:
            return (main_dict, number_dict, max_dict, total_dict)

        number_dict[result['repo_id']] += 1
        total_dict[result['repo_id']] += result['bytes']
        if result['bytes'] > max_dict[result['repo_id']]:
            max_dict[result['repo_id']] = result['bytes']
            main_dict[result['repo_id']] = result['language']

def contribstats(sql):
    """
    Given a query

    Returns following dictionaries with the repo_id as key
    1. main contributor
    2. number of contributors
    3. commits main contributor
    4. commits total (to repo)
    """
    main_dict = {}
    number_dict = defaultdict(int)
    max_dict = defaultdict(int)
    total_dict = defaultdict(int)

    cursor = connection.cursor()
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        if not result:
            return (main_dict, number_dict, max_dict, total_dict)

        number_dict[result['repo_id']] += 1
        total_dict[result['repo_id']] += result['count']
        if result['count'] > max_dict[result['repo_id']]:
            max_dict[result['repo_id']] = result['count']
            main_dict[result['repo_id']] = result['author_id']


def umlstats(sql):
    """
    Given a query

    Returns following dictionaries with the repo_id as key
    1. main contributor to UML files
    2. number of contributors to UML files
    3. commits main contributor to UML files (in the repo)
    4. commits total (to UML files in the repo)
    """
    main_dict = {}
    number_dict = defaultdict(int)
    max_dict = defaultdict(int)
    total_dict = defaultdict(int)

    # I need this temporary dict
    # to store how many contributions per contributor
    # key is (repo_id, author_id)
    tmp_dict = defaultdict(list)

    cursor = connection.cursor()
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        if not result:
            break

        tmp_dict[result['repo_id']].append(result['author_id'])

#        number_dict[result['repo_id']] += 1

    for repo_id in range(1, 950):
        author_list = tmp_dict[repo_id]
        c = Counter(author_list)
        number_dict[repo_id] = len(set(author_list))
        total_dict[repo_id] = sum(c.values())
        try:
            main_dict[repo_id] = c.most_common()[0][0]
            max_dict[repo_id] = c.most_common()[0][1]
        except:
            main_dict[repo_id] = None
            max_dict[repo_id] = None

    return (main_dict, number_dict, max_dict, total_dict)


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
g, h, j, k = langstats('SELECT repo_id, language, bytes FROM repo_langs, languages WHERE repo_langs.lang_id=languages.id ORDER BY repo_id;')

# Get major contributor to the repository
l, m, n, o = contribstats('SELECT repository_id AS repo_id, author_id, count(*) AS count FROM scmlog GROUP BY repo_id, author_id ORDER BY repository_id')

# ,...,  "major_contrib_uml", "number_contribs_uml", "commits_major_contrib_uml", "commits_total_uml",
# We want the modifications (and author_id) for all changes to UML files
p, q, r, s = umlstats('SELECT uml_files.repository_id AS repo_id, file_id, type, author_id FROM actions_file_names, uml_files, scmlog WHERE actions_file_names.file_id=uml_files.id AND scmlog.id=actions_file_names.commit_id ORDER BY uml_files.repository_id')

# Send all to a CSV file

with open('repo_stats2.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["#id", "username", "repository", "committers", "authors", "age_days", "commits", "files", "main_lang", "number_langs", "bytes_main_lang", "bytes_total", "major_contrib", "number_contribs", "commits_major_contrib", "commits_total", "main_uml_author", "number_uml_authors", "changes_by_main_uml_author", "total_uml_changes"])
    for i in range(1, 950):
        username, repo = a[i].replace("https://github.com/", '').split('/')
        days = days_since(d[i])
        try:
            writer.writerow([i, username, repo, b[i], c[i], days, e[i], f[i], g[i], h[i], j[i], k[i], l[i], m[i], n[i], o[i], p[i], q[i], r[i], s[i]])
        except KeyError: # basically when no languages were found
            writer.writerow([i, username, repo, b[i], c[i], days, e[i], f[i],  "None", "None", "None", "None", l[i], m[i], n[i], o[i], p[i], q[i], r[i], s[i]])
