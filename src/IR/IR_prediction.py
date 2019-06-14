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
# import tkinter as tk
# from scipy.sparse import csr_matrix

usingGUI = True

f = open(os.path.join(path.data_path,path.data_wordid),'rb')
data = pickle.load(f)
f = open(os.path.join(path.data_path,path.dict_file),'rb')
dictionary = pickle.load(f)
f = open(os.path.join(path.data_path,path.data_file),'rb')
data_ori = pickle.load(f)

# import pdb;pdb.set_trace()

dict_size = len(dictionary.keys())
doc_num = len(data['data'][0])
docs = data['data'][0]
queries = data['data'][1]
doc_rows_index = data['index'][0]
query_rows_index = data['index'][1]

backgroundLambda = 0.8 
write_top_num = 5

''' generate document language model '''
doc_lm = []
subject_backgroundModel = np.array([0]*dict_size)
for doc in docs:
    termNum = [1]*dict_size
    subject = doc[0]
    description = doc[1]

    for i in subject:
        termNum[int(i)] += 1

    termNum = np.array(termNum)/float(sum(termNum))
    doc_lm.append(termNum)
    subject_backgroundModel = subject_backgroundModel+termNum
subject_backgroundModel = subject_backgroundModel/len(subject)



''' combine document model and backround model'''
startTime = time.time()
for i in range(doc_num):
    doc_lm[i] = (1-backgroundLambda)*doc_lm[i] + backgroundLambda*subject_backgroundModel 
    doc_lm[i] = np.log(doc_lm[i])
doc_lm = np.matrix(np.transpose(doc_lm))
# doc_lm = csr_matrix(doc_lm)
# import pdb;pdb.set_trace()
# with open(path.result_IR_path+'docLM.pickle','wb') as f:
#     pickle.dump(doc_lm,f)
print("Combine document model: "+str(time.time()-startTime))


''' generate query language model '''
with open(os.path.join(path.result_IR_path,'oneQuery.csv'),'w', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['query description', 'retrieval subject', 'retrieval description'])
while True:
    query_str = input("Please input subject:")

    vocs = query_str.split()
    query = []
    for v in vocs:
        if v in dictionary:
            query.append(dictionary[v][0])    

    query_lm = []
    termNum = [1]*dict_size

    for i in query:
        termNum[int(i)] += 1

    query_lm.append(np.array(termNum)/float(sum(termNum)))

    ''' combine query model and backround model'''
    alpha=0
    mode='LM+b'
    if mode=='LM+b':
        query_lm = (1-alpha)*query_lm + alpha*subject_backgroundModel
    query_lm = np.matrix(query_lm)
    print("Read Query File: "+str(time.time()-startTime))

    ''' calculate KL score '''
    startTime = time.time()
    kl = query_lm * doc_lm

    
    temp = [None]*doc_num
    for j in range(doc_num):
        temp[j] = (j,kl.item(0,j))
    score = temp
    print("Calculate Score: "+str(time.time()-startTime))

    ''' rank document and write file '''
    sorted_score = sorted(score, key=lambda x:(x[1], x[0]), reverse = True)

    
    with open(os.path.join(path.result_IR_path,'oneQuery.csv'),'a', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        for j in range(write_top_num):
            index = sorted_score[j][0]
            # import pdb;pdb.set_trace()
            writer.writerow([query_str, data_ori['data'][0][index][0].replace('=',''), data_ori['data'][0][index][1]])
            print(str(j+1)+':')
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print("Retrieval Email Subject:")
            print("------------------------------------------------")
            print(data_ori['data'][0][index][0].replace('=',''))
            print("------------------------------------------------\n")
            print("Retrieval Email Description:")
            print("------------------------------------------------")
            print(data_ori['data'][0][index][1])
            print("------------------------------------------------\n")
