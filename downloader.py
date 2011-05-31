#!/usr/bin/python

'''
Wiktionary dump data can be downloaded from the wikimedia site.

This script is to automatically look for the latest dump and dowmload it.
'''
from HTMLParser import HTMLParser
from urllib2 import urlopen
import os
import re

class Spider(HTMLParser):
    links = []
    def __init__(self, url):
        HTMLParser.__init__(self)
        req = urlopen(url)
        self.feed(req.read())
    def handle_starttag(self, tag, attrs):
        ''' scans all the links and returns the latest dump url '''
        if tag == 'a' and attrs:
            self.links.append(attrs[0][1])
    def latest_dump(self):
        ''' Print the latest dump url '''
        return self.links[-2].strip('/')

if __name__ == "__main__":
    base_url = 'http://dumps.wikimedia.org/tawiktionary/'
    newd = Spider(base_url)
    # Get the list of files from the location
    # select the latest dump
    dat = latest_dump()
    dump_file = 'tawiktionary-'+dat+'-pages-articles.xml.bz2'
    dump_url = base_url+'/'+dat+'/'+dump_file

    files = os.listdir('wiki-files/')
    for fil in files:
        if os.path.isfile('wiki-files/'+fil):
            if re.match('tawiktionary-[0-9]*-pages-articles.xml.bz2', fil):
                dat2 = fil.lstrip('tawiktionary-').rstrip('-pages-articles.xml.bz2')
            if int(dat) > int(dat2):
                #newer dump available update
            elif int(dat) == int(dat2):
                #both are same don't update
            else:
                pass


    # TODO: create a download manager, to manage partial downloads
