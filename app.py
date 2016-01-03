from flask import Flask, jsonify, send_from_directory, render_template, request, redirect
from regex_converter import *
import os, json
import random
from bs4 import BeautifulSoup
import re
from Json2HTML import render_json
import codecs
import requests
from unification import helpers, fs_dispatch, dispatch_functions
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)
Data_Dir = "data/"

# Add this to enable regex parsing of the url.
app.url_map.converters['regex'] = RegexConverter


#precss_stuff = re.compile('=\".*?/(?P<filename>[^/]*)\.css\"')
precss_stuff = re.compile('=\"(.*?/)?(?P<path>[^\s]*)\.(css|js)\"')
css_stuff = re.compile('=\"(?P<filename>[^/]*)\.css\"')
js_stuff = re.compile('=\"(?P<filename>[^/]*)\.js\"')

@app.route("/")
def hello():
    return open('templates/home.html').read()



@app.route('/index')
def index():
    """
    Returns list of available GET commands
    """
    return jsonify({"index":"List of commands",
    "group":"List of groups",
    "group/<number>":"List of files in that group",
    "group/<number>/<file_number>":"Serve the file indexed by file_number",
    "group/<number>/<file_number>/html":"Serve the file indexed by file_number in html"})


def num_group(group_num):
    """
    Returns the number of files in a group
    """
    group_dir = os.path.join(Data_Dir, group_num)
    return len(os.listdir(group_dir))

@app.route("/group")
def list_groups():
   """
   Returns the list of groups (ids)
   """
   groups = os.listdir(Data_Dir)
   groups.sort()
   groupDict = {group : num_group(group) for group in groups}
   return jsonify(groupDict)


@app.route("/group/<regex('.*([0-9]+)'):group>/")
def list_group(group):
    """
    Renders index.html in that group.
    """
    meta = json.loads(open('data/{group}/meta.json'.format(**locals())).read())
    images = os.listdir('images/story_images')
    texts = []


    for text, data in meta.items():
        ntext = {'id':text}
        ntext['title'] = data['title']
        ntext['single'] = False

        if 'trans_title' in data:
            ntext['trans_title'] = data['trans_title']
            ntext['single'] = True
        random.shuffle(images)
        ntext['image'] = '/images/story_images/' + images[0]
        texts.append(ntext)


    print texts

    return render_template('group.html',
                            texts = texts,
                            group = group)



@app.route("/<regex('.*'):path>/")
def serve_static(path):
    print path
    return send_from_directory('.', path)


def get_json_file(group, file_num):
    file_path = os.path.join(os.path.join(Data_Dir, group), file_num + '.json')
    data = None
    print file_path
    with open(file_path) as f:
        data = f.read()
    return json.loads(data)


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/")
def serve_file(group, file_num):
    """
    Given a group id and file number serves the file
    """
    return jsonify(get_json_file(group, file_num)) # I need to do this because jsonify apparently **needs** a dict


def get_sentences(file_name):
    with codecs.open(file_name,'r','utf-8') as f:
        sentences = []
        sentence = {}
        count=0
        for index, line in enumerate(f):
            line = line.strip()
            if len(line) > 0:
                if count % 2 == 0:
                    sentence["id"] = line.strip()
                else:
                    sentence["text"] = line.strip()
                    sentences.append(sentence)
                    sentence = {}
                count += 1

    print sentences

    return sentences



@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/html")
def serve_file_html(group, file_num):
    """
    Given a group id and file number serves the file
    """


    if os.path.exists('data/{group}/{file_num}.source'.format(**locals())) == False:
        return redirect('/group/'+str(group)+'/'+str(file_num)+'/layers')

    sentences = get_sentences('data/{group}/{file_num}.source'.format(**locals()))
    all_files = [f.split('.')[0] for f in os.listdir('data/{group}'.format(**locals())) if f.endswith('.html') == False]
    all_files = list(set(all_files))
    number_of_files = len(all_files)
    nxt = None
    prv = None
    file_num = int(file_num)
    if file_num > 1:
        prv = file_num - 1
    if file_num < number_of_files:
        nxt = file_num + 1


    meta = json.loads(open('data/{group}/meta.json'.format(**locals())).read())


    return render_template('source.html',
                            sentences = sentences,
                            next = nxt,
                            prev = prv,
                            name = meta[str(file_num)]['title'],
                            group = group,
                            curr = file_num)


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/trans")
def serve_file_trans(group, file_num):
    """
    Given a group id and file number serves the file
    """
    sentences = get_sentences('data/{group}/{file_num}.trans'.format(**locals()))
    all_files = [f.split('.')[0] for f in os.listdir('data/{group}'.format(**locals())) if f.endswith('.html') == False]
    all_files = list(set(all_files))
    number_of_files = len(all_files)
    nxt = None
    prv = None
    file_num = int(file_num)
    if file_num > 1:
        prv = file_num - 1
    if file_num < number_of_files:
        nxt = file_num + 1

    meta = json.loads(open('data/{group}/meta.json'.format(**locals())).read())

    return render_template('trans.html',
                            sentences = sentences,
                            next = nxt,
                            prev = prv,
                            group = group,
                            name = meta[str(file_num)]["trans_title"],
                            curr = file_num)


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/layers")
def serve_file_layers(group, file_num):
    """
    Given a group id and file number serves the file
    """
    html = open('data/{group}/{file_num}.layers'.format(**locals())).read()
    #html = process_html(html)
    return html


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/<regex('.*([0-9]+)'):sent_num>/<regex('.*([0-9]+)'):row_num>/<regex('.*([0-9]+)'):col_num>")
@cross_origin()
def request_graph(group, file_num, sent_num, row_num, col_num):
    text = request.args.get('text')
    request_data = {'group':group,
            'file_num':file_num,
            'sent_num':sent_num,
            'row_num':row_num,
            'col_num':col_num,
            'text':text}
    file_data = get_json_file(group, file_num)
    data = {'request' : request_data, 'file' : file_data}
    text = text.strip('\" \n\t')
    #r = requests.get('http://0.0.0.0:5010/pb/p2h/'+text+'/html')
#    r = requests.get('http://localhost:5010/wv/h/'+text+'/html')
    #r = requests.get('http://localhost:5010/hw/'+text+'/html')

    feat =  helpers.dict_to_feat(data)
    content = dispatch_functions.dispatch_functions(feat)
    r = requests.get('http://0.0.0.0:5010/ap/'+text+'/html')
    #print 'http://0.0.0.0:5010/pb/p2h/'+text+'/html'
    #return r.content
    return content
    #return jsonify(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
