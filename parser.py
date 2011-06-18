'''
This file contains the functions that would parse the input search
string and  print the output search result
'''

#---------------------------------------
'''
TODO:
Recode for returning the options and the
markup separately
'''
#---------------------------------------

import bz2
import os
import re
from searcher import search_for

import BeautifulSoup

def get_option(res):
    '''
    The get_option function displays the search results for the user
    and returns the option chosen by the user
    '''
    for re in res:
        print str(res.index(re))+'. '+re['title']
    return int(raw_input('Enter you option: '))
    
def get_markup(srchstr):
    '''
    The get_markup funtion get the search string as the input parameter
    and returns the MediaWiki text as return
    '''
    markup = ''
    results = search_for(srchstr)
    option = get_option(results)

    optdict = results[option]

    bzfile = bz2.BZ2File(os.path.join("wiki-files/bits",optdict['file_name']))
    xmlstr = '  <page>\n'
    write = False
    for line in bzfile:
        if re.search(optdict['title'],line):
            write = True
        if write:
            xmlstr += line
        if re.search('</page>',line):
            write = False
    dom = BeautifulSoup.BeautifulSoup(xmlstr)
    txt=dom.find('text')
    if txt is not None:
        markup = txt.text
    return markup

if __name__ == "__main__":
    mtxt = get_markup(raw_input('Enter your Query:'))
    print mtxt




