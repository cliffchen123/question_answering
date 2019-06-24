import math
import numpy as np
from sklearn.cluster import KMeans
import time
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import pickle

# # XIN
# datasetName = 'XIN'
# fileName = 'XIN1998.18461.wid.Train'
# dictSize = 51252
# docSize = 18461
# clustersNum = 64
# iter_num = 100

# tdt2
datasetName = 'tdt2'
fileName = 'allofdoc.txt'
dictSize = 51253
docSize = 2265
clustersNum = 64
iter_num = 100

kmeans = joblib.load(datasetName+"_kmeans"+str(clustersNum)+".m")
termVector = np.zeros((dictSize,docSize))
document = []
document_nr = []
document_word_num = np.zeros((docSize,dictSize))
term_in_doc = [None]*dictSize
for i in range(dictSize):
	term_in_doc[i]=[]


f = open(fileName,'r')
index=0
for i in f:
	i = i.split(' ')
	i.pop()
	document_i = []
	document_i_nr = []
	for j in i:
		if j!='':
			termVector[int(j)][index]=1
			document_i.append(int(j))
			document_word_num[index,int(j)]+=1
			if document_i_nr.count(int(j))==0:
				document_i_nr.append(int(j))
				term_in_doc[int(j)].append(index)
	document.append(document_i)
	document_nr.append(document_i_nr)
	index+=1
f.close()


pzd = np.random.rand(docSize,clustersNum)
for i in range(docSize):
	pzd[i]/=sum(pzd[i])

pwz = np.zeros((clustersNum,dictSize))
kmeansTransform = kmeans.transform(termVector[0:dictSize])
for i in range(clustersNum):
	temp = kmeansTransform[0:dictSize,i]
	temp = max(temp)-temp+1 #avoid zero
	temp /= sum(temp)
	pwz[i] = temp

# E steps
def Estep(pwz,pzd):
	# s = time.time()
	pzdw = [None]*docSize
	for d in range(docSize):
		pzdw[d] = dict()
	for d in range(docSize):
		# if d%100==0:
		# 	print(str(time.time()-s))
		# 	print(str(d))
		# 	s = time.time()
		for w in document_nr[d]:
			numerator = []
			denominator = 0
			numerator = pwz[:,w]*pzd[d,:]
			denominator = sum(numerator)
			# for z in range(clustersNum):
			# 	temp = pwz[z][w]*pzd[d][z]
			# 	numerator.append(temp)
			# 	denominator += temp
			pzdw[d][w] = numerator/denominator
	return pzdw

# M step
def Mstep(pzdw):

	# update pwz
	new_pwz = np.ones((clustersNum,dictSize))
	for z in range(clustersNum):
		# print(str(z))
		numerator = []
		denominator = 0
		for w in range(dictSize):
			# print(str(w))
			# temp = document_word_num[:,w]*pzdw[:,w,z]
			temp = 0
			for d in term_in_doc[w]:
				temp += document_word_num[d][w]*pzdw[d][w][z]
			numerator.append(temp)
			denominator += temp
		new_pwz[z] = np.array(numerator)/denominator

	# update pzd
	new_pzd = np.ones((docSize,clustersNum))
	for d in range(docSize):
		numerator = []
		denominator = len(document[d])
		for z in range(clustersNum):
			temp = 0
			for w in document_nr[d]:
				temp += document_word_num[d][w]*pzdw[d][w][z]
			numerator.append(temp)
		new_pzd[d] = np.array(numerator)/denominator

	return new_pwz,new_pzd

# Obj function
def Obj(pwz,pzd,pzdw):
	result = 0
	for d in range(docSize):
		for w in document_nr[d]:
			temp = pwz[:,w]*pzd[d,:]
			for i in range(len(temp)):
				if temp[i]==0:
					temp[i]=1
			temp = sum(pzdw[d][w][:]*np.log(temp))
			# temp = 0
			# for z in range(clustersNum):
			# 	if pwz[z,w]*pzd[d,z]==0:
			# 		print "d:"+str(d)+" w:"+str(w)+" z:"+str(z)
			# 		return
			# 	else:
			# 		temp += (pzdw[d][w][z]*math.log(pwz[z,w]*pzd[d,z]))
			result += document_word_num[d][w]*temp
	return result

pzdw = []
print("### " + datasetName + " training start")
for i in range(iter_num):
	
	print("\n---Iter "+str(i+1)+"-----")

	print("Estep start")
	startTime = time.time()
	pzdw = Estep(pwz,pzd)
	print("Estep finish time:"+str(time.time()-startTime))

	print("Mstep start")
	startTime = time.time()
	pwz,pzd = Mstep(pzdw)
	print("Mstep finish time:"+str(time.time()-startTime))

	print("Obj start")
	startTime = time.time()
	print("Obj function: "+str(Obj(pwz,pzd,pzdw)))
	print("Obj finish time:"+str(time.time()-startTime))	

with open(datasetName + '_plsa.pickle', 'w') as f:
	pickle.dump([pwz,pzd], f)

# with open(datasetName + '_plsa.pickle') as f:
# 	pwz,pzd = pickle.load(f)