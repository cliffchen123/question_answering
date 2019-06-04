##########################################################################
# transfer word to id
# 1.input: email word data (email_preprocess.py output file)
# 2.output: the format is as same as input data, and the word is transfered 
#   to id
##########################################################################


import pickle
from config import path


f = open(path.data_path+path.data_file,'rb')
data_file = pickle.load(f)
data = data_file['data']
index = data_file['index']

f = open(path.data_path+path.dict_file,'rb')
dictionary = pickle.load(f)
keys = list(dictionary.keys())
for i in range(len(data)):
	for j in range(len(data[i])):
		for k in range(len(data[i][j])):
			vocs = data[i][j][k].split()
			data[i][j][k] = []
			for v in vocs:
				if v in dictionary.keys():
					data[i][j][k].append(keys.index(v))
				# else:
				# 	data[i][j][k].append(dictionary.keys().index('<unk>'))

fw = open(path.data_path+path.data_wordid,'wb')
pickle.dump({'data':data,'index':index},fw)