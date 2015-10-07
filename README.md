# What is this ?

This is controller for anusaaraka accessor project implemented in flask.

# How to get it running ?

``` bash
python app.py
```

# What does it serve now ?
- /index

``` json
{
  "group": "List of groups",
  "group/<number>": "List of files in that group",
  "group/<number>/<file_number>": "Serve the file indexed by file_number",
  "index": "List of commands"
}
```

- /group

``` json
{
  "1": 1,
  "2": 0
}
```

- /group/1

``` json
{
  "1": "1.json"
}
```

- /group/1/1

``` json
{
  "id_last_word": {
    "21": "goal"
  },
  "id_word": {
    "1": " ever",
    "2": " since",
    "3": " the",
    "4": " incipient",
    "5": " of",
    "6": " computers",
    "7": " and",
    "8": " the",
    "9": " very",
    "10": " first",
    "11": " introduction",
    "12": " of",
    "13": " artificial",
    "14": " intelligence",
    "15": " machine",
    "16": " translation",
    "17": " has",
    "18": " been",
    "19": " a",
    "20": " target",
    "21": " goal"
  }
}
```
