from bs4 import BeautifulSoup
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
    html = html.replace('style.css', 'sanstyle.css')
    html = html.replace('rows.html', '/assets/anurows.html')
    soup = BeautifulSoup(html, 'lxml')
    parent_div = soup.find_all('div', width='700px')
    if len(parent_div) >= 1:
        parent_div = parent_div[0]
        sent = 0
        col = 0
        for child in parent_div.find_all(recursive=False):
            number = child.find_all('td', class_='number')
            if len(number) > 0:
                sent += 1
                col = 1
            child['id'] = sent
            child['col'] = col
            col += 1


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
    center['class'] = 'container'
    center.wrap(body)
    center.insert(0, model)

    html = soup.prettify()


    codecs.open(num+'.layers',"w",'utf-8').write(html)
    #return html


def format_san(html_file, num):
    process_html(html_file, num)
    t = {num : {'title':'Dummy'}}
    print json.dumps(t, indent=2)
    #print html_file, source_file, trans_file


import sys
html_file = sys.argv[1]
num= sys.argv[2]
format_san(html_file, num)