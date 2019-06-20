##########################################################################
# information retrieval: qustion to qustion
# 1.use language model to calculate kl score
# 3.backgroundLambda is tunable parameter
# 2.write csv file
##########################################################################

import os
import math
import time
import numpy as np
import operator
import sys
import pickle
import csv
from config import path
# from scipy.sparse import csr_matrix

f = open(os.path.join(path.data_path,path.data_wordid),'rb')
data = pickle.load(f)
f = open(os.path.join(path.data_path,path.dict_file),'rb')
dictionary = pickle.load(f)
f = open(os.path.join(path.data_path,path.data_file),'rb')
data_ori = pickle.load(f)
f = open(os.path.join(path.data_path,path.BGM_file),'rb')
backgroundModel = pickle.load(f)
# import pdb;pdb.set_trace()

dict_size = len(dictionary.keys())
doc_num = len(data['data'][0])
query_num = len(data['data'][1])
docs = data['data'][0]
queries = data['data'][1]
# doc_rows_index = data['index'][0]
# query_rows_index = data['index'][1]

backgroundLambda = 0.8 
write_top_num = 5

''' generate document language model '''
doc_lm = []
subjectLambda = 0.7 # subject linear combine description
descriptionLambda = 1 - subjectLambda
for doc in docs:
    termNum = [1]*dict_size
    subject = doc[0]
    description = doc[1]

    for i in subject:
        termNum[int(i)] += subjectLambda
    for i in description:
        termNum[int(i)] += descriptionLambda

    termNum = np.array(termNum)/float(sum(termNum))
    doc_lm.append(termNum)


''' generate query language model '''
query_lm = []
for query in queries:
    termNum = [1]*dict_size
    description = query[0]

    for i in description:
        termNum[int(i)] += 1

    termNum = np.array(termNum)/float(sum(termNum))
    query_lm.append(termNum)

''' combine document model and backround model'''
startTime = time.time()
for i in range(doc_num):
    doc_lm[i] = (1-backgroundLambda)*doc_lm[i] + backgroundLambda*backgroundModel 
    doc_lm[i] = np.log(doc_lm[i])
doc_lm = np.matrix(np.transpose(doc_lm))
# with open(path.result_IR_path+'docLM.pickle','wb') as f:
#     pickle.dump(doc_lm,f)
print("Combine document model: "+str(time.time()-startTime))

''' combine query model and backround model'''
alpha=0
mode='LM+b'
for i in range(query_num):
    if mode=='LM+b':
        query_lm[i] = (1-alpha)*query_lm[i] + alpha*backgroundModel
query_lm = np.matrix(query_lm)
print("Read Query File: "+str(time.time()-startTime))

''' calculate KL score '''
startTime = time.time()
score = [None]*query_num
kl = query_lm * doc_lm
for i in range(query_num):
    temp = [None]*doc_num
    for j in range(doc_num):
        temp[j] = (j,kl.item(i,j))
    score[i] = temp
print("Calculate Score: "+str(time.time()-startTime))

''' rank document and write file '''
sorted_score = [None]*query_num
for i in range(query_num):
    sorted_score[i] = sorted(score[i], key=lambda x:(x[1], x[0]), reverse = True)

with open(os.path.join(path.result_IR_path,'output.csv'),'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['query description', 'query response email', 'retrieval subject', 'retrieval description'])
    for i in range(query_num):
        for j in range(write_top_num):
            index = sorted_score[i][j][0]
            # import pdb;pdb.set_trace()
            writer.writerow([data_ori['data'][1][i][0], data_ori['data'][1][i][1], data_ori['data'][0][index][0].replace('=',''), data_ori['data'][0][index][1]])