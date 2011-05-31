#!/usr/bin/python

'''
The downloded wiktionary bz2 files are large in the order of MBs which would inhibit fast searching,
hence the files are split into smaller junks and indexed using the indexer.py.

This script would split the large .bz2 file into smaller .bz2 files.

Note: Make sure that page data isn't split between the smaller bits.
'''
