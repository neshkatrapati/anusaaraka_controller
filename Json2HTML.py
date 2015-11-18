import demjson

def render_json(file_path):

    jsondata = open(file_path,'r').read()
    layers = demjson.decode(jsondata)

    #print layers['padasuthra']

    output = ""

    html = '''<!DOCTYPE html><head>
    <link href="/static/style.css"  rel="stylesheet" />
    </head>
    <body>
    <table cellspacing="0">'''

    layer_order = layers["meta"]["layer_order"]

    #print layer_order
    j = 1
    for layer in layer_order:
        j += 1
        #html += '<tr>\n'
        for kk, vv in layers[layer].iteritems():
            html += '<tr class="row"'+str(j) + '>\n'

            for i in range(1, 13):
            #for kkk, vvv in vv.iteritems():
                if str(i) in vv.keys():
                    html += '<td class="number">' + vv[str(i)] + '</td>\n'
            html += '</tr>\n'

    #print html
    html += '''</table>
    </body>
    </html>'''

    return html