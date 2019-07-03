import json
from documents.utils import get_text, get_clean_text, to_lowercase

from gensim.summarization import keywords
from gensim.parsing.preprocessing import strip_punctuation
from nltk import word_tokenize, bigrams, trigrams, FreqDist
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from nltk.util import ngrams

from subjects.models import Subject

SCORE_THRESHOLD = 4

def stem_text(text):
	porter = PorterStemmer()
	token_words=word_tokenize(text)
	stem_sentence=[]
	for word in token_words:
		stem_sentence.append(porter.stem(word))
		stem_sentence.append(" ")

	return "".join(stem_sentence)

def lemmatize_text(text):
	lemmatizer = WordNetLemmatizer()
	token_words=word_tokenize(text)
	lemmatize_sentence=[]
	for word in token_words:
		lemmatize_sentence.append(lemmatizer.lemmatize(word))
		lemmatize_sentence.append(" ")

	return "".join(lemmatize_sentence)


def remove_stop_words(words):
	stopWords = set(stopwords.words('english'))
	wordsFiltered = []
	for w in words:
		if w not in stopWords:
			wordsFiltered.append(w)

	return wordsFiltered


def get_subjects(text):
	"""
	Logic to predict subject from text contents
	:param text: Text to be processed
	:return: QuerySet of predicted subjects
	"""
	# Preprocessing text data
	# - Removing spaces, bad symbols abd converting to lower cases
	# - Removing punctuations
	text = get_clean_text(text).lower()
	

	# words = get_words_from_text(text)
	# https://radimrehurek.com/gensim/summarization/keywords.html
	# print(keywords(text).split('\n'))
	words_collection = {}
	text = strip_punctuation(text)
	# Stemming text
	text = stem_text(text)

	# Tokenizing text
	# https://stackoverflow.com/questions/32441605/generating-ngrams-unigrams-bigrams-etc-from-a-large-corpus-of-txt-files-and-t
	tokens = word_tokenize(text)
	# Removing stop words
	tokens = remove_stop_words(tokens)

	# Generating uni, bi and trigrams
	ugs = ngrams(tokens, 1)
	bgs = bigrams(tokens)
	tgs = trigrams(tokens)
	# Dictionary to populate frequencies of all uni, bi and trigram words.
	words_collection = {}
	fdist_ugs = FreqDist(ugs)
	fdist_bgs = FreqDist(bgs)
	fdist_tgs = FreqDist(tgs)

	words_collection.update(fdist_ugs.items())
	words_collection.update(fdist_bgs.items())
	words_collection.update(fdist_tgs.items())

	# maintaining scores of each subject
	subjects_score = {}
	subjects_factor = {}

	subject_qs = Subject.objects.filter(is_visible=True)
	# looping through subjects
	for subject in subject_qs:
		slug = subject.slug
		# Getting all keywords related to particular subject
		keywords = subject.keywords.names()
		subjects_factor[slug] = 1
		# looping through each keyword
		for keyword in keywords:
			# Preprocessing: cleaning, stemming, tokenizing and removing stop words
			keyword = strip_punctuation(keyword)
			keyword = stem_text(keyword)
			tokens = word_tokenize(keyword)
			tokens = remove_stop_words(tokens)
			keyword_tuple = tuple(tokens)

			# Checking if keyword occurs in our document
			if keyword_tuple in words_collection:
				# print('##Keyword Matched: ', keyword_tuple)
				# Calculating score and normalizing
				if subjects_score.get(slug):
					subjects_factor[slug] += 0.5
					subjects_score[slug] += words_collection[keyword_tuple]*len(keyword_tuple)*len(keyword_tuple)*subjects_factor[slug]
				else:
					subjects_score[slug] = words_collection[keyword_tuple]*len(keyword_tuple)*len(keyword_tuple)
					

	# Predicting two subjects with top score. If score difference between two subjects is more than 50%, predicting one.
	predicted_subjects = {}
	predicted_subjects_sorted = sorted(subjects_score, key=subjects_score.get, reverse=True)
	total_predictions = len(predicted_subjects_sorted)
	if total_predictions:
		if total_predictions==1:
			w = predicted_subjects_sorted[0]
			predicted_subjects[w] = subjects_score[w]
		else:
			if subjects_score[predicted_subjects_sorted[0]] > 2*subjects_score[predicted_subjects_sorted[1]]:
				w = predicted_subjects_sorted[0]
				predicted_subjects[w] = subjects_score[w]
			else:		
				for w in predicted_subjects_sorted[:2]:
					if subjects_score[w] >= SCORE_THRESHOLD:
						predicted_subjects[w] = subjects_score[w]
	else:
		predicted_subjects['uncategorized'] = 0
	# If no subject is found, adding it to uncategorized
	if not predicted_subjects:
		predicted_subjects['uncategorized'] = 0

	return Subject.objects.filter(is_visible=True, slug__in=predicted_subjects.keys())
	# return predicted_subjects


# https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
# https://towardsdatascience.com/multi-class-text-classification-model-comparison-and-selection-5eb066197568
# https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925
# https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
