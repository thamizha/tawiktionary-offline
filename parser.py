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
import codecs
from searcher import search_for

import BeautifulSoup
    
def get_markup(srchstr):
    '''
    The get_markup funtion get the search string as the input parameter
    and returns the MediaWiki text as return
    '''
    #markup = ''
    results = search_for(srchstr)
    #print the Text Matches
    for r in results:
        print str(results.index(r))+'. '+r['title']
    #Get the option
    option = int(raw_input('Enter you option: '))

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
    else:
        markup = ''
    return markup

if __name__ == "__main__":
    mtxt = get_markup(raw_input('Enter your Query:'))
    f = codecs.open('markup.txt', encoding='utf-8', mode='a')
    f.write(mtxt)
    f.close()
    print mtxt
