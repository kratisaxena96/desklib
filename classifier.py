import os
import textract
import pickle
import re

from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestClassifier

path = input("Folder Path: ")
stopWords = set(stopwords.words('english'))
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-zA-Z .#+_]')


def get_text(loc):
    try:
        return textract.process(loc).decode("utf-8")
    except textract.exceptions.ExtensionNotSupported as e:
        print(e)
        return ''


def get_clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text  # HTML decoding
    #     text = text.lower() # lowercase text
    text = text.replace('\n', ' ').replace('\r', '')
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in stopWords)  # delete stopwors from text
    return text


vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
with open('text_classifier.sav', 'rb') as training_model:
    model = pickle.load(training_model)


def predict(corpus):
    A = vectorizer.transform(corpus)
    y_pred2 = model.predict(A)
    return y_pred2
