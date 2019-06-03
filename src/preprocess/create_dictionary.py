##########################################################################
# preprocess email data
# 1.extract the main section pf email
# 2.create pickle file
##########################################################################



import cPickle
from config import path



f = open(path.data_path+path.data_file,'r')
data_file = cPickle.load(f)
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
for i in dictionary.keys():
	if dictionary[i] <= frequency:
		unk_frequency += dictionary[i]
		dictionary.pop(i)
		

dictionary['<unk>'] = unk_frequency

fw = open(path.data_path+path.dict_file,'w')
cPickle.dump(dictionary,fw)