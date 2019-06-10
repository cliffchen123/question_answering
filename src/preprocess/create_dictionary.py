##########################################################################
# preprocess email data
# 1.extract the main section pf email
# 2.create pickle file
##########################################################################



import pickle
import os
from config import path



f = open(os.path.join(path.data_path,path.data_file),'rb')
data_file = pickle.load(f)
data = data_file['data']

# dictionary: {word1:(index1,frequency1),word2:(index2,frequency2),...}
dictionary = dict()

for i in range(len(data)):
	for j in range(len(data[i])):
		for k in range(len(data[i][j])):
			vocs = data[i][j][k].split()
			for v in vocs:
				if v not in dictionary.keys():
					dictionary[v] = 1
				else:
					dictionary[v] += 1

frequency = 1
unk_frequency = 0

index = 0
keys = list(dictionary.keys())
for i in keys:
	if dictionary[i] <= frequency:
		unk_frequency += dictionary[i]
		dictionary.pop(i)
	else:
		dictionary[i] = [index,dictionary[i]]
		index += 1
		

dictionary['<unk>'] = [index, unk_frequency]


fw = open(os.path.join(path.data_path,path.dict_file),'wb')
pickle.dump(dictionary,fw)