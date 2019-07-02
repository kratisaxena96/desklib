from nltk.tokenize import word_tokenize
import nltk
import re
import difflib
from nltk.util import ngrams
from difflib import SequenceMatcher
from string import punctuation
from termcolor import colored

THRESHOLD_COUNT = 4

s1 = """The legal system is comprised of criminal and civil courts and specialty courts like bankruptcy and family law court. Each court has its own jurisdiction. Jurisdiction means the types of cases each court is permitted to rule on. Sometimes, only one type of court can hear a particular case. For instance, bankruptcy cases an be ruled on only in bankruptcy court. In other situations, it is possible for more than one court to have jurisdiction. For instance, both a state and federal criminal court could have authority over a criminal case that is illegal under federal and state drug laws that is also an offense on the state level."""
s2 = """The legal system is made up of civil courts, criminal courts and specialty courts such as family law courts and bankruptcy court. Each court has its own jurisdiction, which refers to the cases that the court is allowed to hear. In some instances, a case can only be heard in one type of court. For example, a bankruptcy case must be heard in a bankruptcy court. In other instances, there may be several potential courts with jurisdiction. For example, a federal criminal court and a state criminal court would each have jurisdiction over a crime that is a federal drug offense but that is also an offense on the state level."""

print('Text 1: ', s1)
print('Text 2: ', s2)

n1 = list(ngrams(word_tokenize(s1), 1))
n2 = list(ngrams(word_tokenize(s2), 1))
sequence = SequenceMatcher(None,n1,n2)
matches = sequence.get_matching_blocks()

# https://github.com/python/cpython/blob/master/Lib/difflib.py
# https://medium.com/@nikhiljaiswal_9475/sequencematcher-in-python-6b1e6f3915fc
# https://github.com/JonathanReeve/allusion-detection/blob/master/matching-experiments.ipynb

# TODO: https://stackoverflow.com/questions/21948019/python-untokenize-a-sentence

for m in matches:
	if m.size>=THRESHOLD_COUNT:
		print(colored(" ".join([" ".join(ngram) for ngram in n1[m.a: m.a+m.size]]), 'red'), colored('<< '+ str(m.size)+ ' words' +' >>', 'green'), colored(" ".join([" ".join(ngram) for ngram in n2[m.b: m.b+m.size]]), 'red'))



# https://github.com/v1shwa/document-similarity
# https://github.com/NTMC-Community/awesome-neural-models-for-semantic-match
# https://github.com/orsinium/textdistance
# https://github.com/trembacz/diff-checker


