##########################################################################
# preprocess email data
# 1.extract the main section pf email
# 2.create pickle file
##########################################################################



import pickle
from config import path



f = open(path.data_path+path.data_file,'rb')
data_file = pickle.load(f)
data = data_file['data']

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

keys = list(dictionary.keys())
for i in keys:
	if dictionary[i] <= frequency:
		unk_frequency += dictionary[i]
		dictionary.pop(i)
		

dictionary['<unk>'] = unk_frequency

fw = open(path.data_path+path.dict_file,'wb')
pickle.dump(dictionary,fw)