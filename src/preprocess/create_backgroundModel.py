##########################################################################
# Penn Treebank(PTB) Introduction:
#	The Penn Treebank, in its eight years of operation (1989-1996), produced
#	approximately 7 million words of part-of-speech tagged text, 3 million words of skeletally parsed text, 
#	over 2 million words of text parsed for predicateargument structure, 
#	and 1.6 million words of transcribed spoken text annotated for speech disfluencies. 
#	The material annotated includes such wideranging genres as IBM computer manuals, nursing notes, 
#	Wall Street Journal articles, and transcribed telephone conversations, among others.
##########################################################################
import chainer
import numpy as np
import pickle
import os
from config import path

''' Load PTB dataset '''
train, val, test = chainer.datasets.get_ptb_words()
allData = train.tolist()+val.tolist()+test.tolist()
print('train length: ', train.shape)
print('val   length: ', val.shape)
print('test  length: ', test.shape)
ptb_dict = chainer.datasets.get_ptb_words_vocabulary()
ptb_id_word_dict = dict((v, k) for k, v in ptb_dict.items())
print('Number of vocabulary in ptb: '+str(len(ptb_dict)))

''' Load Mail dataset '''
with open(os.path.join(path.data_path,path.dict_file),'rb') as f:
	local_dict = pickle.load(f)
f = open(os.path.join(path.data_path,path.data_wordid),'rb')
data = pickle.load(f)
data = data['data']

count = 0
for v in local_dict:
	if v in ptb_dict:
		count+=1
print("Number of vocabulary in local database: "+str(len(local_dict)))
print("overlap word: "+str(count))

''' combine ptb background model and mail background model '''
# mail background model
backgroundModel_lambda = 0.8
local_backgroundModel = np.array([0.0]*len(local_dict))
for DorQ in range(len(data)):
	for eachData in range(len(data[DorQ])):
		for dataType in range(len(data[DorQ][eachData])):
			for v in data[DorQ][eachData][dataType]:
				local_backgroundModel[v]+=1
local_backgroundModel = local_backgroundModel/sum(local_backgroundModel)

# ptb background model
backgroundModel = [0]*len(local_dict)
for v in allData:
	if ptb_id_word_dict[v] in ptb_dict and ptb_id_word_dict[v] in local_dict:
		backgroundModel[ local_dict[ptb_id_word_dict[v]][0] ]+=1
backgroundModel = np.array(backgroundModel)
backgroundModel = backgroundModel/float(sum(backgroundModel))
backgroundModel = backgroundModel_lambda*backgroundModel + (1-backgroundModel_lambda)*local_backgroundModel

with open(os.path.join(path.data_path,path.BGM_file),'wb') as fw:
	pickle.dump(backgroundModel,fw)


''' create key word list '''
with open(os.path.join(path.data_path,path.keyword_file),'w') as fw:
	sort_dict = sorted(local_dict.items(),key=lambda x:x[1][0])
	word_list = [x[0] for x in sort_dict]
	keyword = dict(zip(word_list,backgroundModel.tolist()))
	keyword = sorted(keyword.items(),key=lambda x:x[1],reverse=True)
	for v in keyword:
		fw.write(v[0]+' , '+str(v[1])+'\n')
	


# import pdb;pdb.set_trace()
# Kneser-Ney smoothing
