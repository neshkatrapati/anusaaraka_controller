#!/usr/bin/python
# -*- coding: utf-8 -*-
from json import load as load
from collections import defaultdict
SAN_ACCEPTED_LAYERS = {
  1 : 'source',
  5 : 'karaka',
  10 : 'morph',
  11 : 'anusarita'
}
class SansStory:
    PADA = 5001
    MORPH = 5002
    VIB = 5003
    PRAT = 5004
    PRATSYM = 6001
    VIBSYM = 6002
    DIVSYM = 6003
    prattyaya_braces = ["<",">"]
    vibhakti_braces = ["{","}"]
    feat_delimiter = "/"
    pratambig_sym = "`"
    div_symbol = "->"
    def __init__(self,fs):
        self.story_data = fs["file"]
        # with open(fs) as f:
        #     self.story_data = load(f)
        # hardcode the file map
        self.featfmap = defaultdict(lambda: None)
        self.featfmap[("gen","पु०")] = "masculine.txt"
        self.featfmap["gen"] = "gen.txt"
    def change_story(self, fs):
        self.story_data = fs["file"]
    def get_text_type(self, text, sentno, layer, colno):
        feats = defaultdict(lambda: None)
        feats.update(self.story_data[str(sentno)][SAN_ACCEPTED_LAYERS[int(layer)]][str(colno)])
        if layer in [10,11]:
            if text.strip() == SansStory.div_symbol:
                return self.featfmap["divsym"]
            elif text.strip() in SansStory.prattyaya_braces:
                return self.featfmap["pratsym"]
            elif text.strip() in SansStory.vibhakti_braces:
                return self.featfmap["vibsym"]
            elif text.strip() == SansStory.pratambig_sym:
                return self.featfmap["pratambigsym"]
            elif text.strip() == SansStory.feat_delimiter:
                return self.featfmap["delimsym"]
            else:
                featdoc = None
                valdoc = None
                auxdoc = None
                selfeat = None
                # identify the feature to get docs for
                # enable a partial match
                for feat in ["num","gen","per","vib","prattyaya","pada"]:
                    if feats[feat] is not None and text in feats[feat].encode("utf8"): # hit the feature
                        selfeat = feat
                        break
                if selfeat is not None:
                    # feature docs
                    if self.featfmap[selfeat] is not None:
                        with open("data/"+self.featfmap[selfeat]) as fdoc:
                            featdoc = fdoc.read().strip()
                    # value docs
                    if self.featfmap[(selfeat, feats[selfeat].encode("utf8"))] is not None:
                        with open("data/"+self.featfmap[(selfeat, feats[selfeat].encode("utf8"))]) as fvdoc:
                            valdoc = fvdoc.read().strip()
                    # aux docs
                    if selfeat == "prattyaya" and feats["pratambig"] == True:
                        if self.featfmap["pratambig"] is not None:
                            with open("data/"+self.featfmap["pratambig"]) as adoc:
                                auxdoc = adoc.read().strip()
                    elif selfeat == "vib" and feats["vibdiv"] == True:
                        if self.featfmap["vibdiv"] is not None:
                            with open("data/"+self.featfmap["vibdiv"]) as adoc:
                                auxdoc = adoc.read().strip()
                return featdoc,valdoc,auxdoc 
a = SansStory("/data/raship/anusaaraka_language_accessor/anusaaraka_controller/data/3/1.json")
print a.get_text_type("पु०",1,10,1)