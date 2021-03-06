#!/usr/bin/python
#-*- coding: utf-8 -*-

from fs_dispatch import *
import requests
import json
from anu_layer_parser import layer_parser, pun_layer_parser

SAN_ACCEPTED_LAYERS = {
  1 : 'source',
  5 : 'karaka',
  10 : 'morph',
  11 : 'anusarita'
}


UI_LAYERS = {
  'dict' : 'Dictionaries',
  'graph' : 'Information',
  'wiki' : 'Wiki'
}

WIKI_TERMS = {k.strip() : v.strip() for k, v in json.loads(open('unification/wiki_docs.json').read()).items()}

WIKI_URL = "http://10.2.8.55/wiki/doku.php?id={term}"

#r = requests.get('http://0.0.0.0:5010/pb/p2h/'+text+'/html')
@dispatch("[request=[row_num='1', group='3']]")
def sanskrit_hindi_bilingual(fs):
  text = fs["request"]["text"]
  r = requests.get('http://0.0.0.0:5010/ap/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Sanskrit-Hindi Bilingual Dictionary(Apte)', 'priority':0}
  return response


@dispatch("[request=[row_num='1', group='2']]")
def punjabi_hindi_bilingual(fs):
  text = fs["request"]["text"]
  r = requests.get('http://0.0.0.0:5010/pb/p2h/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Punjabi-Hindi Bilingual Dictionary', 'priority':0}
  return response


@dispatch("[request=[row_num='5', group='3']]")
def wiki_dispatch(fs):

  text = fs["request"]["text"].strip()
  content = 'None'
  print text
  if ',' in text:
     text = text.split(',')
     text = text[0].strip()
  text = text.decode('utf-8')
  print [text], "TEST", WIKI_TERMS.keys()
  if text in WIKI_TERMS:
     print "I am IN"
     term = WIKI_TERMS[text]
     url = WIKI_URL.format(term = term)
#     r = requests.get(url)
     content = url
  response = {'type' : 'wiki', 'content' : content, 'name':'Wiki', 'priority':0}
  return response


@dispatch("[request=[row_num='5', group='3']]")
def karaka_highlight(fs):

  text = fs["request"]["text"].strip()
  content = 'Something'
  try:
    if ',' in text:
      text = text.split(',')
      rel = text[0].strip()
      idx = int(text[1].strip())
      sent_num = str(fs['request']['sent_num'])
      col_num = str(fs['request']['col_num'])

#      print "Sent_NUM", sent_num
      sentence = fs['file'][sent_num]
#      print sentence
      word_1 = sentence["source"][col_num]["tok"]
      word_2 = sentence["source"][str(idx)]["tok"]

      r = word_1 + " is the " + rel + " of " + word_2
      content = r
  except:
    pass
  response = {'type' : 'graph', 'content' : content, 'name':'Syntactic-Relations', 'priority':0}
  return response


@dispatch_or("[request=[row_num='5']]","[request=[row_num='9']]","[request=[row_num='10']]","[request=[row_num='11']]")
def hindi_wordnet(fs):
  text = fs["request"]["text"]
  r = requests.get('http://localhost:5010/hw/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Hindi-Wordnet', 'priority':0}
  return response


@dispatch_or("[request=[row_num='5']]","[request=[row_num='9']]","[request=[row_num='10']]","[request=[row_num='11']]")
def hindi_w2v(fs):
  text = fs["request"]["text"]
  r = requests.get('http://localhost:5010/wv/h/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Hindi-Word2Vec', 'priority':1}
  return response


def stuff_to_html(stuff):
#  print type(stuff)
  if len(stuff) < 2:
    return ''
  if len(stuff) == 2:
    #print stuff
    if stuff[0] != None and stuff[1] != None:
      return "<div><h4>"+stuff[0]+"</h4>"+stuff[1]+"</div>"
    else:
      return ''
  else:
    t = ""
    for k in stuff:
      t += stuff_to_html(k)
    return t

@dispatch_or("[request=[row_num='10', group='3']]","[request=[row_num='11', group='3']]")
def hprime_san_interpret(fs):
  text = fs["request"]["text"]
  print [text]
  san_story = layer_parser.SansStory(fs)
  stuff = san_story.get_text_type(text)
  print stuff
  html = stuff_to_html(stuff)
#  r = requests.get('http://localhost:5010/hw/'+text+'/html')
  response = {'type' : 'graph', 'content' : html, 'name':'', 'priority':0}
  return response

@dispatch("[request=[row_num='5', group='2']]")
def hprime_pun_interpret(fs):
  text = fs["request"]["text"]
  print [text]
  html = ""
  pun_story = pun_layer_parser.PunStory(fs)
  for k in pun_story.lookup(text):
    html += stuff_to_html(k)


#   san_story = layer_parser.SansStor(fs)
#   stuff = san_story.get_text_type(text)
#   print stuff
#   html = stuff_to_html(stuff)
# #  r = requests.get('http://localhost:5010/hw/'+text+'/html')
  response = {'type' : 'graph', 'content' : html, 'name':'', 'priority':0}
  return response


def dispatch_functions(fs):

  html = """<ul class="nav nav-tabs" role="tablist">"""
  for info_type, info_name in UI_LAYERS.items():
    class_ = ""
    if info_type == 'dict':
      class_ = 'active'
    html += "<li role=\"presentation\" class=\"{class_}\"><a href=\"#{info_type}\" aria-controls=\"{info_type}\" role=\"tab\" data-toggle=\"tab\">{info_name}</a></li>".format(**locals())
    #elif info_type == 'wiki':


  responses = {rt : {} for rt in UI_LAYERS}

  for rule, func in dispatchRules.items():
    resp = None
    try:
      print "Trying :: ", rule
      resp = func(fs)
      if resp['content'] != 'None':
        responses[resp['type']][resp['priority']] = resp
        name = resp['name']
      print "Function Dispatch ::: Got Response from ", rule, "OK"
    except UnificationError as e:
      print  "Function Dispatch Error ::: Failed to unify", rule
      # continue
    except Exception as e:
      print "Function Dispatch Error ::: Failed to execute", rule, "because", e



  html += '</ul>'
  html += """
  <!-- Tab panes -->
  <div class="tab-content">

  """

#  print responses
  for response_type, response_object in responses.items():
      class_ = ""
      content = ""
#      print response_type, response_object
      if response_type == 'dict':
          class_ = 'active'

      if len(response_object) > 0:
        if response_type in ['dict','graph']:
          if response_type == 'dict':
            class_ = 'active'
          content = "\n".join(["<table><th>"+s['name']+"</th><tr><td>"+s['content']+"</td></tr></table>" for k,s in response_object.items()])
        elif response_type == 'wiki':
          content = "<iframe src='{src}' width='500' height='300'></iframe>".format(src = response_object[0]['content'])
      html += "<div role=\"tabpanel\" class=\"tab-pane {class_}\" id=\"{response_type}\">{content}</div>".format(**locals())

  html += '</div>'

  return html
