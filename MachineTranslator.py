import sys

class MachineTranslator:
  def __init__(self, filename):
    self.filename = filename
    pass

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

  def translate(self, sentence):
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
