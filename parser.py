'''
This file contains the functions that would parse the input search
string and  print the output search result
'''
import bz2
import os
import re
from searcher import search_for

def get_option(res):
    '''
    The get_option function displays the search results for the user
    and returns the option chosen by the user
    '''
    for re in res:
        print str(res.index(re))+'. '+re['title']
    return int(raw_input('Enter you option: '))
    

srchstr = raw_input('Enter your Query:')
results = search_for(srchstr)
option = get_option(results)

optdict = results[option]

bzfile = bz2.BZ2File(os.path.join("wiki-files/bits",optdict['file_name']))
xmlstr = ''
write = False
for line in bzfile:
    if re.search(optdict['title'],line):
        write = True
    if write:
        xmlstr += line
    if re.search('</page>',line):
        write = False
print xmlstr

