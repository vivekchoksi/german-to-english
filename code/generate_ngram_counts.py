
import nltk
import sys
from collections import Counter

def generate_counts(outfile, n):
  language_model = [word.lower() for word in nltk.corpus.brown.words()]
  if n == 2:
    lowercase_model = nltk.bigrams(language_model)
  elif n == 3:
    lowercase_model = nltk.trigrams(language_model)
  else:
    print 'generate_ngram_counts.py: only supports bigrams and trigrams.'
  ngram_list = [" ".join(gram) for gram in lowercase_model]
  ngram_counts = Counter(ngram_list)
  with open(outfile, 'a') as f:
    f.write(repr(ngram_counts))


def main():
  if len(sys.argv) != 3:
    print 'generate_ngram_counts.py: expects 2 arguments...'
    print '\tpython generate_ngram_counts.py <n> <outfile-name>'
    sys.exit()

  n = int(sys.argv[1])
  outfile = sys.argv[2]

  generate_counts(outfile, n)


if __name__ == "__main__":
  main()
