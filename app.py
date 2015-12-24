from flask import Flask, jsonify, send_from_directory, render_template, request
from regex_converter import *
import os, json
import random
from bs4 import BeautifulSoup
import re
from Json2HTML import render_json
import codecs
app = Flask(__name__)
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
        ntext['trans_title'] = data['trans_title']
        random.shuffle(images)
        ntext['image'] = '/images/story_images/' + images[0]
        texts.append(ntext)

    print texts

    return render_template('group.html',
                            texts = texts,
                            group = group)



    # group_dir = os.path.join(Data_Dir, group)
    # group_list = os.listdir(group_dir)
    # group_list.sort()
    # group_files = {index + 1: file_name for index, file_name in enumerate(group_list)}
    # return jsonify(group_files)

@app.route("/<regex('.*'):path>/")
def serve_static(path):
    print path
    return send_from_directory('.', path)


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/")
def serve_file(group, file_num):
    """
    Given a group id and file number serves the file
    """
    group_files = os.listdir(os.path.join(Data_Dir, group))
    group_files.sort()
    file_num = int(file_num)
    file_path = os.path.join(os.path.join(Data_Dir, group), group_files[file_num - 1])
    data = None
    print file_path
    with open(file_path) as f:
        data = f.read()
    return jsonify(json.loads(data)) # I need to do this because jsonify apparently **needs** a dict


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



def process_html(html):
    #html = html.replace('../assets','/assets')
    #html = html.replace('../images','/images')
    html = precss_stuff.sub('=\"/assets/'+r'\g<path>'+'.css\"', html)
    html = html.replace('<div class=\"float_clear\">', '<div class=\"float_clear\" />')
    #html = css_stuff.sub('=\"/assets/'+r'\g<filename>'+'.css\"', html)
    #html = js_stuff.sub('=\"/assets/'+r'\g<filename>'+'.js\"', html)

    soup = BeautifulSoup(html, 'html.parser')



    my_divs = soup.find_all('div', class_='float_clear')
    has_table = False
    count = 1
    for div in my_divs:
        next_sibling = div.next_sibling
        e = False
        colid = 1
        for next_sibling in div.next_siblings:
            try:
                if next_sibling.name == 'table':
                    next_sibling['id'] = count
                    next_sibling['col'] = colid
                    colid += 1
                    e = True
                elif next_sibling.name == 'div':
                    break
            except Exception as e:
                print e

        if e:
            count += 1


    jq = soup.new_tag('script')
    jq['src'] = "/assets/jquery_11.min.js"
    ev = soup.new_tag('script')
    ev['src'] = '/assets/events.js'
    soup.body.insert(len(soup.body.contents), jq)
    soup.body.insert(len(soup.body.contents), ev)
    #soup.body.('<script src=\"/assets/events.js\"></script>')


    html = soup.prettify()


    codecs.open('test.html',"w",'utf-8').write(html)
    return html


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/layers")
def serve_file_layers(group, file_num):
    """
    Given a group id and file number serves the file
    """
    html = open('data/{group}/{file_num}.layers'.format(**locals())).read()
    html = process_html(html)
    return html


@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/<regex('.*([0-9]+)'):sent_num>/<regex('.*([0-9]+)'):row_num>/<regex('.*([0-9]+)'):col_num>")
def request_graph(group, file_num, sent_num, row_num, col_num):
    text = request.args.get('text')
    data = {'group':group,
            'file_num':file_num,
            'sent_num':sent_num,
            'row_num':row_num,
            'col_num':col_num,
            'text':text}
    return jsonify(data)



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
