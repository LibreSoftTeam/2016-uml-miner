GitHub UML study scripts

(scripts by Gregorio Robles, available under a GPLv2 or later license)

================================================================================

A. Set of scripts to mine GitHub for potential UML files

1. github-api.py

Given a GHTorrent database, it requests the GitHub API the list of files from its development branch. By default, it asks the master branch, and if that does not exist, it asks for the default branch.

The result is stored as JSON files in the trees subdirectory.

Given its use of the GitHub API, it requires the authentication token. It is also limited to 5,000 hits per hour.

2. github-tree.py

Given JSON files with the tree structure of repositories in the trees subdirectory (as given by the github-api.py script), it prints to STDOUT those files that have an UML extension or a name that may be indicative for an UML file.

The output contains a hit per line. Each line has two fiels separated by a blank space: the relative path of the file in the repository and the absolute path of the file as for the GitHub API.

STDOUT can be redirected to hits.txt to be directly used with hits2urls.py.

3. hits2urls.py

Given a file with all hits as provided by github-tree.py, it prints to STDOUT the complete URL of those files, one per line. This list can be used to retrieve the files that have been identified by the github-tree.py script as potential UML files.

================================================================================

B. Identification of real UML files

This is done as an independent step.

The inputis the result of the hits2urls.py script from the previous phase.

The result of it is stored in the updated.csv CSV file, which contains two columns:
  1. The name of the repository
  2. The URL of the UML file

================================================================================


C. Set of script to mine repos with UML files

1. updated_github_repos.py

Given a CSV file named updated.csv with a list of projects with a positive (i.e., verified) UML files in them, it runs CVSAnalY on the repository to obtain the git metadata from GitHub.

As by now, it should run in a subdirectory where updated.csv is located.

It clones the repositories as subdirectories. By default it does not remove them at the end, so expect an ample amount of storage when running this script. In addition, a database is created (uml_github) with all the git metadata for the repos.


2. umlfiles2table.py

Given a CSV file named updated.csv with a list of projects with a positive (i.e., verified) UML file in them, it creates a new SQL table just with the files that are UML files. The output is printed to STDOUT in MySQL dump format.


3. sql2repo_csv.py

This script extracts data from the database on the changes to UML files and produces a CSV file.

The columns have following labels: "#id", "username", "repository", "committers", "authors", "age_days", "commits", "files", "main_lang", "number_langs", "bytes_main_lang", "bytes_total", "major_contrib", "number_contribs", "commits_major_contrib", "commits_total", "main_uml_author", "number_uml_authors", "changes_by_main_uml_author", "total_uml_changes"


4. updated_github_langs.py

Using updated.csv as input, it queries the GitHub API to obtain the languages of the repositories.

The result is stored as JSON files in the github_langs subdirectory.

Given its use of the GitHub API, it requires the authentication token. It is also limited to 5,000 hits per hour.


5. langs2sql.py

Given a list of JSON files in the github\_langs directory (as obtained from updated_github_langs.py), it prints to STDOUT the resulting SQL for a MySQL database. The database structure of the table is created as well. Database has to be named uml\_github.


6. sql2repo_langs_csv.py

This script extracts data from the database on the changes to UML files and produces a CSV file.

The columns have following labels: "#id", "username", "repository", "committers", "authors", "age_days", "commits", "files", "main_lang"


7. sql2umlfile_csv.py

This script extracts data from the database on the UML files and produces a CSV file.

The columns have following labels: uml_file, file_path, file_url, file_id, repo_id, repo_user, repo_name, author, committer, modifications, repo_age, file_age, commits_before, commits_afte

Each row contains the data for a single UML file

The first columns are:
    a) repository id
    b) UML file id
    c) total days since the first commit to the last commit in the repository

 And then for each modification for the file
    i) Author id of the author who authored this modification
    ii) Days since start of the project
    iii) Commits to the project done before introducing this UML modification
    iv) Commits to the project done after introducting this UML modification

   (these four columns are repeated, for each modification, so the number of columns may vary per row, i.e., per UML file, depending on how often it has been modified).

8. sql2changes_csv.py

This script extracts data from the database on the changes to UML files and produces a CSV file.

Rows may have different lenght as the length depends on the number of modifications.

The author_id before any modification, so:
      a) The 1st column is the repository id
      b) The 2nd column is the UML file id
      c) The 3rd column is the author id who introduced the UML file
      d) The 4th column is when the UML file was introduced (days since the start of the project)
      e) If it exists, the 5th column is the author_id responsible for the 1st modification of the UML file
      f) If it exists, the 6th column is when the UML file was modified for the 1st time (days since start of the project)
      g) If it exists, the 7th column is the author_id responsible for the 2nd modification of the UML file
      h) If it exists, the 8th column is when the UML file was modified for the 2nd time (days since start of the project)
     (and so on... always first author_id of Nth modifcation and date of Nth modification since start of the project)

9. umlfiles_changes_authors.py

This script extracts data from the database with social data (most active contributors) to the UML files and produces a CSV file.

The columns have following labels: id, username, repository, committers, authors, age_days, commits, files, main_lang, number_langs, bytes_main_lang, bytes_total, major_contrib, number_contribs, commits_major_contrib, commits_total, main_uml_committer, number_uml_committers, changes_by_main_uml_committer, total_uml_changes


10. github_users.py

Given a CSV file named updated.csv  it queries the GitHub API for information on the user. The script has a list with already queried users to avoid duplicate queries.

The result is stored as JSON files in the github_users subdirectory.

Given its use of the GitHub API, it requires the authentication token. It is also limited to 5,000 hits per hour.


