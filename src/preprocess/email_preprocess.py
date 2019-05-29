##########################################################################
# preprocess email data
# 1.extract the main section pf email
# 2.create pickle file
##########################################################################

import csv
import cPickle

data_path = '../data/'
test_file = 'NABU FAQ for Worry Free Product 20190401.csv'
doc_file = 'WF Cases 20190517.csv'


def find_important_tag_index(input_str):
	
	description_str = ['DESCRIPTION','Description','description','Issue:','[Issue]','Problem:']
	for i in description_str:
		if input_str.find(i)!=-1:
			return input_str.find(i)+len(i)
	return -1

def find_main(input_str):
	tag = ['[',':']
	result = ''
	split_line = input_str.split(' ')
	
	for i in split_line:
		isInclude_tag = False
		for j in tag:
			if i.find(j)!=-1:
				isInclude_tag = True
		if not isInclude_tag:
			result += (' '+i)
		else:
			break
	if result.count(' ') > 3: # if result is more than 3 words, then determine it is main instead of tag
		return result
	else:
		return ''

def isPhone(input_str):
	for i in input_str:
		if (i>'9' or i<'0') and i!='+' and i!='-':
			return False
	return True

def remove_garbage_information(input_str):
	split_str = input_str.split(' ')
	result = ''
	for i in split_str:
		if i.find('@')!=-1 or isPhone(i): # if str is email adress or phone number
			continue
		result += (' '+i)
	return result


test_rows = []
isFirst_row = True
with open(data_path+test_file) as csvfile:
	rows = csv.reader(csvfile)

	for row in rows:
		if isFirst_row:
			isFirst_row = False
			continue
		new_row = [None,None] # 0:description

		description = row[3]

		''' DESCRIPTION '''
		if find_main(description)!='': # determine the start of mail is main not tag
			new_row[0] = find_main(description)
		elif description.count('\n') != 0 and find_important_tag_index(description)!=-1: # find the key word: 'description',..
			description_index = -1
			for i in range(find_important_tag_index(description),len(description)):
				if description[i]=='\n' or description[i]==':':
					description_index = i+1
					break
			description_main =' '
			for i in range(description_index,len(description)):
				if description[i] == '\n' and description_main[-1] == '\n': # if appearing continuous '\n', then end 
					break
				description_main += description[i]
			description_main = description_main.replace('-','')
			new_row[0] = description_main
		else:
			continue
		new_row[0] = remove_garbage_information(new_row[0])
		# import pdb;pdb.set_trace()
		test_rows.append(new_row)


doc_rows = []
with open(data_path+doc_file) as csvfile:
	rows = csv.reader(csvfile)
	new_rows = []
	isFirst_row = True
	for row in rows:
		subject = row[1]
		description = row[2]

		if isFirst_row:
			isFirst_row = False
			continue		
		if subject=='' or description=='':
			continue

		new_row = ['',''] # 1:subject 2:description
		isUseful = True

		''' Subject '''
		for i in range(len(subject)): 
			''' remove tag [*] '''
			if subject[i]=='[':
				isUseful = False
			elif subject[i]==']':
				isUseful = True
			elif isUseful:
				new_row[0] += subject[i]

		''' Description '''
		if description.find('[') == -1 and description.find(':') == -1: # if not including any tag
			new_row[1] = description
		elif find_main(description)!='': # determine the start of mail is main not tag
			new_row[1] = find_main(description)
		elif find_important_tag_index(description) != -1: # find the key word: 'description',..
			for i in range(find_important_tag_index(description)+1,len(description)): # +1 is to jump the ':' and ']'
				if description[i]==':' or description[i]=='[':
					break
				new_row[1] += description[i]
		new_row[1] = new_row[1].replace('-','')
		new_row[1] = remove_garbage_information(new_row[1])

		new_rows.append(new_row)
doc_rows = new_rows

''' write file '''
f = open(data_path+'data.cpickle','w')
cPickle.dump([doc_rows,test_rows],f)
# import pdb;pdb.set_trace()
