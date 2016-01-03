#!/usr/bin/python
#-*- coding: utf-8 -*-

from fs_dispatch import *
import requests
import json 

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


@dispatch("[request=[row_num='1']]")
def sanskrit_hindi_bilingual(fs):
  text = fs["request"]["text"]
  r = requests.get('http://0.0.0.0:5010/ap/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Sanskrit-Hindi Bilingual Dictionary(Apte)'}
  return response

@dispatch("[request=[row_num='5']]")
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
  response = {'type' : 'wiki', 'content' : content, 'name':'Wiki'}
  return response



@dispatch_or("[request=[row_num='10']]","[request=[row_num='11']]")
def hindi_wordnet(fs):
  text = fs["request"]["text"]
  r = requests.get('http://localhost:5010/hw/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Hindi-Wordnet'}
  return response


@dispatch_or("[request=[row_num='10']]","[request=[row_num='11']]")
def hindi_w2v(fs):
  text = fs["request"]["text"]
  r = requests.get('http://localhost:5010/wv/h/'+text+'/html')
  response = {'type' : 'dict', 'content' : r.content, 'name':'Hindi-Word2Vec'}
  return response

def dispatch_functions(fs):

  html = """<ul class="nav nav-tabs" role="tablist">"""
  for info_type, info_name in UI_LAYERS.items():
    class_ = ""
    if info_type == 'dict':
      class_ = 'active'
    html += "<li role=\"presentation\" class=\"{class_}\"><a href=\"#{info_type}\" aria-controls=\"{info_type}\" role=\"tab\" data-toggle=\"tab\">{info_name}</a></li>".format(**locals())
    #elif info_type == 'wiki':
  responses = {rt : [] for rt in UI_LAYERS}

  for rule, func in dispatchRules.items():
    try:
      resp = func(fs)
      if resp['content'] != 'None':
        responses[resp['type']].append(resp)
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
  for response_type, response_object in responses.items():
    class_ = ""
    if response_type == 'dict':
      class_ = 'active'
      content = "\n".join(["<table><th>"+s['name']+"</th><tr><td>"+s['content']+"</td></tr></table>" for s in response_object])
    elif response_type == 'wiki':
      content = "<iframe src='{src}' width='500' height='300'></iframe>".format(src = response_object[0]['content'])
    html += "<div role=\"tabpanel\" class=\"tab-pane {class_}\" id=\"{response_type}\">{content}</div>".format(**locals())

  html += '</div>'

  return html
