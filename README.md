# Karthika - A Offline Tamil Wiktionary
This code repository contains the source files of the software Karthika, which is a offline
Dictionary made using the Wiktionary data obtained from its XML dumps. The words and its meanings
are parsed from the dump and are indexed using the Whoosh Search Engine. There are two kinds of indexing to be done:
#### 1.Bulk Indexing
Creating the index of words and complete text associated with it - this results in large index size
of about a few hundred megabytes and indexing takes more than a hour time in a average machine. 
This is the currently employed method in the indexer.py and corresponding searching in searcher.py.

#### 2.Split Indexing
Splitting the large XML dump file into smaller files and indexing the word and the associated filename. In this method the index size is about 30-40 megabytes in size and the xml chunks equal to the size of the original XML file. The time taken is about 5 min for splitting the files and 10 min for indexing. The splitting can be done using the splitter.py file.

### Note
The current ouput is raw wiki markup text. Due to its unparseablity, raw text is being displayed. Steps are being taken to parse it and produce a readable content.

## Dependencies
### 1. Whoosh
The indexing and searching are carried out using the Whoosh Python Search Engine.
http://pypi.python.org/pypi/Whoosh/

### 2. wxPython
The GUI is written using the wxPython library
http://www.wxpython.org/

## How to use?
These instructions are for running from the source.
Before going down, download and install the dependencies mentioned above.

This following instruction is for the download of source code v0.2.0 from this repo:

1. Download the code version v0.2.0 from [here] (https://github.com/tecoholic/tawiktionary-offline/zipball/v0.2.0)
2. Unzip it in a suitable location to get the folder "tawiktionary-offline"
3. Download the latest wiktionary XML dump from http://dumps.wikimedia.org/tawiktionary/latest/tawiktionary-latest-pages-articles.xml.bz2
4. Create a directory inside the tawiktionary-offline folder named "wiki-files"
5. Move the XML dump file into the wiki-files folder
6. Run `python gui.py`
7. Select `File` -> `Split`, if you want to do Split Indexing (Recommended) or Go for step 9
8. Select `Index` and Choose `Split Indexing` and `Start Indexing`. Once the indexing is complete your dictionary is ready to use
9. Alternatively, if you want a fast response software, skip step 7 and goto `File` -> `Index` and select `Bulk Indexing' and hit 'Start Indexing`.But it would take over 1 full hour for indexing to finish.

Note:

1. The Splitting and Indexing is only needed for the first time. Next time on, just run `gui.py` and use the dictionary
2. As already stated the output is raw wiki-markup, just go through it and write a parser to print readable data, I would be glad to have a parser. :-P

## To Create a Standalone Application (.exe)
### Dependency
### py2exe
A standalone .exe application can be built from these files using py2exe. Download the suitable py2exe from http://www.py2exe.org

### How to?

1. Open the tawiktionary-offline folder and run `python setup.py py2exe`
2. Now open the newly created `dist` folder inside tha tawiktionary-offline folder and find gui.exe file. That is all you need. Take that file put it anywhere you like (even in other machines without Python installed)
3. Download the latest wiktionary XML dump from http://dumps.wikimedia.org/tawiktionary/latest/tawiktionary-latest-pages-articles.xml.bz2
4. Create a directory inside the tawiktionary-offline folder named "wiki-files"
5. Move the XML dump file into the wiki-files folder
6. Select `File` -> `Split`, if you want to do Split Indexing (Recommended) or Go for step 9
7. Select `Index` and Choose `Split Indexing` and `Start Indexing`. Once the indexing is complete your dictionary is ready to use
8. Alternatively, if you want a fast response software, skip step 7 and goto `File` -> `Index` and select `Bulk Indexing' and hit 'Start Indexing`. But it would take over 1 full hour for indexing to finish.
9. You can create a shortcut for this application anywhere you like (Desktop?) and run it from there.
