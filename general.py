import os 

def create_project_dir(directory):
	if not os.path.exists(directory):
		print('creating directory: ' + directory)
		os.makedirs(directory)

def create_data_files(project_name, base_url, directory):
	queue = directory + '/queue.txt'
	crawled = directory + '/crawled.txt'
	databased = directory + '/databased.txt'
	domains_covered = directory + '/domains_covered.txt'
	sql = directory +'/'+ project_name+'.sql'
	
	print('creating queue file')
	write_file(queue, base_url)
	
	print('creating crawled file')
	write_file(crawled, '')
	
	print('creating sql file')
	write_file(sql, '')
	
	print('creating databased file')
	write_file(databased, '')

	print('creating domains file')
	write_file(domains_covered, '')

def write_file(path,data):
	f = open(path, 'w')
	f.write(data)
	f.close()

def append_to_file(path, data):
	with open(path, 'a') as file :
		file.write(data + '\n')

def delete_file_contents(path):
	with open(path, 'w'):
		pass

def file_to_set(file_name):
	results = set()
	with open(file_name, 'rt') as f:
		for line in f:
			results.add(line.replace('\n', ''))
	return results

def set_to_file(links, file):
	delete_file_contents(file)
	for link in sorted(links):
		append_to_file(file, link)

def file_to_list(file_name):
	results = []
	with open(file_name, 'r') as f:
		for line in f:
			results.append(line.replace('\n', ''))
	return results

def get_path(filename):
	if '/' not in filename:
		return ''

	splitpath = filename.split('/')
	path = ''

	for i in range(0, len(splitpath)-1):
		path += splitpath[i]

	return path