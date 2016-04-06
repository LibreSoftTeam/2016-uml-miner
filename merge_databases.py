#!/usr/bin/python3

import csv
import pymysql
import os
from collections import defaultdict, Counter

def fix_string(parameter):

    char1 = "\\"
    char2 = char1 + char1
    tmp_result = parameter.replace("'", "")
    result = tmp_result.replace(char1, char2)
    return result


main_db = 'chunk1_uml_xmi'

# Connect to the database
main_connection = pymysql.connect(
                host='localhost',
                user='operator',
                passwd='operator',
                db=main_db,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

main_cursor = main_connection.cursor()

databases = ['chunk1_images', 'chunk2_uml_xmi', 'chunk2_images', 'chunk3_uml_xmi', 'chunk3_images',
            'chunk4_uml_xmi', 'chunk4_images']

for db in databases:

    dicc_people = {} # dicc[(old_id, chunk)] = new_id
    dicc_repos = {} # dicc[(old_id, chunk)] = new_id
    dicc_files = {} # dicc[(old_id, chunk)] = new_id
    dicc_commits = {} # dicc[(old_id, chunk)] = new_id

    connection = pymysql.connect(
                    host='localhost',
                    user='operator',
                    passwd='operator',
                    db=db,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    """
    PEOPLE
    """

    sql = 'SELECT max(id) AS max FROM people;'
    #        print(sql)
    main_cursor.execute(sql)
    result = main_cursor.fetchone()
    max_id = result['max']

    sql = 'SELECT id, name, email FROM people;'
    cursor.execute(sql)
    result = cursor.fetchall()

    for line in result:
        new_id = line['id'] + int(max_id)
        dicc_people[(line['id'])] = new_id
        sql = "INSERT INTO people (id, name, email) VALUES (" + str(new_id) + ", '"
        sql += fix_string(line['name']) + "', '" + fix_string(line['email']) + "');"
        main_cursor.execute(sql)


    print("people table... done")

    """
    REPOSITORIES
    """

    sql = 'SELECT max(id) AS max FROM repositories;'
    #        print(sql)
    main_cursor.execute(sql)
    result = main_cursor.fetchone()
    max_id = result['max']

    sql = 'SELECT id, uri, name, type FROM repositories;'
    cursor.execute(sql)
    result = cursor.fetchall()

    for line in result:
        new_id = line['id'] + int(max_id)
        dicc_repos[(line['id'])] = new_id
        sql = "INSERT INTO repositories (id, uri, name, type) VALUES ("
        sql += str(new_id) + ", '" + line['uri'] + "', '" + fix_string(line['name'])
        sql += "', '" + line['type'] + "');"
        main_cursor.execute(sql)

    print("repositories table... done")

    """
    FILES
    """

    sql = 'SELECT max(id) AS max FROM files;'
    #        print(sql)
    main_cursor.execute(sql)
    result = main_cursor.fetchone()
    max_id = int(result['max'])

    sql = 'SELECT id, file_name, repository_id FROM files;'
    cursor.execute(sql)
    result = cursor.fetchall()

    for line in result:
        new_id = line['id'] + int(max_id)
        dicc_files[(line['id'])] = new_id
        new_repo_id = dicc_repos[(line['repository_id'])]
        sql = "INSERT INTO files (id, file_name, repository_id) VALUES ("
        sql += str(new_id) + ", '" + fix_string(line['file_name']) + "', " + str(new_repo_id)
        sql += ");"
        try:
            main_cursor.execute(sql)
        except pymysql.err.ProgrammingError:
            print("Error: ", sql)

    print("files table... done")


    """
    SCMLOG
    """

    sql = 'SELECT max(id) AS max FROM scmlog;'
    #        print(sql)
    main_cursor.execute(sql)
    result = main_cursor.fetchone()
    max_id = result['max']

    sql = 'SELECT id, rev, committer_id, author_id, date, date_tz, author_date, '
    sql += 'author_date_tz, message, composed_rev, repository_id FROM scmlog;'
    cursor.execute(sql)
    result = cursor.fetchall()

    for line in result:
        new_id = line['id'] + int(max_id)
        dicc_commits[(line['id'])] = new_id
        new_committer_id = dicc_people[(line['committer_id'])]
        new_author_id = dicc_people[(line['author_id'])]
        new_repo_id = dicc_repos[(line['repository_id'])]

        sql = "INSERT INTO scmlog (id, rev, committer_id, author_id, date, "
        sql += "date_tz, author_date, author_date_tz, message, composed_rev, "
        sql += "repository_id) VALUES ("
        sql += str(new_id) + ", '" + line['rev'] + "', " + str(new_committer_id)
        sql += ", " + str(new_author_id) + ", '" + str(line['date']) + "', '" + str(line['date_tz'])
        sql += "', '" + str(line['author_date']) + "', " + str(line['author_date_tz'])
        sql += ", '" + fix_string(line['message']) + "', " + str(line['composed_rev'])
        sql += ", " + str(new_repo_id) + ");"
        main_cursor.execute(sql)

    print("scmlog table... done")


    """
    FILE LINKS


    sql = 'SELECT max(id) AS max FROM file_links;'
    #        print(sql)
    main_cursor.execute(sql)
    result = main_cursor.fetchone()
    max_id = result['max']

    sql = 'SELECT id, parent_id, ile_name, repository_id FROM files;'
    cursor.execute(sql)
    result = cursor.fetchall()
    """
