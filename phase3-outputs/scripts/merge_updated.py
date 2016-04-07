#!/usr/bin/python3

import csv


with open('updated1_uml_xmi.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        print myupdatedCSV[0]
        
with open('updated1_images.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if myupdatedCSV[3] == "UML":
            print myupdatedCSV[2]

with open('updated2_uml_xmi.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if len(myupdatedCSV) > 0:
            print myupdatedCSV[0]
        
with open('updated2_images.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if myupdatedCSV[3] == "UML":
            print myupdatedCSV[2]

with open('updated3_uml_xmi.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        print myupdatedCSV[0]
        
with open('updated3_images.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if myupdatedCSV[3] == "UML":
            print myupdatedCSV[2]
            
with open('updated4_uml_xmi.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        print myupdatedCSV[0]
        
with open('updated4_images.csv', 'r') as csvfile:
    for myupdatedCSV in csv.reader(csvfile):
        if myupdatedCSV[3] == "UML":
            print myupdatedCSV[2]
