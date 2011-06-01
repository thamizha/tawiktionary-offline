#!/usr/bin/python

'''
The text entered during the searching should be parsed into search objects for the Whoosh library.

This file recieves the text entered and parses into searchable objects and performs search operations.
'''
from whoosh import index
from whoosh.fields import *


ix = index.open_dir("indexdir")


from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("title", ix.schema).parse(u"ocean")
    results = searcher.search(query, limit=None)
    for result in results:
        print result
