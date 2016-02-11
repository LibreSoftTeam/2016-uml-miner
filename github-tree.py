#!/usr/bin/python
import json
import os

repo_jsons = os.listdir("trees")
repo_list = []

for jsonfile in repo_jsons:
    (username, repo) = jsonfile.split(":")
    repo_list.append((username, repo[:-5]))

# Common extensions for UML files
uml_extensions = ["uml", "xmi", "uxf", "xdr"]

# (1) Common filenames for UML files AND (see (2))
keyword_list = ["xmi", "uml", "diagram", "architecture", "design"]
# (2) with following extensions
other_extensions = ["", "xml", "bmp", "jpg", "jpeg", "gif", "png", "svg"]

def interesting(path):
    ext = extension(path)
    if ext in uml_extensions:
        return 1
    if ext in other_extensions:
        for keyword in keyword_list:
            if keyword in filename(path):
                return 1
        return 0
    else:
        return 0

def extension(path):
    """"
    Given a path, return its extension
    """
    tmp_list = path.split('.')
    if len(tmp_list) > 1:
        return tmp_list[-1].lower()
    else:
        return ""

def filename(path):
    """"
    Given a path, return its filename (without extension)
    """
    tmp_list = path.split('/')
    if tmp_list > 1:
        full_name = tmp_list[-1] # with extension
        if '.' in full_name:
            full_name = '.'.join(full_name.split('.')[:-1])
        return full_name.lower()
    else:
        return ""

def tree(path):
    """"
    Given a path, return its tree (without the final filename)
    """
    tmp_list = path.split('/')
    if tmp_list > 1:
        return '/'.join(tmp_list[:-1])
    else:
        return ""

for repo in repo_list:
    with open("trees/" + repo[0] + ":" + repo[1] + ".json") as data_file:    
        data = json.load(data_file)

    try:
        tree = data["tree"]
    except KeyError:
        print "KeyError: ", repo[0], repo[1]
        continue
        
    for file_dict in tree:
        if file_dict["type"] != "tree":
            if interesting(file_dict["path"]):
                print file_dict["path"], file_dict["url"]
            else:
                pass
#                print "Nooooo", file_dict["path"]
