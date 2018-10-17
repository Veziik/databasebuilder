#!/usr/bin/env python3
# coding: utf-8
import os
import os.path
import sys
from sqlwriter import *

if len(sys.argv) < 2:
	sys.exit(1)

folder = sys.argv[1]
writename = folder.split('/')[-1]
create_project_dir('scripts')
writepath = 'scripts/' + writename + '.sql' 
dirpaths = []
write_file(writepath,'')
if not folder:
	folder = '.'

for dirpath, dirnames, filenames in os.walk(folder):
    if dirpath not in dirpaths:
            dirpaths.append(dirpath)
            split = dirpath.split('/')
            if len(split) > 2:
                create_CATEGORY(writepath, split[-1], dirpath)
                insert_CATEGORY(writepath)
                parent = ''
                child = ''
                for i in range(0,len(split) -1) :
                    if i < len(split) -2 :
                        child += split[i] + '/'
                    parent += split[i] + '/'

                parent +=  split[-1]
                child += split[-2]
                insert_HAS_from_databased_Items(writepath,parent, child)
            else:
                create_CATEGORY(writepath, dirpath, dirpath)
                insert_CATEGORY(writepath)

    for filename in [f for f in filenames ]:
        insertfile = os.path.join(dirpath, filename)
        
        print(insertfile)
        handle_sql_insert_filepath(writepath,insertfile)