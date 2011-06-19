#!/usr/bin/python

'''
In order to make the Dictionary searchable the wikipage titles should be indexed.

This indexer is based on the Whoosh search engine library.
'''
#----------------------------------------------------------------------
'''
Algorithm:
----------
xml.bz2
line by line
detect <page>
Make soup
find Title & index
find Text & index

'''
#----------------------------------------------------------------------
import os
import bz2
import re
import codecs
import BeautifulSoup
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, STORED

class MySchema(SchemaClass):
    word = TEXT(stored=True)
    meaning = TEXT(stored=True)
    

def dump_file():
    ''' This function searches the directory and returns the latest xml dump file'''
    files = [fil for fil in os.listdir('wiki-files') if os.path.isfile(os.path.join('wiki-files',fil))]
    #print os.listdir('wiki-files')
    print files
    return files[0]

def create_index():
    ''' This is the main function '''
    # check wether a index exists
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    # create a indexer object
    ix = index.create_in("indexdir", MySchema)
    ix = index.open_dir("indexdir")
        
    # Some function globals
    page_count = 0
    writ = False
    xmlstr = ''
    #Open the dump file
    bzfile = bz2.BZ2File(os.path.join('wiki-files',dump_file()))
    f = codecs.open('list.txt', encoding='utf-8', mode='w')
    # create a writer to write index
    writer = ix.writer()
    for line in bzfile:
        if re.search('<page>',line):
            writ = True
        if writ:
            xmlstr += line
        if re.search('</page>',line):
            writ = False
            #create soup
            dom = BeautifulSoup.BeautifulSoup(xmlstr)
            title = dom.find('title').text
            txt = dom.find('text').text
            #write to index
            writer.add_document(word=title, meaning=txt)
            f.write(title+'\n')
            print title
            page_count += 1
            xmlstr = ''
        if page_count > 500:
            writer.commit()
            writer = ix.writer()
            # Reset page count after each commit
            page_count = 0
    # to commit the last bit in writer
    try:
        writer.commit()
    bzfile.close()
    f.close()
        
    

#-----------------------------------------------------------------------

if __name__ == "__main__":
    create_index()
    '''
    # check wether a index exists
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    # create a indexer object
    ix = index.create_in("indexdir", MySchema)
    ix = index.open_dir("indexdir")
    
    
    # read all the file in the bits folder
    for fil in os.listdir("wiki-files/bits"):
        # check the object is a file and not folder
        if os.path.isfile(os.path.join("wiki-files/bits",fil)):
            # create a writer to write index
            writer = ix.writer()
            # open the bz2 file for reading
            bzfile = bz2.BZ2File(os.path.join("wiki-files/bits",fil))
            # get line by line
            for line in bzfile:
                # if "title" is found index it
                if re.search("<title>",line):
                    txt = line.strip().strip("<title>").strip("</")
                    utitle = unicode(txt, 'utf-8')
                    ufile = unicode(fil, 'utf-8')
                    writer.add_document(title=utitle, file_name=ufile)
            # commit once each file is done
            writer.commit()
            print fil+'-> Indexed'
    '''
