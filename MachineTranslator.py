import sys
import nltk

dictionary = eval(open('dictionary.txt').read())

class MachineTranslator:
  def __init__(self, filename):
    self.filename = filename
    self.tokenized_sentences = extract_tokenized_sentences(filename)    
    self.tokenized_translations = direct_translate(self.tokenized_sentences)
    import pdb; pdb.set_trace()
  
  def direct_translate(self, tokenized_sentences):
    '''Translates a list of tokenized german sentences word-by-word'''
    result = []
    for sentence in tokenized_sentences:
      translation = [dictionary[word]['translations'][0] for word in tokenized_sentence]
      result.append(translation)
    return result

  def extract_tokenized_sentences(self, filename):
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
  if len(sys.argv) != 2:
    print 'MachineTranslator.py: expects 1 argument...'
    print '\tUsage: python MachineTranslator.py <corpus-to-translate>'
    sys.exit()

  filename = sys.argv[1]
  mt = MachineTranslator(filename)
  pass

if __name__ == "__main__":
  main()
