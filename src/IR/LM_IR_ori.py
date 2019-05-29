__author__ = 'slp'
import os
import math
import time
import numpy as np
import operator
import sys

test_num = len(queryList)

filenameDir = [None]*2265
backgroundModel = [0]*51253
tf = [None]*2265
backgroundLambda = 0.8  #short:0.8  long:0.9
allTermNum = 0
docTermList = [None]*2265
tdorsd = 'td'
if tdorsd=='sd':
    docPath = 'Spoken_Doc'
elif tdorsd=='td':
    docPath = 'SPLIT_DOC_WDID_NEW'
path = docPath
fileIndex = 0
for filename in os.listdir(path):
    filenameDir[fileIndex] = filename
    f = open(path+'/'+filename,'r')
    hasTerm = [0]*51253
    termNum = [0]*51253
    docTermNum = 0
    termList = []
    index=-1
    for i in f:
        index+=1
        if index < 3:
            continue
        line = i.split(' ')
        line.pop()
        for j in line:
            if j=='' or j=='-1':
                continue
            termNum[int(j)] += 1    
            allTermNum += 1
            docTermNum +=1
            termList.append(int(j))
    docTermList[fileIndex] = termList
    termNum = np.array(termNum)/float(docTermNum)
    tf[fileIndex] = termNum
    fileIndex += 1
    f.close()

startTime = time.time()
f = open('XIN1998.18461.wid.n1.lm.wid','r')
index = 0
for i in f:
    line = i.split(' ')
    backgroundModel[index] = math.e**float(line[3])
    index+=1
backgroundModel = np.array(backgroundModel)
print "Read background model: "+str(time.time()-startTime)

startTime = time.time()
for i in range(2265):
    tf[i] = (1-backgroundLambda)*tf[i] + backgroundLambda*backgroundModel 
    tf[i] = np.log(tf[i])
print "Combine document model: "+str(time.time()-startTime)

alpha=0
mode='LM+b'
queryTf = [None]*test_num
for i in range(test_num):
    if mode=='LM+b':
        queryTf[i] = (1-alpha)*query_model[i] + alpha*backgroundModel[i]
print "Read Query File: "+str(time.time()-startTime)


startTime = time.time()
score = [None]*test_num
kl = np.matrix(queryTf) * np.matrix(np.transpose(tf))
for i in range(test_num):
    temp = [None]*2265
    for j in range(2265):
        temp[j] = (filenameDir[j],kl.item(i,j))
    score[i] = temp
print "Calculate Score: "+str(time.time()-startTime)


sorted_score = [None]*test_num
for i in range(test_num):
    sorted_score[i] = sorted(score[i], key=lambda (k,v): (v,k), reverse = True)

f = open('VsmResult.txt','w')
for i in range(test_num):
    f.write('Query '+str(i)+'\t'+queryList[i]+' 2265\n')
    for j in range(2265):
        f.write(sorted_score[i][j][0]+'\r\n')

f = open('QDRelevanceTDT2_forHMMOutSideTrain.'+tdorsd+'10','w')
for i in range(test_num):
    f.write(str(i)+' '+queryList[i]+' 10\n')
    for j in range(10):
        f.write(sorted_score[i][j][0]+'\r\n')

execfile("calMap_test.py")