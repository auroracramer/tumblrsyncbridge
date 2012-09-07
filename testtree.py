import xml.etree.ElementTree as ET
from updateposts import *
sample = {'post_url': 'http://post_url', 'date': '12/12/1212', 'body': 'TEST BODY', 'type': 'text', 'title': 'Test Title'}
f = open('test.xml', 'r+b')
etree = get_etree(f)
add_post_element(sample, etree)
save_etree(etree, f)