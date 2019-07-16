import textract
import os
import nltk.data
from django.utils.text import slugify
from rake_nltk import Rake
import re
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import random
import string


# FILES_DIR = 'files'
# files_list = os.listdir(FILES_DIR)


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-zA-Z .#+_]')
STOPWORDS = set(stopwords.words('english'))
ALLOWED_FORMATS = ['.doc', '.docx', '.pdf', '.ppt', '.pptx', '.odt']  # + ['.png', '.jpg', '.jpeg']
# ALLOWED_FORMATS = ['.doc']
os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata/'

def key_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_text(loc):
    try:
        return textract.process(loc).decode("utf-8")
    except textract.exceptions.ExtensionNotSupported as e:
        print(e)
        return ''


# def separate_words(text, min_word_return_size):
#     """
#     Utility function to return a list of all words that are have a length greater than a specified number of characters.
#     @param text The text that must be split in to words.
#     @param min_word_return_size The minimum no of characters a word must have to be included.
#     """
#     splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
#     words = []
#     for single_word in splitter.split(text):
#         current_word = single_word.strip().lower()
#         # leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
#         if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
#             words.append(current_word)
#     return words


def is_format_allowed(filename):
    return filename.lower().endswith(tuple(ALLOWED_FORMATS))


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def get_sentences_from_text(text):
    # return tokenizer.tokenize('. '.join(text.splitlines()))
    return sent_tokenize(text)


def get_summary(sentences):
    return sentences[0:5]


def get_length(sentences):
    return len(sentences)


def get_keywords_from_text(text, count=10):
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the text.
    r.extract_keywords_from_text(text)

    # To get keyword phrases ranked highest to lowest.
    # print(r.get_ranked_phrases())

    # To get keyword phrases ranked highest to lowest with scores.
    # print(r.get_ranked_phrases_with_scores())

    return r.get_ranked_phrases()[:count]


def get_keywords_from_sentences(sentences, count=10):
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()

    # Extraction given the list of strings where each string is a sentence.
    r.extract_keywords_from_sentences(sentences)

    # To get keyword phrases ranked highest to lowest.
    # print(r.get_ranked_phrases())

    # To get keyword phrases ranked highest to lowest with scores.
    # print(r.get_ranked_phrases_with_scores())

    return r.get_ranked_phrases()[:count]


def get_words_from_text(text):
    tokens = word_tokenize(text)
    return tokens


def is_redundant_text(text):
    return 'ORIGINALITY REPORT' in text


def get_clean_text(text):
    """
        text: a string

        return: modified initial string
    """
    text = BeautifulSoup(text, "lxml").text  # HTML decoding
    # text = text.lower() # lowercase text
    text = text.replace('\n', ' ').replace('\r', '')
    text = REPLACE_BY_SPACE_RE.sub(' ', text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)  # delete stopwors from text
    return text


def get_first_sentence(sentences):
    if sentences:
        return sentences[0]

    return ''


def get_title(text):
    # Get extension
    # https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    # filename, file_extension = os.path.splitext(filename)
    # if file_extension == '.docx':
    # 	text = text.replace('\n', ' ').replace('\r', '')
    # 	# text = text.replace('Running Head', '')
    # 	insensitive = re.compile(re.escape('Running Head'), re.IGNORECASE)
    # 	text = insensitive.sub('', text)
    # 	text = re.sub(r'\s{2,}', ". ", text.strip())
    # 	sentences = get_sentences_from_text(text)
    # 	first_sentence =  get_first_sentence(sentences)
    # 	if len(first_sentence) > 55:
    # 		return first_sentence[:55] + '...'
    # 	else:
    # 		return first_sentence

    # elif file_extension == '.doc':
    text = text.replace('\n', ' ').replace('\r', '')
    text = text.replace('Running Head', '')
    # https://stackoverflow.com/questions/919056/case-insensitive-replace
    insensitive = re.compile(re.escape('Running Head'), re.IGNORECASE)
    text = insensitive.sub('', text)
    text = re.sub(r'\s{2,}', ". ", text.strip())
    # print(text)
    sentences = get_sentences_from_text(text)
    first_sentence = get_first_sentence(sentences)
    if len(first_sentence) > 65:
        # https://stackoverflow.com/questions/6266727/python-cut-off-the-last-word-of-a-sentence
        return first_sentence[:65].rsplit(' ', 1)[0] + '...'
    elif len(first_sentence) < 15:
        return text[:55] + '...'
    else:
        return first_sentence


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)

    return new_words


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.conf import settings

def get_html_from_pdf_url(url):
    """
    This function returns html of given pdf url. We use converted html from pdf.js library which is used by mozilla
    firefox to render pdf. A headless mozilla browser with selenium is used to render pdf and extract html.

    :param url: A browser friendly url.
    :return: A dictionary with page numbers as keys and page as values.
    """
    data = {}
    options = webdriver.FirefoxOptions()
    # We need a headless firefox browser
    options.headless = True
    geckodriver = settings.GECKO_DRIVER_URL

    # print(geckodriver)
    driver = webdriver.Firefox(executable_path=geckodriver, options=options)
    # url = 'file:///home/siddharth/Downloads/itc-brands-brochure.pdf'
    # url = 'http://www.pdf995.com/samples/pdf.pdf'
    driver.get(url)
    try:
        # Waiting for page to be rendered
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "page"))
        )

        # Getting total pages in pdf
        numpages = driver.execute_script("return PDFViewerApplication.pdfViewer.pagesCount")

        # looping through pages and extracting html
        for i in range(1, numpages + 1):
            # Going through each page
            driver.execute_script("PDFViewerApplication.page = " + str(i))

            # try:
            #     xpath_loading = "//div[@class='page' and @data-page-number='" + str(i) + "']//div[@class='loadingIcon']"
            #     WebDriverWait(driver, 10).until(
            #         EC.presence_of_element_located((By.XPATH, xpath_loading))
            #     )
            # except:
            #     pass

            # xpath_loading = "//*[@id='viewer']//div[@class='page' and @data-page-number='" + str(i) + "']//div[@class='loadingIcon']"
            # WebDriverWait(driver, 10).until_not(
            #     EC.presence_of_element_located((By.XPATH, xpath_loading))
            # )

            # Waiting till content of the page is rendered in DOM
            xpath = "//*[@id='viewer']//div[@class='page' and @data-page-number='" + str(i) + "' and @data-loaded='true']//div[@class='endOfContent']"
            # xpath = "/html/body/div[1]/div[2]/div[4]/div/div[" + str(i) + "]/div[2]/*[@class='endOfContent']"
            print(xpath)
            # css_selector = 'div.endOfContent'
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

            # Removing canvas from rendered html
            canvas_xpath = "//*[@id='viewer']//div[@class='page' and @data-page-number='" + str(i) + "' and @data-loaded='true']//div[@class='canvasWrapper']"
            element = driver.find_element_by_xpath(canvas_xpath)
            driver.execute_script("""
            var element = arguments[0];
            element.parentNode.removeChild(element);
            """, element)

            # Extracting html data for particular page
            element_xpath = "//*[@id='viewer']//div[@class='page' and @data-page-number='" + str(i) + "' and @data-loaded='true']"
            element = driver.find_element_by_xpath(element_xpath);
            html = element.get_attribute('outerHTML')
            # adding data to our dictionary
            data[i] = html

    finally:
        driver.quit()

    return data


def get_filename_from_path(path):
    return os.path.basename(path)

def get_directory_path_from_path(path):
    return os.path.dirname(path)

# https://www.codingforentrepreneurs.com/blog/a-unique-slug-generator-for-django/
def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug