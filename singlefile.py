#!/usr/bin/env python3
# coding: utf-8
from urllib.request import urlopen
from urllib.request import Request
import sys
from sqlwriter import *
from general import *
from getMediaDetails import *
from domain import *
from spider import Spider

def inspect_url(page_url,path):
	html_string = ''
	returnlinks = set()
		
	try:	
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		headers = {'Connection' : 'keep-alive', 'User-Agent': user_agent,}
		request=Request(page_url,None,headers) #The assembled request
		response = urlopen(request)	
		handle_sql_insert(path,response, page_url, '')
		response.close()
	
	except URLError:
		print('error encountered, most likely a 404\n')
		

def inspect_filepath(path, writepath):
	if '.' not in path:
		print('no file format specified')
		sys.exit(1)

	
	handle_sql_insert_filepath(writepath, path)

	print('sql script printed at ' + writepath)

	


#MAIN START

if len(sys.argv) < 2:
	print('usage: singleFile <url/filepath>')
	sys.exit(0)

filepath = sys.argv[1]
create_project_dir('scripts')


if filepath.startswith('http://') or filepath.startswith('https://'):
	HOMEPAGE = sys.argv[1]
	DOMAIN_NAME = get_domain_name(HOMEPAGE)
	PROJECT_NAME = (DOMAIN_NAME.split('.'))[0]
	FILE_DIRECTORY = 'scripts'
	Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, FILE_DIRECTORY)
	
	
else:
	writepath = 'scripts/'
	filename = filepath.split('/')[-1]
	names  = filename.split('.')
	for i in range(0,len(names)-1):
		writepath +=  names[i] + '.'
	writepath += 'sql' 
	write_file(writepath,'')
	print(filename)
	inspect_filepath(filepath,writepath)
