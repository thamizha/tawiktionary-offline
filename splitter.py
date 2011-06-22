#!/usr/bin/python

'''
This script would split the large .bz2 file into smaller .bz2 files.

The downloded wiktionary bz2 files are large in the order of MBs which would
inhibit fast searching, hence the files are split into smaller junks and
indexed using the indexer.py.
'''

import os
import bz2

def split_xml(filename):
    ''' The function gets the filename of wiktionary.xml.bz2 file as  input
    and creates smallers chunks of it in a the diretory chunks
    '''
    # Check and create chunk diretory
    if not os.path.exists("chunks"):
        os.mkdir("chunks")
    # Counters
    pagecount = 0
    filecount = 1
    #open chunkfile in write mode
    chunkname = lambda filecount: os.path.join("chunks",
                                               "chunk-"+str(filecount)+
                                               ".xml.bz2")
    chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
    # Read line by line
    bzfile = bz2.BZ2File(filename)
    for line in bzfile:
        chunkfile.write(line)
        # the </page> determines new wiki page
        if '</page>' in line:
            pagecount += 1
        if pagecount > 1999:
            #print chunkname() # For Debugging
            chunkfile.close()
            pagecount = 0 # RESET pagecount
            filecount += 1 # increment filename           
            chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
    try:
        chunkfile.close()
    except:
        print 'Files already close'


if __name__ == '__main__':
    # When the script is self run
    split_xml('wiki-files/tawiktionary-20110518-pages-articles.xml.bz2')
