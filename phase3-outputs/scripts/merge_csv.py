#!/usr/bin/python3

import csv
import pymysql
import os
from collections import defaultdict, Counter

dicc_authors = {}
dicc_old_authors =  {}
dicc_repos = {}
dicc_old_repos = {}
dicc_files = {}
dicc_old_files = {}
counter_authors = 0
counter_repos = 0
counter_files = 0

output3_fill = {}

list_files1 = ['repo_stats2_1uml.csv', 'repo_stats2_1images.csv', 'repo_stats2_2uml.csv', 'repo_stats2_2images.csv',
'repo_stats2_3uml.csv', 'repo_stats2_3images.csv', 'repo_stats2_4uml.csv', 'repo_stats2_4images.csv']

list_files2 = ['uml_files_1uml.csv', 'uml_files_1images.csv', 'uml_files_2uml.csv', 'uml_files_2images.csv', 'uml_files_3uml.csv', 'uml_files_3images.csv', 'uml_files_4uml.csv', 'uml_files_4images.csv']

list_files3 = ['umlfiles_changes2_1uml.csv', 'umlfiles_changes2_1images.csv', 'umlfiles_changes2_2uml.csv',
'umlfiles_changes2_2images.csv', 'umlfiles_changes2_3uml.csv', 'umlfiles_changes2_3images.csv', 'umlfiles_changes2_4uml.csv', 'umlfiles_changes2_4images.csv']

# Retrieval & assingment phase

os.chdir('output1')
for csv_file in list_files1:
    with open(csv_file, 'r') as csvfile00:
        for outputCSV in csv.reader(csvfile00):
            if "#id" in outputCSV[0]:
                continue
            repo = outputCSV[2]
            username = outputCSV[1]
            repo_key = repo + ',' + username
            old_id = outputCSV[0]
            chunk = list_files1.index(csv_file)
            counter_repos += 1
            dicc_old_repos[(old_id, chunk)] = counter_repos

os.chdir("..")

os.chdir('output2')
for csv_file in list_files2:
    with open(csv_file, 'r') as csvfile01:
        for outputCSV in csv.reader(csvfile01):
            if "#uml_file" in outputCSV[0]:
                continue
            file_url = outputCSV[2]
            old_file_id = outputCSV[3]
            old_repo_id = outputCSV[4]
            old_author = outputCSV[7]
            chunk = list_files2.index(csv_file)
            if file_url not in dicc_files:
                counter_files += 1
                dicc_files[file_url] = counter_files
                dicc_old_files[(old_file_id, chunk)] = counter_files
            else:
                new_file_id = dicc_repos[file_url]
                dicc_old_files[(old_file_id, chunk)] = new_file_id

            if (old_author, chunk) not in dicc_old_authors:
                counter_authors += 1
                dicc_old_authors[(old_author, chunk)] = counter_authors

os.chdir("..")

os.chdir('output3')
for csv_file in list_files3:
    with open(csv_file, 'r') as csvfile03:
        for outputCSV in csv.reader(csvfile03):
            if "#repo_id" in outputCSV[0]:
                continue

            old_repo_id = outputCSV[0]
            old_file_id = outputCSV[1]
            old_author = outputCSV[3]
            chunk = list_files3.index(csv_file)

            if (old_file_id, chunk) not in dicc_old_files:
                counter_files += 1
                dicc_old_files[(old_file_id, chunk)] = counter_files

            if (old_author, chunk) not in dicc_old_authors:
                counter_authors += 1
                dicc_old_authors[(old_author, chunk)] = counter_authors


os.chdir("..")


# Merge phase

os.chdir('output1')

with open('output1.csv', 'wt') as csvfile_write:
    writer = csv.writer(csvfile_write)
    for csv_file in list_files1:
        with open(csv_file, 'r') as csvfile1:
            for outputCSV in csv.reader(csvfile1):
                if "#id" in outputCSV[0]:
                    continue
                old_id = outputCSV[0]
                repo = outputCSV[2]
                username = outputCSV[1]
                repo_key = repo + ',' + username
                chunk = list_files1.index(csv_file)
                outputCSV[0] = dicc_old_repos[(old_id, chunk)]
                writer.writerow(outputCSV)

os.chdir('..')

os.chdir('output2')
with open('output2.csv', 'wt') as csvfile_write:
    writer = csv.writer(csvfile_write)
    for csv_file in list_files2:
        with open(csv_file, 'r') as csvfile2:
            for outputCSV in csv.reader(csvfile2):
                if "#uml_file" in outputCSV[0]:
                    continue
                file_url = outputCSV[2]
                old_file_id = outputCSV[3]
                old_repo_id = outputCSV[4]
                old_author = outputCSV[7]
                chunk = list_files2.index(csv_file)

                outputCSV[3] = dicc_old_files[(old_file_id, chunk)]
                outputCSV[4] = dicc_old_repos[(old_repo_id, chunk)]
                outputCSV[7] = dicc_old_authors[(old_author, chunk)]
                writer.writerow(outputCSV)

os.chdir('..')

os.chdir('output3')
with open('output3.csv', 'wt') as csvfile_write:
    writer = csv.writer(csvfile_write)
    for csv_file in list_files3:
        with open(csv_file, 'r') as csvfile3:
            for outputCSV in csv.reader(csvfile3):
                if "#repo_id" in outputCSV[0]:
                    continue

                old_repo_id = outputCSV[0]
                old_file_id = outputCSV[1]
                old_author = outputCSV[3]
                chunk = list_files3.index(csv_file)

                outputCSV[0] = dicc_old_repos[(old_repo_id, chunk)]

                try:
                    outputCSV[1] = dicc_old_files[(old_file_id, chunk)]
                except KeyError:
                    print("Key Error: (file_id, chunk)", old_file_id, chunk + 1)
                    outputCSV[1] = old_file_id
                try:
                    outputCSV[3] = dicc_old_authors[(old_author, chunk)]
                except KeyError:
                    print("Key Error: (author_id, chunk)", old_author, chunk + 1)
                    outputCSV[3] = old_author

                writer.writerow(outputCSV)

os.chdir('..')
