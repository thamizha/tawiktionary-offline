#!/usr/bin/python
# -*- encoding: UTF-8 -*-
'''
The text entered during the searching should be parsed into search objects for the Whoosh library.

This file recieves the text entered and parses into searchable objects and performs search operations.
'''
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser

def search_for(text):
    ''' This function gets the search query string and returns the list of
    dictionary of the hits (file_name and titles) '''
    ix = index.open_dir("indexdir")
    res = []
    with ix.searcher() as searcher:
        query = QueryParser("title", ix.schema).parse(unicode(text))
        results = searcher.search(query, limit=None, sortedby='file_name')
        for result in results:
            temp = {}
            temp['file_name'] = result['file_name']
            temp['title'] = result['title']
            res.append(temp)
    return res

if __name__ == "__main__":
    searchterm = raw_input("Enter the Search Term: ")
    r = search_for(searchterm)
    for rs in r:
        print unicode(rs['title'])

