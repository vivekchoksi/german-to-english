german-to-english
=================

Machine translator from German to English, built as a class project for CS124 at Stanford. 

### Reference information

#### Reference for pattern.de
* Get it here: http://www.clips.ua.ac.be/pages/pattern
* Reference on what the POS tags mean: http://www.clips.ua.ac.be/pages/mbsp-tags
* ...

#### Reference for nltk
* To download any nltk resource, go to the Python interpreter and execute `import nltk` and `nltk.download()`
* We can use the Brown corpus (nltk.corpus.brown) as a basis for a language model
* ...


#### Usage
After installing dependencies:
  > python code/MachineTranslator.py corpus/dev-corpus.txt

#### Summary of files
  code
    contains: Machine Translator program, google translate scraper, dictionary generator, and ngram language model generator
  corpus
    contains: training and testing corpora
    sources
      contains: list of sources for each sentence in the corpus
  data
    contains dictionary and other various cached data to help the machine translator
