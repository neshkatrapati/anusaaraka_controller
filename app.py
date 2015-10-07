from flask import Flask, jsonify
from werkzeug.routing import BaseConverter
import os, json

app = Flask(__name__)
Data_Dir = "data/"

class RegexConverter(BaseConverter):
    """
    Need this for flask to parse regex.
    """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter



@app.route("/")
def hello():
    return "Hello World!"


@app.route('/index')
def index():
    """
    Returns list of available GET commands
    """
    return jsonify({"index":"List of commands",
    "group":"List of groups",
    "group/<number>":"List of files in that group",
    "group/<number>/<file_number>":"Serve the file indexed by file_number"})


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

@app.route("/group/<regex('.*([0-9]+)'):group>/<regex('.*([0-9]+)'):file_num>/")
def serve_file(group, file_num):
    """
    Given a group id and file number serves the file
    """
    file_path = os.path.join(os.path.join(Data_Dir, group), file_num + ".json")
    data = None
    with open(file_path) as f:
        data = f.read()
    return jsonify(json.loads(data)) # I need to do this because jsonify apparently **needs** a dict

if __name__ == "__main__":
    app.run(host='0.0.0.0')
