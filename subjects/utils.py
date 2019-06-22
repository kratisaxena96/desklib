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
	# text = get_text('files/2666673_1936048055_americanhistory.811822.docx')
	# text = get_text(file_loc)

	text = get_clean_text(text).lower()
	

	# words = get_words_from_text(text)
	# https://radimrehurek.com/gensim/summarization/keywords.html
	# print(keywords(text).split('\n'))
	words_collection = {}
	text = strip_punctuation(text)
	text = stem_text(text)
	# https://stackoverflow.com/questions/32441605/generating-ngrams-unigrams-bigrams-etc-from-a-large-corpus-of-txt-files-and-t
	tokens = word_tokenize(text)
	tokens = remove_stop_words(tokens)
	ugs = ngrams(tokens, 1)
	bgs = bigrams(tokens)
	tgs = trigrams(tokens)
	words_collection = {}
	fdist_ugs = FreqDist(ugs)
	
	fdist_bgs = FreqDist(bgs)
	fdist_tgs = FreqDist(tgs)

	words_collection.update(fdist_ugs.items())
	words_collection.update(fdist_bgs.items())
	words_collection.update(fdist_tgs.items())

	# print(words_collection)

	subjects_data_modified = {}
	subjects_score = {}
	subjects_factor = {}

	subject_qs = Subject.objects.filter(is_visible=True)
	for subject in subject_qs:
		subject_name = subject.name
		slug = subject.slug
		# subjects_score[slug] = 0
		keywords = subject.keywords.names()
		# print("subject={}\nslug={}\nkeywords={}".format(subject, slug, keywords))
		keyword_tuple = ()
		subjects_factor[slug] = 1

		for keyword in keywords:
			keyword = strip_punctuation(keyword)
			keyword = stem_text(keyword)
			tokens = word_tokenize(keyword)
			tokens = remove_stop_words(tokens)
			keyword_tuple = tuple(tokens)

			if keyword_tuple in words_collection:
				# print('##Keyword Matched: ', keyword_tuple)
				if subjects_score.get(slug):
					subjects_factor[slug] += 0.5
					subjects_score[slug] += words_collection[keyword_tuple]*len(keyword_tuple)*len(keyword_tuple)*subjects_factor[slug]
				else:
					subjects_score[slug] = words_collection[keyword_tuple]*len(keyword_tuple)*len(keyword_tuple)
					


	# print(subjects_score)
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

	if not predicted_subjects:
		predicted_subjects['uncategorized'] = 0

	return Subject.objects.filter(is_visible=True, slug__in=predicted_subjects.keys())
	# return predicted_subjects


# import os
# import random
#
# path ='files'
# files = os.listdir(path)
# index = random.randrange(0, len(files))
# print(files[index])
#
# file_loc = os.path.join('files', files[index])
# # file_loc = 'files/2669342_1070405960_2665540496057639FinancialAccou.docx'
# # file_loc = 'files/2670386_663385549_HigherEducationandHealthPromot.docx'
# # file_loc = 'files/2672096_982360195_2016MGMT310-Assignment1doc3-Jo.doc'
# # file_loc = 'files/2671825_1105177032_26699781230768885articlereview.docx'
# # file_loc = 'files/2675673_390392621_ASSIGNMENTONSOILMECHANIC.docx'
#
#
# # file_loc = 'files/2678457_1916787519_Multipleregressions2.docx'
#
# # file_loc = 'files/BZ-NR-MITS4402_Assignment_2018_25%.docx'
# # file_loc = 'files/2698806_1286029317_5cd98742-e31c-4eac-9539-01b1b7.jpg'
#
# # file_loc = 'files/2674212_1224967721_ITC556Week-9SQLPracticalsUsing.pdf'
#
#
# print(get_subject(file_loc))
#



# https://towardsdatascience.com/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a
# https://towardsdatascience.com/multi-class-text-classification-model-comparison-and-selection-5eb066197568
# https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925
# https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f
