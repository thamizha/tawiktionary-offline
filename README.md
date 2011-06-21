# tawiktionary-offline
This code repository contains the source files of the software Karthika, which is a offline
Dictionary made using the Wiktionary data obtained from its XML dumps. The words and its meanings
are parsed from the dump and are indexed using the Whoosh Search Engine. There are two kinds of 
indexing to be done:
* creating the index of words and complete text associated with it - this results in large index size
of about a few hundred megabytes and indexing takes more than a hour time in a average machine. 
This is the currently employed method in the indexer.py and corresponding searching in searcher.py.

* splitting the large XML dump file into smaller files and indexing the word and the associated filename.
In this method the index size is about 30-40 megabytes in size and the xml chunks equal to the size of the
original XML file. The time taken is about 5 min for splitting the files and 10 min for indexing. The splitting
can be done using the splitter.py file.

### Note
1. The code for the second type of searching is being written and the way to include both types in the final software
is being worked out.
2. The current ouput is raw wiki markup text. Due to its unparseablity, raw text is being displayed. Steps are being 
taken to parse it and produce a readable content.

## Dependencies
### 1.Whoosh
The indexing and searching are caaried out using the Whoosh Python Search Engine.
http://pypi.python.org/pypi/Whoosh/

### 2.wxPython
The GUI is written using the wxPython library
http://www.wxpython.org/

## How to use?
Before going down, download and install the dependencies mentioned above.

This following instruction is for the download of source code v0.1.0 from this repo:
1. Download the code version v0.1.0 from here
2. Unzip it in a suitable location to get the folder "tawiktionary-offline"
3. Download the latest wiktionary XML dump from http://dumps.wikimedia.org/tawiktionary/latest/tawiktionary-latest-pages-articles.xml.bz2
4. Create a directory inside the tawiktionary-offline folder named "wiki-files"
5. Move the XML dump file into the wiki-files folder
6. Run `python indexer.py` and wait for the indexing to complete (you will see the words being indexed in the terminal)
7. Run `python gui.py` and use the dictionary.

Note: As already stated the output is raw wiki-markup, just go through it and write a parser to print readable data,
I would be glad to have a parser. :-P