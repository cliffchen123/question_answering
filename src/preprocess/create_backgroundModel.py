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
train, val, test = chainer.datasets.get_ptb_words()
print('train length: ', train.shape)
print('val   length: ', val.shape)
print('test  length: ', test.shape)
ptb_dict = chainer.datasets.get_ptb_words_vocabulary()
print('Number of vocabulary', len(ptb_dict))
backgroundModel = [1]*len(ptb_dict)
for i in train:
	if i in ptb_dict:
		backgroundModel[ptb_dict[i]]+=1
backgroundModel = np.array(backgroundModel)
backgroundModel = backgroundModel/float(sum(backgroundModel))
import pdb;pdb.set_trace()
ptb_word_id_dict = ptb_dict
ptb_id_word_dict = dict((v, k) for k, v in ptb_word_id_dict.items())
# Kneser-Ney smoothing
# print([ptb_id_word_dict[i] for i in train[:30]])