import sys
import nltk

dictionary = eval(open('dictionary.txt').read())

class MachineTranslator:
  def __init__(self, filename):
    self.filename = filename
  
  def translate(self, outfile):
    self.tokenized_sentences = self._extract_tokenized_sentences(self.filename)    
    self.tokenized_translations = self._direct_translate(self.tokenized_sentences)
    self._save_translations(self.tokenized_translations, outfile)

  def _save_translations(self, tokenized_translations, outfile):
    '''Saves our translations to outfile'''
    with open(outfile, 'w') as f:
      for sentence in tokenized_translations:
        f.write(' '.join(sentence))
        f.write('\n')

  
  def _direct_translate(self, tokenized_sentences):
    '''Translates a list of tokenized german sentences word-by-word'''
    result = []
    for sentence in tokenized_sentences:
      translation = [dictionary[word.lower()]['box_translation'] for word in sentence]
      result.append(translation)
    return result

  def _extract_tokenized_sentences(self, filename):
    '''Extracts a list of tokenized sentences from a file'''
    result = []
    with open(filename) as f:
      for sentence in f:
        sentence_tokens = nltk.word_tokenize(sentence)
        result.append(sentence_tokens)
    return result


  class PreProcessor:
    def __init__(self):
      pass

    def pre_process(self, sentence):
      """Takes in a raw German sentence and returns a pre-processed German sentence."""
      pass

  class PostProcessor:
    def __init__(self):
      pass

    def post_process(self, sentence):
      """Takes in an English sentence and returns a post-processed English sentence."""
      pass



def main():
  if len(sys.argv) != 3:
    print 'MachineTranslator.py: expects 2 argument...'
    print '\tUsage: python MachineTranslator.py <corpus-to-translate> <translation-outfile>'
    sys.exit()

  filename = sys.argv[1]
  outfile = sys.argv[2]
  mt = MachineTranslator(filename)
  mt.translate(outfile)
  pass

if __name__ == "__main__":
  main()
