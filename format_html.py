from bs4 import BeautifulSoup, NavigableString
import re
import codecs
import json

precss_stuff = re.compile('=\"(.*?/)?(?P<path>[^\s]*)\.css\"')
prejs_stuff = re.compile('=\"(.*?/)?(?P<path>[^\s]*)\.js\"')
css_stuff = re.compile('=\"(?P<filename>[^/]*)\.css\"')
js_stuff = re.compile('=\"(?P<filename>[^/]*)\.js\"')


def process_html(file_name, num):
    html = open(file_name).read()
    html = precss_stuff.sub('=\"/assets/'+r'\g<path>'+'.css\"', html)
    html = prejs_stuff.sub('=\"/assets/'+r'\g<path>'+'.js\"', html)
    html = html.replace('<div class=\"float_clear\">', '<div class=\"float_clear\" />')
    html = html.replace('rows.html', '/assets/rows.html')
    html = html.replace('anusaaraka_tran.js', 'pun_anusaaraka_tran.js')
    soup = BeautifulSoup(html, 'html.parser')

    #my_divs = soup.find_all('div', class_='float_clear')
    my_tables = soup.find_all('table')
    has_table = False
    count = 0
    colid = 0
    for table in my_tables:
        #next_sibling = div.next_sibling
        trs =  table.find_all('tr', recursive = False)
        my_tr = trs[0]
        my_tr_l = len([t for t in my_tr.children if t not in ['\n']])
        #print my_tr_l
        if my_tr_l > 1:
            count += 1
            colid = 1

        table["id"] = count
        table["col"] = colid
        all_tds = table.find_all('td')
        colid += 1


        # colid = 1
        # for next_sibling in div.next_siblings:
        #     try:
        #         if next_sibling.name == 'table':
        #             next_sibling['id'] = count
        #             next_sibling['col'] = colid
        #             colid += 1
        #             e = True
        #         elif next_sibling.name == 'div':
        #             break
        #     except Exception as e:
        #         print e

        # if e:
        #     count += 1




    model_stuff = BeautifulSoup("""
    <div class="modal-dialog">

      <!-- Modal content-->
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" onclick='closeModal()'>&times;</button>
          <h4 class="modal-title">Modal Header</h4>
        </div>
        <div class="modal-body" id='reqbody'>
          <p>Some text in the modal.</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>

    </div>
    """,'html.parser')

    jq = soup.new_tag('script')
    jq['src'] = "/assets/jquery_11.min.js"
    ev = soup.new_tag('script')
    bj = soup.new_tag('script')
    bj['src'] = "/assets/bootstrap/js/bootstrap.js"
    ev['src'] = '/assets/events.js'
    bc = soup.new_tag('link')
    bc['href'] = "/assets/bootstrap/css/bootstrap.css"
    bc['type'] = 'text/css'
    bc['rel'] = 'stylesheet'
    soup.head.insert(len(soup.head.contents), bc)
    soup.body.insert(len(soup.body.contents), jq)
    soup.body.insert(len(soup.body.contents), bj)
    soup.body.insert(len(soup.body.contents), ev)
    #soup.body.('<script src=\"/assets/events.js\"></script>')

    center = soup.body
    soup.body['id'] = 'center'
    #soup.body['style'] ='width:80%;display:table-cell'
    soup.body.name = 'div'
    body = soup.new_tag('body')
    model = soup.new_tag('div')
    model["class"] = "modal fade"
    model["id"] = "modal"
    model["role"] = "modal"
    model.append(model_stuff)
    #side_bar = soup.new_tag('div')
    #side_bar['id'] = 'side_bar'
    #side_bar['style'] = ''
    #d = soup.new_tag('div')
    #d['class'] = 'container'
    center['class'] = 'container'
    center.wrap(body)
    center.insert(0, model)
    #d.wrap(body)


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