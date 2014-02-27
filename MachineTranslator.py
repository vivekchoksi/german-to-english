import sys
import nltk
import pattern.de
import re
dictionary = eval(open('dictionary.txt').read())

class MachineTranslator:


  class PreProcessor:

    # List of words of form "have" or "was/is". (static class variable)
    PERFECT_VERB_FORMS = pattern.de.lexeme('haben') + pattern.de.lexeme('werden') + pattern.de.lexeme('sein')

    # List of reflexive words that can be omitted. (static class variable)
    REFLEXIVE_WORDS = ['sich', 'dich', 'euch', 'uns', 'mich', 'mir', 'dir']

    # Regex pattern to distinguish word tokens from punctuation
    WORD_PATTERN = re.compile(r'\w+')

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
    def _change_perfect_verb_order(self, sentence_tokens):
      ''' Identify German sentences of the form 'The city was in 1170 taken.' and move
          the perfect verb to the correct place in the sentence. '''

      # Don't change verb order if the sentence is a question
      if sentence_tokens[-1] == '?':
        return

      last_word_index = self._get_last_word_index(sentence_tokens)
      last_word_token = sentence_tokens[last_word_index]
      last_word_parsed = pattern.de.parse(last_word_token)

      # Check if sentence ends with verb. Is there a better way to do this?
      if (dictionary[last_word_token.lower()].get('part_of_speech', None) == 'verb') or ('VB' in last_word_parsed):
        for i in reversed(range(0, len(sentence_tokens) - 1)):
          # Insert the perfect verb after a 'have/was'-form verb.
          if sentence_tokens[i] in self.PERFECT_VERB_FORMS:
            del sentence_tokens[last_word_index]
            # Delete unnecessary reflexive word
            if sentence_tokens[i + 1] in self.REFLEXIVE_WORDS:
              del sentence_tokens[i + 1]

            sentence_tokens.insert(i + 1, last_word_token)

    def _get_last_word_index(self, sentence_tokens):
      ''' Get the index of the last word in the list of sentence tokens. '''
      for i in reversed(range(0, len(sentence_tokens))):
        if self.WORD_PATTERN.findall(sentence_tokens[i]):
          return i
      return False

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
