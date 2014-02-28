import sys
from translator import Translator
from translate import Translator as WordTranslator
import nltk
import codecs
from pprint import pformat
from collections import defaultdict

translator = Translator(from_lang='de', to_lang='en') #gets multiple translations
word_translator = WordTranslator(from_lang='de', to_lang='en') #gets one translation



'''This outputs all translated words into dictionary.txt. To load:
		dictionary = eval(open('dictionary.txt').read())

		All words have dictionary[word]['box_translation'] = box translation
		Some words have dictionary[word]['part_of_speech'] = str part of speech
		and				dictionary[word]['alt_translations'] = list of alternate translations
'''
def main(dev_filename, test_filename):
	words = []
	with codecs.open(dev_filename, 'r') as f:
		for line in f:
			words.extend(nltk.word_tokenize(line))
	
	with codecs.open(test_filename, 'r') as f:
		for line in f:
			words.extend(nltk.word_tokenize(line))

	words = set(words)
	dictionary = defaultdict(dict)

	for word in words:
		dictionary[word.lower()]['box_translation'] = word_translator.translate(word)
		try:
			part_of_speech, english_translations = translator.translate(word)
			dictionary[word.lower()]['part_of_speech'] = part_of_speech
			dictionary[word.lower()]['alt_translations'] = english_translations
		except Exception, e:
			pass

	dictionary = dict(dictionary) # so it prints properly
	with codecs.open('dictionary.txt', 'w', encoding='utf-8') as f:
		f.write(pformat(dictionary))


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: python generate_dict.py dev.txt test.txt')
		sys.exit(1)
	main(sys.argv[1], sys.argv[2])