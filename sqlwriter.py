import os
from general import *
from domain import *
from urllib.parse import urlparse
from PIL import ImageFile
from PIL import Image
from io import BytesIO
from getMediaDetails import handle_attr_capture
import time
import datetime

CATEGORY = ''

def handle_sql_insert(path,response, link, parent_link):
	parsedlink = urlparse(link)
	readresponse = response.read()
	header = response.getheader('Content-Type')
	#TODO
	


	
	name = '\'index.html\''
	if parsedlink.path.split('/')[-1]:
		name = '\'' + (parsedlink.path.split('/')[-1]) + '\''
	
	creatorname = get_domain_name(link).split('.')[0]
	
	creationtime = '\'' + response.getheader('Date') + '\''
	modificationtime = creationtime
	containsdagrs = '0'
	if 'html' in header:
		containsdagrs = '1' 

	filesize = '\'' + str(len(readresponse)) + '\''
	storagepath = '\'' + link + '\''
	keywords = creatorname
	
	for keyword in parsedlink.path.split('/'):
		if keyword:
			keywords = keywords + ', '+ keyword

	keywords = '\'' + keywords + '\''
	domain = creatorname
	creatorname = '\'' + creatorname + '\''
	#category = creatorname
	
	domainpath = 'scripts/domains_covered.txt'
	domains = file_to_list(domainpath)
	

	if domain not in domains:
		create_CATEGORY(path, domain, domain)
		insert_CATEGORY(path)
		append_to_file(domainpath, domain)


	insert_DAGR(path, name, creatorname, creationtime, modificationtime, containsdagrs, filesize, storagepath, keywords)
	#insert_CATEGORY(path, category)
	
	if 'html' in header:
		insert_HTML(path)
		
	else :
		if 'image' in header or link.endswith('.png') or link.endswith('.jpg') or link.endswith('jpeg') or  link.endswith('JPG') or link.endswith('PNG'):
			print('img')
			dimensions = get_image_dimensions(response)
			resolution = getDPI(response)
			insert_IMAGE(path, dimensions,resolution)
			
		else:
			if 'video' in header or link.endswith('.mp4') or link.endswith('.mov'):
				if link.endswith('.mp4') :
					filename = generate_temp(response, '.mp4')
					length = '\'' + handle_attr_capture(filename, 'Duration').replace('\n', '').replace('\r', '') + '\''
					framewidth = leading_number(handle_attr_capture(filename, 'Width'))
					frameheight = leading_number(handle_attr_capture(filename, 'Height'))
					framerate = leading_number(handle_attr_capture(filename, 'Frame rate    '))
					insert_VIDEO(path, length, framewidth, frameheight, framerate)
				if link.endswith('.mov') : 
					filename = generate_temp(response, '.mov')
					length = '\'' + handle_attr_capture(filename, 'Duration').replace('\n', '').replace('\r', '') + '\''
					framewidth = leading_number(handle_attr_capture(filename, 'Width'))
					frameheight = leading_number(handle_attr_capture(filename, 'Height'))
					framerate = leading_number(handle_attr_capture(filename, 'Frame rate     '))
					insert_VIDEO(path, length, framewidth, frameheight, framerate)
				#insert_CATEGORY(path, 'VIDEO')	
			else: 
				if 'audio' in header or link.endswith('.mp3') or link.endswith('.wav'):
					if link.endswith('.mp3') :
						filename = generate_temp(response, '.mp3')
						length = '\'' + handle_attr_capture(filename, 'Duration').replace('\n', '').replace('\r', '') + '\''
						bitrate = leading_number(handle_attr_capture(filename, 'Overall bit rate   ')) #keep the spaces in this string
						channels = leading_number(handle_attr_capture(filename, 'Channel(s)'))
						audiosamplerate = leading_number(handle_attr_capture(filename, 'Sampling rate'))
						insert_AUDIO(path, length, bitrate, channels, audiosamplerate)
					if link.endswith('.wav') : 
						filename = generate_temp(response, '.wav')
						length = '\'' + handle_attr_capture(filename, 'Duration').replace('\n', '').replace('\r', '') + '\''
						bitrate = leading_number(handle_attr_capture(filename, 'Overall bit rate   ')) #keep the spaces in this string
						channels = leading_number(handle_attr_capture(filename, 'Channel(s)'))
						audiosamplerate = leading_number(handle_attr_capture(filename, 'Sampling rate'))
						insert_AUDIO(path, length, bitrate, channels, audiosamplerate)
					#insert_CATEGORY(path, 'AUDIO')
				else: 
					if link.endswith('.txt') :
						filename = generate_temp(response, '.txt')
						wordcount = str(get_wordcount(filename))
						charcount = str(get_charcount(filename))
						insert_TEXT(path, wordcount, charcount)
						#insert_CATEGORY(path, 'TEXT')
					if link.endswith('.pdf') or  link.endswith('.doc') or link.endswith('.docx'):
						insert_TEXT(path, '0', '0')
						#insert_CATEGORY(path, 'TEXT')
					else:
						copyright = creatorname
						fileversion = '\'1.0\''
						language =  "\'English\'"
						insert_SOFTWARE(path,copyright,fileversion,language)
						#insert_CATEGORY(path, 'SOFTWARE')
						
	if parent_link:
		insert_HAS( path, parent_link)
	insert_HAS(path,domain)
	

def leading_number(string):
	temp = string.split()
	ret = ''
	for item in temp:
		if item.isdigit() or '.' in item:
			ret += item
	
	return ret

def generate_temp(response, ext):
	filename = 'tempfile' + ext
	data = response.read()
	with open(filename , 'wb') as out:
		out.write(data)
	return filename

def get_image_dimensions(response):
    # get image size (None if not known)
    p = ImageFile.Parser()
    while 1:
        data = response.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            height, width  = p.image.size
            return '\'' + str(height) + 'X' + str(width) + '\''
            break
    return '\'0x0\''

def get_image_dimensions_file(file):
    # get image size (None if not known)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            height, width  = p.image.size
            return '\'' + str(height) + 'X' + str(width) + '\''
            break
    return '\'0x0\''

def getDPI(response):
	try:

		img  = Image.open(BytesIO(response.read()))
		info = img.info
	
		if info['dpi']:
			dpix, dpiy = info['dpi']
			return '\'' + str(dpix) + 'dpiX' + str(dpiy) +'dpi\''
		else:
			return '\'72dpix72dpi\''
	except:
		return '\'72dpix72dpi\''

def getDPI_file(file):
	try:

		img  = Image.open(BytesIO(file.read()))
		info = img.info
	
		if info['dpi']:
			dpix, dpiy = info['dpi']
			return '\'' + str(dpix) + 'dpiX' + str(dpiy) +'dpi\''
		else:
			return '\'72dpix72dpi\''
	except:
		return '\'72dpix72dpi\''


def get_wordcount(filename):
	count = 0
	with open(filename,'r') as file:
		words = file.read().split()
		count = len(words)
	return count


def get_charcount(filename):
	count = 0
	with open(filename,'r') as file:
		words = file.read()
		count = len(words)
	return count

def insert_DAGR(path, name, creatorname, creationtime, modificationtime, containsdagrs, filesize, storagepath, keywords):
	statement = 'SET @GUID = (SELECT UUID());'
	print(statement)
	append_to_file(path, statement)
	statement = 'insert into DAGR (guid,name,creatorname,creationtime,modificationtime,containsdagrs,filesize,storagepath,keywords) values ( @GUID ,' + name + ',' + creatorname + ',' + creationtime + ',' + modificationtime +',' + containsdagrs + ','+ filesize + ','+ storagepath+ ',' + keywords + ' );\n' 
	print(statement)
	append_to_file(path, statement)


def insert_TEXT(path, wordcount, charcount):
	statement = 'insert into TEXT (id,wordcount,charcount) values ( @GUID,' + wordcount + ',' + charcount + ');\n' 
	print(statement)
	append_to_file(path, statement)

def insert_IMAGE(path, dimensions,resolution):
	statement = 'insert into IMAGE (id,dimensions,resolution) values ( @GUID,' + dimensions + ',' + resolution+');\n' 
	print(statement)
	append_to_file(path, statement)

def insert_VIDEO(path, length, framewidth, frameheight, framerate):
	statement = 'insert into VIDEO (id,length,framewidth,frameheight,framerate) values ( @GUID,' + length + ',' + framewidth + ',' + frameheight + ',' + framerate + ');\n' 
	print(statement)
	append_to_file(path, statement)

def insert_AUDIO(path, length, bitrate, channels, audiosamplerate):
	statement = 'insert into AUDIO (id,length,bitrate,channels,audiosamplerate) values ( @GUID,' + length +  ',' + bitrate + ',' + channels + ',' + audiosamplerate +');\n' 
	print(statement)
	append_to_file(path, statement)

def insert_SOFTWARE(path, copyright,fileversion,language):
	statement = 'insert into SOFTWARE (id,copyright,fileversion,language) values ( @GUID ,' + copyright + ',' + fileversion + ',' + language + ');\n' 
	print(statement)
	append_to_file(path, statement)

def insert_HTML(path):
	statement = 'insert into HTML (id) values (@GUID);\n' 
	print(statement)
	append_to_file(path, statement)

def insert_HAS(path, parent_link):
	statement = 'SET @HID = (SELECT GUID FROM DAGR WHERE STORAGEPATH=\'' + parent_link +  '\');'
	print(statement)
	append_to_file(path, statement)
	statement = 'insert into HAS (guid,hid) values ( @HID, @GUID );\n' 
	print(statement)
	append_to_file(path, statement)

def insert_HAS_from_databased_Items(path,link, parent_link):
	print(link + ' already in database, adding to HAS')
	statement = 'SET @GUID = (SELECT GUID FROM DAGR WHERE STORAGEPATH=\'' + link +  '\');'
	print(statement)
	append_to_file(path, statement)
	insert_HAS(path, parent_link)

def insert_CATEGORY(path):
	statement = 'insert into CATEGORY (id) values (@GUID);\n' 
	print(statement)
	append_to_file(path, statement)

def create_CATEGORY(path, category, filepath):
	print('creating category: ' + category)
	keywords = '\'category, ' + category + '\''
	category = '\'' + category + '\'' 
	time = '\'' + str(datetime.datetime.now()) + '\''
	notapplicable = '\'N/A\''
	filepath = '\'' + filepath + '\''
	insert_DAGR(path, category, notapplicable , time , time , '1', '0', filepath, keywords)
 
def handle_sql_insert_filepath(path,filepath):
	
	name = filepath.split('/')[-1]
	creatorname = 'user submission'
	#if not filepath.split('/')[1] == 'uploadedFiles':
	#	creatorname = filepath.split('/')[1]

	creationtime = '\'' + str(datetime.datetime.now()) + '\''
	modificationtime = creationtime
	containsdagrs = '0'
	#category = get_path(filepath)
	#if not category:
		#category = 'user submission'
	#category = '\'' + category +'\''

	filesize = str(float(leading_number(handle_attr_capture(filepath, 'File size')))*1000*1000)
	filesize = filesize.split('.')[0]
	storagepath = '\'' + filepath + '\''
	keywords = creatorname
	
	for keyword in filepath.split('\\'):
		if keyword:
			keywords = keywords + ', '+ keyword

	keywords += ', USERMADE'
	keywords = '\'' + keywords + '\''
	creatorname = '\'' + creatorname + '\''
	
	if filepath.endswith('html') :
		containsdagrs =  1;

	name = '\'' + name + '\''
	insert_DAGR(path, name, creatorname, creationtime, modificationtime, containsdagrs, filesize, storagepath, keywords)
	#insert_CATEGORY(path, category)

	if filepath.endswith('html') :
		insert_HTML(path)
		#insert_CATEGORY(path, 'HTML')
	else :
		if  filepath.endswith('.png') or filepath.endswith('.jpg') or filepath.endswith('jpeg') or  filepath.endswith('JPG') or filepath.endswith('PNG'):
			print('img')
			file = open(filepath , 'rb')
			dimensions = get_image_dimensions_file(file)
			resolution = getDPI_file(file)
			file.close()
			insert_IMAGE(path, dimensions,resolution)
			#insert_CATEGORY(path, 'IMAGE')
		else:
			if filepath.endswith('.mp4') or filepath.endswith('.mov'):
				if filepath.endswith('.mp4') :
					length = '\'' + handle_attr_capture(filepath, 'Duration').replace('\n', '').replace('\r', '') + '\''
					framewidth = leading_number(handle_attr_capture(filepath, 'Width'))
					frameheight = leading_number(handle_attr_capture(filepath, 'Height'))
					framerate = leading_number(handle_attr_capture(filepath, 'Frame rate   ')) # keep spaces here
					print('framerate: ' + framerate)
					insert_VIDEO(path, length, framewidth, frameheight, framerate)
				if filepath.endswith('.mov') : 
					length = '\'' + handle_attr_capture(filepath, 'Duration').replace('\n', '').replace('\r', '') + '\''
					framewidth = leading_number(handle_attr_capture(filepath, 'Width'))
					frameheight = leading_number(handle_attr_capture(filepath, 'Height'))
					framerate = leading_number(handle_attr_capture(filepath, 'Frame rate   ')) # keep spaces here
					insert_VIDEO(path, length, framewidth, frameheight, framerate)
				#insert_CATEGORY(path, 'VIDEO')	
			else: 
				if filepath.endswith('.mp3') or filepath.endswith('.wav'):
					if filepath.endswith('.mp3') :
						length = '\'' + handle_attr_capture(filepath, 'Duration').replace('\n', '').replace('\r', '') + '\''
						bitrate = leading_number(handle_attr_capture(filepath, 'Overall bit rate   ')) #keep the spaces in this string
						channels = leading_number(handle_attr_capture(filepath, 'Channel(s)'))
						audiosamplerate = leading_number(handle_attr_capture(filepath, 'Sampling rate'))
						insert_AUDIO(path, length, bitrate, channels, audiosamplerate)
					if filepath.endswith('.wav') : 
						length = '\'' + handle_attr_capture(filepath, 'Duration').replace('\n', '').replace('\r', '') + '\''
						bitrate = leading_number(handle_attr_capture(filepath, 'Overall bit rate   ')) #keep the spaces in this string
						channels = leading_number(handle_attr_capture(filepath, 'Channel(s)'))
						audiosamplerate = leading_number(handle_attr_capture(filepath, 'Sampling rate'))
						insert_AUDIO(path, length, bitrate, channels, audiosamplerate)
					#insert_CATEGORY(path, 'AUDIO')
				else: 
					if filepath.endswith('.txt') :
						wordcount = str(get_wordcount(filepath))
						charcount = str(get_charcount(filepath))
						insert_TEXT(path, wordcount, charcount)
						#insert_CATEGORY(path, 'TEXT') 
					else:
						if filepath.endswith('.pdf') or  filepath.endswith('.doc') or filepath.endswith('.docx'):
							insert_TEXT(path, '0', '0')
							#insert_CATEGORY(path, 'TEXT')
						else:
							copyright = creatorname
							fileversion = '\'1.0\''
							language =  "\'English\'"
							insert_SOFTWARE(path,copyright,fileversion,language)
						#insert_CATEGORY(path, 'SOFTWARE')
	
	
	
	folders = filepath.split('/')
	folder = ''

	for i in range(0,len(folders)-2):
		folder+= folders[i] + '/'
	folder += folders[-2]

	if len(folders) > 1 and folders[-2] != 'uploadedFiles':
		insert_HAS(path, folder)
	#		for i in range(0, len(folders)-1):
	#			insert_HAS(path, folders[i])