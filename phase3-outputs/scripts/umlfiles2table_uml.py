#!/usr/bin/python3

import csv
import pymysql

singleList = []
multipleList = []

# Connect to the database
connection = pymysql.connect(
                host='localhost',
                user='operator',
                passwd='operator',
                db='chunk4_uml_xmi',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor)

with open('updated4_uml_xmi.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if len(myupdatedCSV) > 0:
            updatedCSV = myupdatedCSV[0].split('/')
            repo = updatedCSV[3] + "/" + updatedCSV[4]
            fileurl = myupdatedCSV[0]
            filename = fileurl.split('/')[-1]
            filepath = '/'.join(fileurl.split('/')[6:])
            if 'https://raw.githubusercontent.com/' not in fileurl:
                continue
            # Get repo id from database
            cursor = connection.cursor()
            sql = 'SELECT id FROM repositories WHERE uri="'
            sql += 'https://github.com/{0}"'.format(repo)
    #        print(sql)
            cursor.execute(sql)
            result = cursor.fetchone()
            try:
                repo_id = result['id']
    #            print(repo_id)
            except:
                #print("# Error", result, repo)
                continue

            # Get file id from database
            sql = 'SELECT id FROM files WHERE repository_id={0} and file_name="{1}"'.format(repo_id, filename)
    #        print(sql)
            cursor.execute(sql)
            if cursor.rowcount == 1:
                result = cursor.fetchone()
                file_id = result['id']
                singleList.append((file_id, repo_id, fileurl.replace("'", "\\'"), filepath.replace("'", "\\'")))
            else:
                result = cursor.fetchall()
    #            print("Warning:", result, filepath)
                found = 0
                for file in result:
                    sql = 'SELECT file_path from file_links WHERE file_id={0}'.format(file['id'])
    #                print(sql)
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    db_path = result['file_path']
                    if db_path == filepath:
                        singleList.append((file['id'], repo_id, fileurl.replace("'", "\\'"), filepath.replace("'", "\\'")))
                        found = 1
                        break
                #if not found:
                    #print("# ERROR:", filepath, "not found")


connection.close()

# Write data into database

create = """

USE chunk4_uml_xmi;

CREATE TABLE uml_files (
  id int,
  repository_id int,
  file_url VARCHAR(255),
  file_path VARCHAR(255)
);
"""

print(create)

for entry in singleList:
    print("INSERT INTO uml_files (id, repository_id, file_url, file_path) VALUES ({0}, {1}, '{2}', '{3}');".format(*entry))
