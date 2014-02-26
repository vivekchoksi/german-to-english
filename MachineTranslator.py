import sys
import nltk
import pattern.de
dictionary = eval(open('dictionary.txt').read())

class MachineTranslator:


  class PreProcessor:

    # List of words of form "have" or "was/is". (static class variable)
    perfect_verb_forms = pattern.de.lexeme('haben') + pattern.de.lexeme('werden')

    def __init__(self, infile):
      self.infile = infile


    def pre_process(self):
      '''Reads a raw German corpus and returns a pre-processed German corpus.'''
      result = []
      with open(self.infile) as f:
        for sentence in f:
          sentence_tokens = nltk.word_tokenize(sentence)
          self._pre_process_sentence(sentence_tokens)
          #tagged_sentence = pattern.de.parse(sentence)
          #tagged_sentence_tokens = nltk.word_tokenize(tagged_sentence)
          # TODO: something with the tagged_sentence_tokens
          result.append(sentence_tokens)
      return result

    def _pre_process_sentence(self, sentence_tokens):
      if len(sentence_tokens) == 0:
        return
      self._change_perfect_verb_order(sentence_tokens)

    # NOTE: method under construction...
    # TODO: Need to find reliable way of identifying perfect verb at end of sentence
    # TODO: Need to more elegantly get the last word in a sentence
    # TODO: Create a list of reflexive words like 'sich'
    def _change_perfect_verb_order(self, sentence_tokens):
      ''' Identify German sentences of the form 'The city was in 1170 taken.' and move
          the perfect verb to the correct place in the sentence. '''
      last_token = sentence_tokens[-2] # get last non-punctuation word. TODO: make robust
      last_parsed = pattern.de.parse(last_token)
      #if 'VB/B-VP' in last_parsed:
      if (('part_of_speech' in dictionary[last_token.lower()].keys() and
              dictionary[last_token.lower()]['part_of_speech'] == 'verb') or
              'VB/B-VP' in last_parsed):
        # Sentence ends with verb
        for i in reversed(range(0, len(sentence_tokens) - 1)):
          if sentence_tokens[i] in self.perfect_verb_forms:
            # Delete the word 'sich' in this case (meaning 'itself')
            if sentence_tokens[i + 1] == 'sich':
              del sentence_tokens[i + 1]
            # Insert the perfect verb after the 'have/was'-form verb.
            sentence_tokens.insert(i + 1, last_token)
            del sentence_tokens[-2]

  class PostProcessor:
    def __init__(self, tokenized_translations):
      self.tokenized_translations = tokenized_translations

    def post_process(self):
      '''Takes in a translated, tokenized English corpus and returns a post-processed, tokenized English corpus.'''
      return self.tokenized_translations


  def __init__(self, infile, outfile):
    self.infile = infile
    self.outfile = outfile

  def translate(self):
    pre = self.PreProcessor(self.infile)
    pre_processed = pre.pre_process()
    tokenized_translations = self._direct_translate(pre_processed)

    post = self.PostProcessor(tokenized_translations)
    post_processed = post.post_process()
    self._save_translations(post_processed, self.outfile)

  def _save_translations(self, tokenized_translations, outfile=""):
    '''If outfile is specified, save our translations to outfile;
       else, print translations to console.'''
    if outfile:
      with open(outfile, 'w') as f:
        for sentence in tokenized_translations:
          f.write(' '.join(sentence))
          f.write('\n')
    else:
      for sentence in tokenized_translations:
        print ' '.join(sentence)

  
  def _direct_translate(self, tokenized_sentences):
    '''Translates a list of tokenized german sentences word by word'''
    result = []
    for sentence in tokenized_sentences:
      translation = [dictionary[word.lower()]['box_translation'] for word in sentence]
      result.append(translation)
    return result

  def _extract_tokenized_sentences(self, infile):
    '''Extracts a list of tokenized sentences from a file'''
    result = []
    with open(infile) as f:
      for sentence in f:
        sentence_tokens = nltk.word_tokenize(sentence)
        tagged_sentence = pattern.de.parse(sentence)
        tagged_sentence_tokens = nltk.word_tokenize(tagged_sentence)
        # TODO: something with the tagged_sentence_tokens
        result.append(sentence_tokens)
    return result




def main():
  if len(sys.argv) != 2 and len(sys.argv) != 3:
    print 'MachineTranslator.py: expects 2 or 3 arguments...'
    print '\tTo write translations to file:    python MachineTranslator.py <corpus-to-translate> <translation-outfile>'
    print '\tTo print translations to console: python MachineTranslator.py <corpus-to-translate>'
    sys.exit()

  infile = sys.argv[1]
  outfile = sys.argv[2] if len(sys.argv) == 3 else ""
  mt = MachineTranslator(infile, outfile)
  mt.translate()


if __name__ == "__main__":
  main()
