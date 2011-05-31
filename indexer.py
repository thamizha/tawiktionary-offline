#!/usr/bin/python

'''
In order to make the Dictionary searchable the wikipage titles should be indexed.

This indexer is based on the Whoosh search engine library.
'''
import os
import bz2
import re
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, STORED

class MySchema(SchemaClass):
    file_name = TEXT(stored=True)
    title = TEXT(stored=True)

if __name__ == "__main__":
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
