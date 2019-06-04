
# Question Answering
<i><b>information retrieval</b></i>

---

## Data set
document set: WF Cases 20190517.csv<br>
query set:    NABU FAQ for Worry Free Product 20190401.csv

---

## Preprocessing
### email_preprocess.py
Extract the main of email and remove garbage information.<br>
Finally output is a cPickle file.
### create_dictionary.py
Use the output file of email_preprocess.py to create dictionary.
### word2id.py
Use dictionary to transfer the word of email to word ID.

---

## Method
### Unigram Language Model
<i>Q:What is unigram language model?<br>
A:probability distribution over the words in a language.<br></i>

We use document and query to generate document language model and query language model, and then calculate KL-Divergence score to rank the relevant document.
<img src="http://latex.codecogs.com/gif.latex?\\ {KL(Q||D)}=\sum_{w\in{V}}\frac{f_{w,Q}}{|Q|}\log{P(w|D)}" />

<img src="http://latex.codecogs.com/gif.latex?\\ Q" /> is query, <img src="http://latex.codecogs.com/gif.latex?\\ D" /> is document, <img src="http://latex.codecogs.com/gif.latex?\\ w" /> is word, <img src="http://latex.codecogs.com/gif.latex?\\ V" /> is all of the vocabulary, <img src="http://latex.codecogs.com/gif.latex?\\ f_{w,Q}" /> is frequency of the word <img src="http://latex.codecogs.com/gif.latex?\\ w" /> in query <img src="http://latex.codecogs.com/gif.latex?\\ Q" />


### IR_qustion2qustion.py
We use the subject of "NABU FAQ for Worry Free Product 20190401.csv" as query, and the subject of "WF Cases 20190517.csv" as document. At the beginning of the code is LM generation, and then calculate the KL score between document LM and query LM. Finally, rank and select top N relevant subject to output<br> 


---
