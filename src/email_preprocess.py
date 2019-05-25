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
	index = -1
	description_str = ['DESCRIPTION','Description','description']
	for i in description_str:
		if input_str.find(i)!=-1:
			return index
	return index


test_rows = []
with open(data_path+test_file) as csvfile:
	rows = csv.reader(csvfile)
	for row in rows:
		new_row = [None,None]

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
			description_main.replace('-','')
			new_row[0] = description_main
		else:
			continue
		# import pdb;pdb.set_trace()
		test_rows.append(new_row)
doc_rows = []
with open(data_path+doc_file) as csvfile:
	rows = csv.reader(csvfile)
	new_rows = []
	for row in rows:
		new_row = ''
		isUseful = True

		''' row[1] is Subject'''
		for i in range(len(row[1])): 
			if row[1][i]=='[':
				isUseful = False
			elif row[1][i]==']':
				isUseful = True
			elif isUseful:
				new_row = row[1][i]
		new_rows.append(new_row)
doc_rows = new_rows
import pdb;pdb.set_trace()
