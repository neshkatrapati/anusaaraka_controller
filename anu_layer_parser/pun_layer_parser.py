import os
DOC_PREFIX = 'anu_layer_parser/data'
class PunStory(object):
  def __init__(self, fs):
    self.symbols = {
      'm' : ('Gender', 'masculine'),
      'f' : ('Gender', 'feminine'),
      'sg' : ('Number', 'singular'),
      'pl' : ('Number', 'plural'),
      '1'  : ('Person', 'first'),
      '2' : ('Person', 'second'),
      '3' : ('Person', 'third')
    }
    self.fs = fs

  def get_doc(self, doc_path):
    with open(os.path.join(DOC_PREFIX,doc_path)) as f:
      return f.read()


  def lookup(self, symbol):
    symbol = symbol.strip('\s\t\n,')
    print "Got Symbol :: ", symbol

    if symbol in self.symbols:
      t = []
      for doc in self.symbols[symbol]:
        print "Serving", doc
        t.append((doc, self.get_doc(doc)))

      if len(t) == 1:
        return t[0]
      return t
    return []