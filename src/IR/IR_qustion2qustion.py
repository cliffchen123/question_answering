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
import cPickle
import csv
from config import path


f = open(path.data_path+path.data_wordid)
data = cPickle.load(f)
f = open(path.data_path+path.dict_file)
dictionary = cPickle.load(f)
f = open(path.data_path+path.data_file)
data_ori = cPickle.load(f)

# import pdb;pdb.set_trace()

dict_size = len(dictionary.keys())
doc_num = len(data['data'][0])
query_num = len(data['data'][1])
docs = data['data'][0]
queries = data['data'][1]
doc_rows_index = data['index'][0]
query_rows_index = data['index'][1]

filenameDir = [None]*2265
subject_backgroundModel = np.array([0]*dict_size)
doc_lm = []
doc_description_lm = []
backgroundLambda = 0.8  #short:0.8  long:0.9
write_top_num = 5

for doc in docs:
    hasTerm = [0]*dict_size
    termNum = [1]*dict_size
    termList = []
    subject = doc[0]
    description = doc[1]

    for i in subject:
        termNum[int(i)] += 1

    termNum = np.array(termNum)/float(sum(termNum))
    doc_lm.append(termNum)
    subject_backgroundModel = subject_backgroundModel+termNum

subject_backgroundModel = subject_backgroundModel/len(subject)

query_lm = []
for query in queries:
    hasTerm = [0]*dict_size
    termNum = [1]*dict_size
    termList = []
    description = query[0]

    for i in description:
        termNum[int(i)] += 1

    termNum = np.array(termNum)/float(sum(termNum))
    query_lm.append(termNum)


startTime = time.time()
for i in range(doc_num):
    doc_lm[i] = (1-backgroundLambda)*doc_lm[i] + backgroundLambda*subject_backgroundModel 
    doc_lm[i] = np.log(doc_lm[i])
print "Combine document model: "+str(time.time()-startTime)

alpha=0
mode='LM+b'
for i in range(query_num):
    if mode=='LM+b':
        query_lm[i] = (1-alpha)*query_lm[i] + alpha*subject_backgroundModel[i]
print "Read Query File: "+str(time.time()-startTime)


startTime = time.time()
score = [None]*query_num
kl = np.matrix(query_lm) * np.matrix(np.transpose(doc_lm))
for i in range(query_num):
    temp = [None]*doc_num
    for j in range(doc_num):
        temp[j] = (j,kl.item(i,j))
    score[i] = temp
print "Calculate Score: "+str(time.time()-startTime)


sorted_score = [None]*query_num
for i in range(query_num):
    sorted_score[i] = sorted(score[i], key=lambda (k,v): (v,k), reverse = True)

with open(path.result_path+'output.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['query description', 'query response email', 'retrieval subject', 'retrieval description'])
    for i in range(query_num):
        for j in range(write_top_num):
            index = sorted_score[i][j][0]
            # import pdb;pdb.set_trace()
            writer.writerow([data_ori['data'][1][i][0], data_ori['data'][1][i][1], data_ori['data'][0][index][0].replace('=',''), data_ori['data'][0][index][1]])