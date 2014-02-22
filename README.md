german-to-english
=================

Machine translator from German to English, built as a class project for CS124 at Stanford. 

### Notes from second meeting (2/21/14)

#### Agenda
1. Review 10 training sentences and finalize 6-10 post-processing strategies
2. Get Python toolkit set up on everyone's computer
3. Plan framework for machine translator
4. Divide up work to implement framework

### Notes from first meeting (2/20/14)

1. Decide language which to translate to English
  * German
2. Brainstorm approach
  * What helper tools to use? Locate off-the-shelf tool kits
        - Python NLP tools: http://www.nltk.org/
        - Part-of-speech tagger for German: http://www.clips.ua.ac.be/pages/pattern-de
  * What post-processing strategies to implement? (we need 6-10)
        - Info on German verb tense and order: http://esl.fis.edu/grammar/langdiff/german.htm
        - Other info on German vs English grammars: http://www.slideshare.net/LauriRintelman/a-comparison-of-german-and-english-12296261
        - Verb order (verb precedes subject in questions)
        - Verb order (sometimes verb goes at end of sentence)
            - My understanding is that if we find the case in German, then it's easier to reconstruct word order in English (?)
        - Verb stemming to deal with conjugations
        - Difference between written and spoken verb conjugation
        - Gender stem changes in dative phrases (??)   
        - Verb tense; in particular, German has no present continuous tense
        - Disambiguate many-to-many relationships between prepositions (see the table here: http://german.about.com/library/verbs/blverb_prep01.htm) 
3. Decide which programming language to use
  * Python
4. Find 15 sentences to translate
  * TODO
5. Create GitHub repo
  * arjunmathur chrisvh vivekchoksi
6. Divide up programming tasks
  * TODO
