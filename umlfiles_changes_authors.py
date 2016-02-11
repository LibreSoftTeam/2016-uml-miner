#!/usr/bin/python3
"""
"""

import csv
from collections import namedtuple, Counter

excludedRepos = [917, 915, 857, 840, 816, 810, 751, 737, 671, 640, 631, 595, 590, 566, 553, 545, 515, 483, 458, 443, 422, 405, 394, 392, 385, 384, 353, 344, 343, 340, 323, 304, 299, 289, 262, 250, 228, 212, 205, 197, 143, 127, 122, 82, 78, 63, 58, 7
]

# Get main stats of repository into a dictionary of namedtuples

RepoRecord = namedtuple('RepoRecord', 'id, username, repository, committers, authors, age_days, commits, files, main_lang, number_langs, bytes_main_lang, bytes_total, major_contrib, number_contribs, commits_major_contrib, commits_total, main_uml_committer, number_uml_committers, changes_by_main_uml_committer, total_uml_changes')

repo_dict = {}

for row in map(RepoRecord._make, csv.reader(open("repo_stats2.csv", "r"))):
    if row.id == '#id':
        continue
    repo_dict[row.id] = row

# 1. How many UML authors in a repo?

counter = Counter()
for repo in repo_dict:
    if int(repo) not in excludedRepos:
        counter[repo_dict[repo].number_uml_committers] += 1

print("Number of UML authors")
print(counter)

# 2. Who introduces UML models? Is it the main author? (for repos with more than n authors)

print("Who introduces UML models? Is it the main author? (for repos with more than n authors) -- same -- other -- difference ")

for n in list(range(1,11)) + [20, 30, 40, 50, 100, 200, 250, 500, 1000]: # n is the number of authors in a repo
    same = 0
    different = 0
    for repo in repo_dict:
        if int(repo) in excludedRepos:
            continue
        if int(repo_dict[repo].authors) < n+1:
            if not repo_dict[repo].main_uml_committer:
                continue
#            print(repo_dict[repo].major_contrib, repo_dict[repo].main_uml_committer)
            if repo_dict[repo].major_contrib == repo_dict[repo].main_uml_committer:
                same +=1
            else:
                different +=1
    print(n, 'contributors or less:', same, different, same-different)
print()

# When does specialization start?

# By share of commits by the main author

counter_main = Counter()
counter_other = Counter()
for repo in repo_dict:
    if int(repo) in excludedRepos:
        continue
    if not repo_dict[repo].main_uml_committer:
        continue
    percent = round(int(repo_dict[repo].commits_major_contrib)*100/int(repo_dict[repo].commits_total))
    if repo_dict[repo].major_contrib != repo_dict[repo].main_uml_committer:
        counter_other[percent] += 1
    else:
        counter_main[percent] += 1

print("When do other authors become the main UMLers in a project?")
print("Percent_main #main_agg #other_agg diff")
aggregate_main = 0
aggregate_other =0
for percent in range(100,-1,-1):
    aggregate_main += counter_main[percent]
    aggregate_other += counter_other[percent]
    if percent%10 == 0:
        print(percent, aggregate_main, aggregate_other, aggregate_main - aggregate_other)


# By number of contributors to the project

counter_main = Counter()
counter_other = Counter()
for repo in repo_dict:
    if int(repo) in excludedRepos:
        continue
    if not repo_dict[repo].main_uml_committer:
        continue
    if repo_dict[repo].major_contrib != repo_dict[repo].main_uml_committer:
        counter_other[repo_dict[repo].number_contribs] += 1
    else:
        counter_main[repo_dict[repo].number_contribs] += 1

print()

print("When do other authors become the main UMLers in a project?")
print("Number_contribs #main_agg #other_agg diff")
aggregate_main = 0
aggregate_other =0
for n in range(1,50): # n is the number of authors in a repo
    aggregate_main += counter_main[str(n)]
    aggregate_other += counter_other[str(n)]
    print(n, aggregate_main, aggregate_other, aggregate_main - aggregate_other)
