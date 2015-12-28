from bs4 import BeautifulSoup
import re
import codecs
import json

precss_stuff = re.compile('=\"(.*?/)?(?P<path>[^\s]*)\.(css|js)\"')
css_stuff = re.compile('=\"(?P<filename>[^/]*)\.css\"')
js_stuff = re.compile('=\"(?P<filename>[^/]*)\.js\"')


def process_html(file_name, num):
    html = open(file_name).read()
    html = precss_stuff.sub('=\"/assets/'+r'\g<path>'+'.css\"', html)
    html = html.replace('<div class=\"float_clear\">', '<div class=\"float_clear\" />')
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

    center = soup.body
    soup.body['id'] = 'center'
    #soup.body['style'] ='width:80%;display:table-cell'
    soup.body.name = 'div'
    body = soup.new_tag('body')
    side_bar = soup.new_tag('div')
    side_bar['id'] = 'side_bar'
    #side_bar['style'] = ''
    center.wrap(body)
    soup.body.append(side_bar)


    html = soup.prettify()


    codecs.open(num+'.layers',"w",'utf-8').write(html)
    #return html

def format_simple(file_name, num, typ):
    html = open(file_name).read()
    soup = BeautifulSoup(html, 'html.parser')
    plain_text = soup.getText().strip()
    open(num+'.'+typ, 'w').write(plain_text.encode('utf-8'))

def format_pun(prefix, num):
    html_file = prefix + '.html'
    source_file = prefix + '_source.html'
    trans_file = prefix + '_trans.html'
    format_simple(source_file, num, 'source')
    format_simple(trans_file, num, 'trans')
    process_html(html_file, num)
    t = {num : {'title':'Dummy', 'trans_title':'dummy'}}
    print json.dumps(t, indent=2)
    #print html_file, source_file, trans_file


import sys
prefix = sys.argv[1]
num= sys.argv[2]
format_pun(prefix, num)