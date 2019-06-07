import textract
import os
import nltk.data
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

FILES_DIR = 'files'
files_list = os.listdir(FILES_DIR)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-zA-Z .#+_]')
STOPWORDS = set(stopwords.words('english'))
ALLOWED_FORMATS = ['.doc', '.docx', '.pdf', '.ppt', '.pptx', '.odt'] # + ['.png', '.jpg', '.jpeg']
# ALLOWED_FORMATS = ['.doc']
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata/'


def get_text(loc):
    try:
        return textract.process(loc).decode("utf-8")
    except textract.exceptions.ExtensionNotSupported as e:
        print(e)
        return ''

def get_text_from_file():
    pass