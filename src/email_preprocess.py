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


def find_description(input_str):
	
	description_str = ['DESCRIPTION','Description','description']
	for i in description_str:
		if input_str.find(i)!=-1:
			return input_str.find(i)
	return -1


test_rows = []
isFirst_row = True
with open(data_path+test_file) as csvfile:
	rows = csv.reader(csvfile)

	for row in rows:
		if isFirst_row:
			isFirst_row = False
			continue
		new_row = [None,None] # 0:description

		''' row[3] is DESCRIPTION '''

		if row[3].count('\n') == 0 and len(row[3]) > 2: # only one line and word is enough
			new_row[0] = row[3]
		elif row[3].count('\n') != 0 and find_description(row[3])!=-1: # find the key word: 'description'
			description_index = -1
			for i in range(find_description(row[3]),len(row[3])):
				if row[3][i]=='\n' or row[3][i]==':':
					description_index = i+1
					break
			description_main =' '
			for i in range(description_index,len(row[3])):
				if row[3][i] == '\n' and description_main[-1] == '\n': # if appearing continuous '\n', then end 
					break
				description_main += row[3][i]
			description_main = description_main.replace('-','')
			new_row[0] = description_main
		else:
			continue
		# import pdb;pdb.set_trace()
		test_rows.append(new_row)


doc_rows = []
with open(data_path+doc_file) as csvfile:
	rows = csv.reader(csvfile)
	new_rows = []
	isFirst_row = True
	for row in rows:
		if isFirst_row:
			isFirst_row = False
			continue		
		if row[1]=='' or row[2]=='':
			continue

		new_row = ['',''] # 0:subject 1:description
		isUseful = True

		''' row[1] is Subject'''
		for i in range(len(row[1])): 
			''' remove tag [*] '''
			if row[1][i]=='[':
				isUseful = False
			elif row[1][i]==']':
				isUseful = True
			elif isUseful:
				new_row[0] += row[1][i]

		''' row[2] is Subject'''
		for i in range(len(row[2])): 
			''' remove tag [*] '''
			if row[2][i]=='[':
				isUseful = False
			elif row[2][i]==']':
				isUseful = True
			elif isUseful:
				new_row[1] += row[2][i]
		try:
			new_row[1] = new_row[1].replace('-','')
		except:
			import pdb;pdb.set_trace()


		new_rows.append(new_row)
doc_rows = new_rows
import pdb;pdb.set_trace()
