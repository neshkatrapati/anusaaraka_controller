from nltk.featstruct import FeatStruct


def dict_to_feat(d):
  return FeatStruct(_dict_to_feat(d))

def _dict_to_feat(d):
  s = unicode("[")
  for key, value in d.items():
    if type(value) is dict:
      value = _dict_to_feat(value)
      s += key + '=' + value
    else:

      if type(value) in [str, unicode]:
        value = value.strip(' \"\t\n')
      else:
        value = str(value)

      s += key + '=\'' + value + '\''

    s += ", "
  s += "]"
  return s