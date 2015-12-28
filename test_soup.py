from bs4 import BeautifulSoup
import re
import codecs
import json


html = """
<html>
  <body>
    <i> test </i>
    <a href=""></a>
  </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')
soup.body.name = 'div'
print soup