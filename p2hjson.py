from bs4 import BeautifulSoup
from collections import defaultdict
from pprint import pprint
from json import dump, load, dumps
import sys

LAYER_FILE = "3.layers"
LAYER_NAME_MAP = {
	"row1": "source",
	"row2": "transliterated",
	"row3": "sourcemorph",
	"row4": "guessmorph",
	"row5": "pickonemorph",
	"row6": "lextransfer",
	"row7": "pos",
	"row8": "chunk",
	"row9": "target",
	"row10": "jk"
}

def tok_handler(story, sentno, layer_name, pada_cat, pada_token):
	story[sentno][layer_name]["tok"] = pada_token

def pos_handler(story, sentno, layer_name, pada_cat, pada_token):
	story[sentno][layer_name]["pos"] = pada_token

def chunktag_handler(story, sentno, layer_name, pada_cat, pada_token):
	story[sentno][layer_name]["chunktag"] = pada_token

def af_handler(story, sentno, layer_name, pada_cat, pada_token):
	for feat, val in zip(["root", "lcat", "gen", "per", "num", "cm/tam", "suff"], pada_token.split(",")):
		# if val is not "-":
		story[sentno][layer_name][feat] = val.strip()

LAYER_HANDLER = {
	LAYER_NAME_MAP["row1"]: tok_handler,
	LAYER_NAME_MAP["row2"]: tok_handler,
	LAYER_NAME_MAP["row3"]: af_handler,
	LAYER_NAME_MAP["row4"]: af_handler,
	LAYER_NAME_MAP["row5"]: af_handler,
	LAYER_NAME_MAP["row6"]: tok_handler,
	LAYER_NAME_MAP["row7"]: pos_handler,
	LAYER_NAME_MAP["row8"]: chunktag_handler,
	LAYER_NAME_MAP["row9"]: tok_handler,
	LAYER_NAME_MAP["row10"]: tok_handler
}

storyid = sys.argv[1]	# this is the file name
story = BeautifulSoup(open(storyid + ".layers"), "html.parser")
story_data = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
numsents = 0
for sentno, sentence in enumerate(story.find_all("table")):
	sentence_id = sentence.get('id')
	#print sentence_id
	#print sentence
	for layer in sentence.find_all("tr", recursive = False):
		layer_name = LAYER_NAME_MAP[layer.get("class")[0]].strip().encode("utf8")	# bs4 can give multiple class values?! So, take the first one. Trivial.
		handler = LAYER_HANDLER[layer_name]
		tds = list(layer.find_all('td'))
		#print tds, len(tds)
		if len(tds) > 1:
			tds = tds[1:]

		for pada in tds:	# the first element is the ID eg. "1.1.J" which is not needed.
			pada_cat = pada.get("class")[0].strip().encode("utf8")	# bs4 can give multiple class values?! So, take the first one. Trivial.
			#print pada
			pada_token = pada.contents[0].strip().encode("utf8")
			#print pada_token
			handler(story_data, sentence_id, layer_name, pada_cat, pada_token)
	numsents += 1
story_data["meta"]["numsents"] = numsents
story_data["meta"]["storyid"] = storyid
print dumps(story_data)
# with open(storyid + ".json", "w") as f:
# 	dump(story_data, f, ensure_ascii=False)
