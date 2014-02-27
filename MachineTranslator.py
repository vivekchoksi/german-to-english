import sys
import nltk
import pattern.de
import re
dictionary = eval(open('dictionary.txt').read())
brown_bigrams = eval(open('bigram_counts.txt').read())
brown_trigrams = eval(open('trigram_counts.txt').read())

class MachineTranslator:

  class PreProcessor:

    # List of words of form "have" or "was/is". (static class variable)
    PERFECT_VERB_FORMS = pattern.de.lexeme('haben') + pattern.de.lexeme('werden') + pattern.de.lexeme('sein') + pattern.de.lexeme('muss')

    # List of reflexive words that can be omitted. (static class variable)
    REFLEXIVE_WORDS = ['sich', 'dich', 'euch', 'uns', 'mich', 'mir', 'dir']

    # Regex pattern to distinguish word tokens from punctuation
    WORD_PATTERN = re.compile(r'\w+')

    # List of german conjunctions
    GERMAN_CONJUNCTIONS = set(open('german_conjunctions.txt').read().split('\n'))

    def __init__(self, infile):
      self.infile = infile


    def pre_process(self):
      '''Reads a raw German corpus and returns a pre-processed German corpus.'''
      result = []
      with open(self.infile) as f:
        for sentence in f:
          sentence_tokens = nltk.word_tokenize(sentence)
          pos_map = self._POS_map(sentence)
          clauses = self._clausify(sentence_tokens, pos_map)
          self._pre_process_sentence(clauses, pos_map)    
          result.append(self._declausify(clauses))
      return result

    def _pre_process_sentence(self, clauses, pos_map):
      if len(clauses) == 0: return
      self._reorder_verb_subject_in_second_position(clauses, pos_map)
      self._change_perfect_verb_order(clauses, pos_map)
      self._reorder_adjective_phrases(clauses, pos_map)
      self._delete_reflexive_words(clauses, pos_map)

    def _POS_map(self, sentence):
      result = {}
      tagged_words = pattern.de.parse(sentence)

      # Tag word based on sentence context
      for tagged_word in tagged_words.split(' '):
        tag_index = tagged_word.find('/')
        word = tagged_word[:tag_index]
        tag = tagged_word[tag_index:]
        result[word] = tag

      # For missing tags, tag directly
      for word in nltk.word_tokenize(sentence):
        if word not in result:
          result[word] = pattern.de.parse(word)

      return result


    def _clausify(self, sentence_tokens, pos_map):

      result = []
      last = 0
      for i, word in enumerate(sentence_tokens):
        is_prev_comma = i>0 and sentence_tokens[i-1] == ','

        is_conjuction = (word in self.GERMAN_CONJUNCTIONS) or ('WDT' in pos_map[word])
        if (word in (':', ';')) or (is_conjuction and is_prev_comma):
          result.append(sentence_tokens[last:i])
          result.append(sentence_tokens[i:i+1])
          last = i+1
      result.append(sentence_tokens[last:len(sentence_tokens)])

      return result

    def _declausify(self, clauses):
      return [word for clause in clauses for word in clause]

    # NOTE method under construction... (Chris)
    def _reorder_verb_subject_in_second_position(self, clauses, pos_map):
      # when some form of time is in the beginning of the sentence: "heute habe ich meine Hausaufgaben gemacht" -> "I did my homework today"
      if self._declausify(clauses)[-1] == '?':
        return
      for clause_tokens in clauses:
        for i in range(1, len(clause_tokens)):
          if self._is_verb(clause_tokens[i], pos_map):
            if self._is_pronoun(clause_tokens[i-1], pos_map): 
              break
            if self._is_noun(clause_tokens[i-1], pos_map):
              if self._is_pronoun(clause_tokens[i+1], pos_map): 
                verb = clause_tokens[i]
                pronoun = clause_tokens[i+1]
                del clause_tokens[i+1]
                del clause_tokens[i]
                clause_tokens.insert(0, pronoun)
                clause_tokens.insert(1, verb)
                break
            else:
              for j in range(i+1, len(clause_tokens)):
                if self._is_noun(clause_tokens[j], pos_map) or self._is_pronoun(clause_tokens[j], pos_map):
                  verb = clause_tokens[i]
                  del clause_tokens[i]
                  clause_tokens.insert(j, verb)
                  break
      # print clauses

    def _reorder_adjective_phrases(self, clauses, pos_map):
      for clause in clauses:
        clause_string = " ".join(clause)
        # print clause_string
        tree = pattern.de.parsetree(clause_string)
        for index, chunk in enumerate(tree[0].chunks):
          if "ADJP" in chunk.type:
            # print chunk
            index = 0
            for i, word in enumerate(clause):
              if word in chunk.words[0].string:
                index = i 
                for i in range(0, len(chunk.words)):
                  del clause[index]
                break
            for i in range(0, index):
              if self._is_verb(clause[i], pos_map):
                # print clause[1]
                for word in reversed(chunk.words):
                  clause.insert(i, word.string)
                break

    def _delete_reflexive_words(self, clauses, pos_map):
      ''' Delete unnecessary reflexive words '''
      for sentence_tokens in clauses:
        for word_index, word in enumerate(sentence_tokens):
          if word in self.REFLEXIVE_WORDS:
            del sentence_tokens[word_index]


    def _change_perfect_verb_order(self, clauses, pos_map):
      ''' Identify German sentences of the form 'The city was in 1170 taken.' and move
          the perfect verb to the correct place in the sentence. '''

      # Don't change verb order if the sentence is a question
      if self._declausify(clauses)[-1] == '?':
        return

      for sentence_tokens in clauses:
        for i, word1 in enumerate(sentence_tokens):
          if word1 in self.PERFECT_VERB_FORMS:
            for j, word2 in enumerate(sentence_tokens[i+1:]):
              j += i+1
              if self._is_verb(word2, pos_map):              
                del sentence_tokens[j]
                sentence_tokens.insert(i + 1, word2)


    def _get_last_word_index(self, sentence_tokens):
      ''' Get the index of the last word in the list of sentence tokens. '''
      for i in reversed(range(0, len(sentence_tokens))):
        if self.WORD_PATTERN.findall(sentence_tokens[i]):
          return i
      return False

    def _is_verb(self, word, pos_map):
      return (dictionary[word.lower()].get('part_of_speech', None) == 'verb') or ('VB' in pos_map[word])

    def _is_noun(self, word, pos_map):
      return (dictionary[word.lower()].get('part_of_speech', None) == 'noun') or ('NN' in pos_map[word])

    def _is_pronoun(self, word, pos_map):
      return (dictionary[word.lower()].get('part_of_speech', None) == 'pronoun') or ('PRP' in pos_map[word])

  class PostProcessor:

    ARTICLES_TO_PRUNE = ["the"]

    ARTICLES_FOLLOWING_OF = ["the", "this"]

    def __init__(self, tokenized_translations):
      ''' This initialization will be slow because it processes the large
          nltk Brown corpus '''
      self.language_model = [word.lower() for word in nltk.corpus.brown.words()]
      self.bigram_counts = brown_bigrams
      self.trigram_counts = brown_trigrams
      # self._get_bigram_counts()

      # Enforce that all tokens only contain 1 word
      for index, sentence in enumerate(tokenized_translations):
        stringed = " ".join(tokenized_translations[index])
        tokenized_translations[index] = nltk.word_tokenize(stringed)
      self.tokenized_translations = tokenized_translations

    def post_process(self):
      '''Takes in a translated, tokenized English corpus and returns a post-processed, tokenized English corpus.'''
      for tokenized_sentence in self.tokenized_translations:
        self._remove_extra_articles(tokenized_sentence)
        self._add_missing_of(tokenized_sentence)
        tokenized_sentence[0] = tokenized_sentence[0].capitalize()
      return self.tokenized_translations

    def _remove_extra_articles(self, tokenized_sentence):
      ''' Remove extra instances of the word "the" '''
      # TODO: if 'the' is deleted twice, make sure there is no index out of bounds error
      for i in range(1, len(tokenized_sentence) - 1):
        if tokenized_sentence[i] in self.ARTICLES_TO_PRUNE:
          raw_bigram = tokenized_sentence[i].lower() + " " + tokenized_sentence[i + 1].lower()
          pruned_bigram = tokenized_sentence[i - 1].lower() + " " + tokenized_sentence[i + 1].lower()

          # If the new form (i.e. without 'and') is significantly more probable, then change the translation
          if pruned_bigram in self.bigram_counts:
            if raw_bigram not in self.bigram_counts:
              del tokenized_sentence[i]
            elif float(self.bigram_counts[pruned_bigram]) / float(self.bigram_counts[raw_bigram]) > 2: # TODO: tune this
              del tokenized_sentence[i]

    def _add_missing_of(self, tokenized_sentence):
      ''' Add the word 'of' before certain articles if it's missing.
          Affects dev sentences 6 and 9. '''
      for i in range(1, len(tokenized_sentence)):
        if tokenized_sentence[i] in self.ARTICLES_FOLLOWING_OF:
          raw_bigram = tokenized_sentence[i - 1].lower() + " " + tokenized_sentence[i].lower()
          new_trigram = tokenized_sentence[i - 1].lower() + " of " + tokenized_sentence[i].lower()

          # If the new form (i.e. with 'of') is significantly more probable, then change the translation
          if new_trigram in self.trigram_counts:
            if raw_bigram not in self.bigram_counts:
              tokenized_sentence.insert(i, 'of')
            elif float(self.trigram_counts[new_trigram]) / float(self.bigram_counts[raw_bigram]) > 2: # TODO: tune this
              tokenized_sentence.insert(i, 'of')

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
    print 'MachineTranslator.py: expects 1 or 2 arguments...'
    print '\tTo write translations to file:    python MachineTranslator.py <corpus-to-translate> <translation-outfile>'
    print '\tTo print translations to console: python MachineTranslator.py <corpus-to-translate>'
    sys.exit()

  infile = sys.argv[1]
  outfile = sys.argv[2] if len(sys.argv) == 3 else ""
  mt = MachineTranslator(infile, outfile)
  mt.translate()


if __name__ == "__main__":
  main()
