from MediaInfoDLL3 import MediaInfo

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1


def get_attr_value(info, name):
	startIndex = find_str(info, name)
	line = ''
	ret = ''

	while startIndex < len(info) and '\n' not in info[startIndex]  :
		line += info[startIndex]
		startIndex+=1 

	startIndex = find_str(line, ':')
	for i in range(startIndex+2, len(line)):
		ret += line[i] 

	return ret


def handle_attr_capture(filename, attr_name):
	handler = MediaInfo()
	handler.Open(filename)
	info  = handler.Inform()
	value = 'unable to retrieve data'
	if info:
		value  = get_attr_value( info, attr_name)

	
	handler.Close()
	return value

