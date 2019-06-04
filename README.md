
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
$$ KL\left(Q||D\right)=\sum _{w\in V}\frac {f_{w\cdot Q}}{\left| Q\right| }\log P\left( w| D\right) $$
$Q$ is query, $D$ is document, $w$ is word, $V$ is all of the vocabulary, $f_{w\cdot Q}$ is frequency of the word $w$ in query $Q$

<img src="http://latex.codecogs.com/gif.latex?\\ {KL(Q||D)}=\sum _{w\in V} \frac {1}{Q}" />
<img src="http://latex.codecogs.com/gif.latex?\\ \sum_{k=1}^{n}\frac{1}{k}" />


### IR_qustion2qustion.py
We use the subject of "NABU FAQ for Worry Free Product 20190401.csv" as query, and the subject of "WF Cases 20190517.csv" as document. At the beginning of the code is LM generation, and then calculate the KL score between document LM and query LM. Finally, rank and select top N relevant subject to output<br> 


---
