#!/usr/bin/env python
import requests
import sys
import re
from bs4 import BeautifulSoup as BS
from jinja2 import Template, Environment, PackageLoader

index_url = 'https://www.microchip.com/webdoc/avrassembler/' + \
        'avrassembler.wb_instruction_list.html'
inst_url = 'https://www.microchip.com/webdoc/avrassembler/%s'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)' + \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'

class Parser():
    __bs = None
    __html = ''

    def __init__(self):
        return None
    
    def load(self, html):
        self.__bs = BS(html, 'html.parser')

    def clear(self):
        self.__bs = None

    def get_html(self, tag, _id=None, _class=None):
        tags = self.__bs.find_all(tag, id=_id)
        if len(tags) == 0:
            return None

        if _class != None:
            for tag in tags:
                if _class == tag.get('class'):
                    return [tag]

        return tags

def perror(e):
    sys.stderr.write("%s\n" % e)

def GET(url):
    headers = { 'User-Agent': user_agent }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        perror("GET(): error getting content (code: %d)"
                % r.status_code)
        return None
    return r

def main(args):
    # steal data
    index = GET(index_url)
    if index == None:
        return False
 
    # setup parser and template environment
    tpl_env = Environment(loader=PackageLoader('__main__',
        'templates'))
    p = Parser()
    p.load(index.text)

    # get table of contents
    content = p.get_html('div',_class='chapter')
    if content == None:
        perror("Parser.get_html(): error parsing tags")
        return False
    
    # get links and beautify them
    rawlinks = content[0].find_all('a')
    instructs = {}
    ids = 0
    for l in rawlinks:
        t = l.get_text()
        if t == '':
            continue
        t = re.sub(r'[\r\n]+', '', t)
        m = re.match(r'^\s*(?P<inst>[A-Z\s\(\)]+?)\s*-\s*(?P<desc>.+)$', t, \
                re.MULTILINE)
        if m == None:
            continue
        instructs[m.group('inst')] = \
                {'id': ids, 'desc':m.group('desc'), 'href': l.get('href') }
        ids += 1

    template = tpl_env.get_template('index.tpl')
    render = template.render(inst=instructs)

    # generate index
    fd = open('./index.html','w')
    fd.write(render)
    fd.close()

    p.clear()


    template = tpl_env.get_template('instruction.tpl')
    for i in instructs:
        inst_data = GET(inst_url % instructs[i]['href'])
        if inst_data == None:
            perror("main(): error. Not generating %s!" % i)
            continue
        p.load(inst_data.text)
        content = p.get_html('div', _class='section')
        if content == None:
            perror("Parser.get_html(): error parsing tags")
            continue

        render = template.render(instruction=i,content=content[0])
        fd = open(instructs[i]['href'],'wb')
        fd.write(render.encode('utf-8'))
        fd.close()

    p.clear()
    
    return True

if __name__ == '__main__':
    quit(main(sys.argv))
