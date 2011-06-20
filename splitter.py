#!/usr/bin/python

'''
The downloded wiktionary bz2 files are large in the order of MBs which would inhibit fast searching,
hence the files are split into smaller junks and indexed using the indexer.py.

This script would split the large .bz2 file into smaller .bz2 files.

Note: Make sure that page data isn't split between the smaller bits.
'''

#-------------------------------------------------------------------------
'''
Steps
-----
1. Set pages_per_file = 2000
2. Open the large .xml.bz2 file
3. parse the large file as such without decompression
4. Read each page block and into a file buffer until count is 1000
    or end of file
5. Write the buffer as a file
6. Repeat 4&5 until end of file

Pseudo code - for splitting
---------------------------
open input file
open output file 1
count = 0
for each line in file:
    write to output file
    count = count + 1
    if count > maxlines:
         close output file
         open next output file
         count = 0


'''
#-------------------------------------------------------------------------
import os
import bz2

def split_xml(filename):
    ''' The function gets the filename of wiktionary.xml.bz2 file as  input and creates
    smallers chunks of it in a the diretory chunks
    '''
    # Check and create chunk diretory
    if not os.path.exists("chunks"):
        os.mkdir("chunks")
    # Counters
    pagecount = 0
    filecount = 1
    #open chunkfile in write mode
    chunkname = lambda filecount: os.path.join("chunks","chunk-"+str(filecount)+".xml.bz2")
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

#-------------------------------------------------------------------------
if __name__ == '__main__':
    # When the script is self run
    split_xml('wiki-files/tawiktionary-20110518-pages-articles.xml.bz2')
