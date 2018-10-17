#!/usr/bin/env python3
# coding: utf-8
import os
import os.path
from sqlwriter import *

def extract_sql_statements(insertfile):
	retstring = ''

	with open(insertfile, 'r') as file :
		retstring = file.read()

	return retstring


#MAIN START#
writepath = 'scripts/mergedscripts.sql' 
folder = 'scripts'
mergedstatements = ''

if not folder:
	folder = '.'

for dirpath, dirnames, filenames in os.walk(folder):
	for filename in [f for f in filenames if f.endswith('.sql') and 'mergedscripts' not in f]:
		insertfile = os.path.join(dirpath, filename)
		mergedstatements += extract_sql_statements(insertfile)

write_file(writepath,mergedstatements)
        