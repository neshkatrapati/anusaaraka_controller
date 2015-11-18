from flask import Flask, jsonify, send_from_directory
from regex_converter import *
import os, json
from Json2HTML import render_json

app = Flask(__name__)
Data_Dir = "data/"

# Add this to enable regex parsing of the url.
app.url_map.converters['regex'] = RegexConverter

@app.route("/")
def hello():
    return index()


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
    Returns the list of files (file_id:file_name) that belong to a group
    """
    group_dir = os.path.join(Data_Dir, group)
    group_list = os.listdir(group_dir)
    group_list.sort()
    group_files = {index + 1: file_name for index, file_name in enumerate(group_list)}
    return jsonify(group_files)

@app.route("/static/<regex('.*'):path>/")
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

@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/html")
def serve_file_html(group, file_num):
    """
    Given a group id and file number serves the file
    """
    group_files = os.listdir(os.path.join(Data_Dir, group))
    group_files.sort()
    file_num = int(file_num)
    file_path = os.path.join(os.path.join(Data_Dir, group), group_files[file_num - 1])
    data = None
    html = render_json(file_path)
    #print html
    return html
    # print file_path
    # with open(file_path) as f:
    #     data = f.read()
    # return jsonify(json.loads(data)) # I need to do this because jsonify apparently **needs** a dict



if __name__ == "__main__":
    app.run(host='0.0.0.0')
