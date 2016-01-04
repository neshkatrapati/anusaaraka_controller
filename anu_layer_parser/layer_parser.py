#!/usr/bin/python
# -*- coding: utf-8 -*-
from json import load as load
from collections import defaultdict
import codecs
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
        self.req = fs["request"]
        # with open(fs) as f:
        #     self.story_data = load(f)
        # hardcode the file map
        self.featfmap = defaultdict(lambda: None)
        self.featfmap["gen"] = "Gender"
        self.featfmap[("gen","पु०")] = "masculine"
        self.featfmap[("gen","स्त्री०")] = "feminine"
        self.featfmap[("gen","न०")] = "neuter"
        self.featfmap[("gen","सर्व०")] = "pronoun"

        self.featfmap["num"] = "Number"
        self.featfmap[("num","एक०")] = "singular"
        self.featfmap[("num","द्वि०")] = "dual"
        self.featfmap[("num","बहु०")] = "plural"

        self.featfmap["per"] = "Person"

        self.featfmap["prattyaya"] = "pratyaya-upasarga"
        self.featfmap[("prattyaya","कर")] = "kar_pratyaya"
        self.featfmap[("prattyaya","में")] = "vibhakti-mem"
        self.featfmap[("prattyaya","को")] = "vibhakti-ko"
        self.featfmap[("prattyaya","के")] = "vibhakti-kA"
        self.featfmap[("prattyaya","का")] = "vibhakti-kA"
        self.featfmap[("prattyaya","की")] = "vibhakti-kA"
        self.featfmap[("prattyaya","से")] = "vibhakti-se"
        self.featfmap[("prattyaya","से3")] = "vibhakti-se"
        self.featfmap[("prattyaya","के_लिये")] = "vibhakti-ke-liye"
        self.featfmap[("prattyaya","ने")] = "vibhakti-ne"
        self.featfmap[("prattyaya","पर")] = "vibhakti-par"

        self.featfmap["vib"] = "pratyaya-upasarga"
        self.featfmap[("vib","0")] = "zero-vibhakti"
        self.featfmap[("vib","में")] = "vibhakti-mem"
        self.featfmap[("vib","को")] = "vibhakti-ko"
        self.featfmap[("vib","के")] = "vibhakti-kA"
        self.featfmap[("vib","का")] = "vibhakti-kA"
        self.featfmap[("vib","की")] = "vibhakti-kA"
        self.featfmap[("vib","से")] = "vibhakti-se"
        self.featfmap[("vib","से3")] = "vibhakti-se"
        self.featfmap[("vib","के_लिये")] = "vibhakti-ke-liye"
        self.featfmap[("vib","ने")] = "vibhakti-ne"
        self.featfmap[("vib","पर")] = "vibhakti-par"
    def change_story(self, fs):
        self.story_data = fs["file"]
    def get_text_type(self, text):
        layer = int(self.req["row_num"])
        sentno = self.req["sent_num"]
        colno = self.req["col_num"]
        feats = defaultdict(lambda: None)
        feats.update(self.story_data[str(sentno)][SAN_ACCEPTED_LAYERS[int(layer)]][str(colno)])
        if layer in [10,11]:
            if text.strip() == SansStory.div_symbol:
                with codecs.open("anu_layer_parser/data/"+"->symbol",encoding="utf-8") as symdoc:
                    symtitle = "Divergence Marker"
                    symdoc = symdoc.read().strip().encode("utf8")
                return symtitle,symdoc
            elif text.strip() in SansStory.vibhakti_braces:
                with codecs.open("anu_layer_parser/data/"+"{}symbol",encoding="utf-8") as symdoc:
                    symtitle = "Vibhakti Marker"
                    symdoc = symdoc.read().strip().encode("utf8")
                return symtitle,symdoc
            elif text.strip() in SansStory.prattyaya_braces:
                with codecs.open("anu_layer_parser/data/"+"<>symbol",encoding="utf-8") as symdoc:
                    symtitle = "Prattyaya Marker"
                    symdoc = symdoc.read().strip().encode("utf8")
                return symtitle,symdoc
            elif text.strip() == SansStory.pratambig_sym:
                with codecs.open("anu_layer_parser/data/"+"\'symbol",encoding="utf-8") as symdoc:
                    symtitle = "Ambiguous Prattyaya Marker"
                    symdoc = symdoc.read().strip().encode("utf8")
                return symtitle,symdoc
            else:
                featdoc = None
                valdoc = None
                auxdoc = None
                feattitle, valtitle, auxtitle = None, None, None
                selfeat = None
                # identify the feature to get docs for
                # enable a partial match
                print text, [text], type(text)
                titlemap = {"num":"Number","gen":"Gender","per":"Person","vib":"Vibhakti","prattyaya":"Prattyaya","pada":"Pada"}
                for feat in ["num","gen","per","vib","prattyaya","pada"]:
                    if feats[feat] is not None and text in feats[feat]: # hit the feature
                        selfeat = feat
                        break
        #        print "Selfeat::", selfeat
                if selfeat is not None:
                    # feature docs
                    if self.featfmap[selfeat] is not None:
                        with codecs.open("anu_layer_parser/data/"+self.featfmap[selfeat],encoding="utf-8") as fdoc:
                            feattitle = titlemap[selfeat]
                            featdoc = fdoc.read().strip().encode("utf8")
                    # value docs
                    if self.featfmap[(selfeat, feats[selfeat])] is not None:
                        with codecs.open("anu_layer_parser/data/"+self.featfmap[(selfeat, feats[selfeat])],encoding="utf-8") as fvdoc:
                            valtitle = self.featfmap[(selfeat, feats[selfeat])]
                            valdoc = fvdoc.read().strip().encode("utf8")
                    # aux docs
                    if selfeat == "prattyaya" and feats["pratambig"] == True:
                        if self.featfmap["pratambig"] is not None:
                            with codecs.open("anu_layer_parser/data/"+"\'symbol",encoding="utf-8") as adoc:
                                auxtitle = "Ambiguous Prattyaya Marker"
                                auxdoc = adoc.read().strip().encode("utf8")
                    elif selfeat == "vib" and feats["vibdiv"] == True:
                        if self.featfmap["vibdiv"] is not None:
                            with codecs.open("anu_layer_parser/data/"+"->symbol",encoding="utf-8") as adoc:
                                auxtitle = "Divergence Marker"
                                auxdoc = adoc.read().strip().encode("utf8")
                return (feattitle,featdoc),(valtitle,valdoc),(auxtitle,auxdoc)
# a = SansStory("/anu_layer_parser/data/raship/anusaaraka_language_accessor/anusaaraka_controller/anu_layer_parser/data/3/1.json")
# a.get_text_type("पु०",1,10,1)
