#!/usr/bin/python3
"""
uml_file, file_id, repo_id, repo_name, author, commiter, modifications, repo_age, file_age, commits_before, commits_after

"""

import csv
import pymysql
from collections import defaultdict
import time

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
    days = (time.time() - time.mktime(date.timetuple()))/(3600*24)
    return int(days)

def yield_query(select, table, where='', group=''):
    """
    Given a query

    Returns a dictionary with the values in the select
    """
    dictionary = {}

    cursor = connection.cursor()
    sql = "SELECT " + select + " FROM " + table
    if where:
        sql += " WHERE " + where
    if group:
        sql += " GROUP BY " + group
    print(sql)
    cursor.execute(sql)
    while 1:
        result = cursor.fetchone()
        yield result

def query(select, table, where='', group=''):
    """
    Given a query

    Returns a dictionary with the values in the select
    """
    dictionary = {}

    cursor = connection.cursor()
    sql = "SELECT " + select + " FROM " + table
    if where:
        sql += " WHERE " + where
    if group:
        sql += " GROUP BY " + group
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    if not result:
        print("None found!")
        return None
    return result


with open('uml_files.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["#uml_file, file_path, file_url, file_id, repo_id, repo_user, repo_name, author, commiter, modifications, repo_age, file_age, commits_before, commits_after"])

    # GET database info for file
    # SELECT id, repository_id, file_url, file_path FROM uml_files;
    files = yield_query('id, repository_id, file_url, file_path', 'uml_files')

    for values in files:
        if not values:
            break
        print(values)
        uml_file = values['file_path'].split('/')[-1]
        file_path = values['file_path']
        file_id = values['id']
        repo_id = values['repository_id']
        file_url = values['file_url']

        # GET name of repo
        # SELECT id, uri FROM repositories WHERE id=repository_id;
        a = query('uri', 'repositories', 'id=' + str(values['repository_id']))
        print(a)
        repo_user, repo_name = a['uri'].replace("https://github.com/", '').split('/')

        # Get author/commiter who introduced UML file and date
        # SELECT author_id, committer_id FROM scmlog, actions WHERE type="A" AND file_id=132 AND actions.commit_id=scmlog.id;
        b = query('author_id, committer_id, date', 'scmlog, actions', 'type="A" AND actions.commit_id=scmlog.id AND file_id=' + str(values['id']))
        print(b)
        if not b:
            continue
        author = b['author_id']
        committer = b['committer_id']
        file_age = days_since(b['date'])

        # Get number of modifications to UML file
        # SELECT COUNT(*) FROM actions WHERE type="M" AND file_id=;
        c = query('COUNT(*) as number', 'actions', 'type="M" AND file_id=' + str(values['id']))
        print(c)
        modifications = c['number']

        # Get repository first commit date
        # select min(date) from scmlog WHERE repository_id = ;
        d = query('MIN(date) as start', 'scmlog', 'repository_id=' + str(values['repository_id']))
        print(d)
        repo_age = days_since(d['start'])

        # Get # commits before first commit of UML file
        # SELECT count(*) FROM scmlog WHERE repository_id= AND date < '';
        print("hola")
        e = query('COUNT(*) AS previous', 'scmlog', 'repository_id=' + str(values['repository_id']) + ' AND date < "' + str(b['date']) + '"')
        print(e)
        commits_before = e['previous']

        # Get # commits after first commit of UML file
        # SELECT count(*) FROM scmlog WHERE repository_id= AND date > '';
        f = query('COUNT(*) AS posterior', 'scmlog', 'repository_id=' + str(values['repository_id']) + ' AND date > "' + str(b['date']) + '"')
        print(f)
        commits_after = f['posterior']

        writer.writerow([uml_file, file_path, file_url, file_id, repo_id, repo_user, repo_name, author, committer, modifications, repo_age, file_age, commits_before, commits_after])
