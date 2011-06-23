#!/usr/bin/python

'''
In order to make the Dictionary searchable the wikipage titles should be indexed.

This indexer is based on the Whoosh search engine library.
'''

import os
import bz2
import re
import codecs

import wx
import BeautifulSoup
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, STORED

class MySchema(SchemaClass):
    word = TEXT(stored=True)
    meaning = TEXT(stored=True)
    
class IndexDialog(wx.Dialog):
    ''' This class defines the dialog box to be shown for carrying out Indexing
    '''
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)

        self.txt = wx.StaticText(self, -1, "Choose the method of indexing",
                                 style=wx.ALIGN_LEFT)
        self.bulkrb = wx.RadioButton(self, -1, 'Bulk Indexing', 
                                     style=wx.RB_GROUP)
        self.splitrb = wx.RadioButton(self, -1,  'Split Indexing')
        self.gauge = wx.Gauge(self, -1, 100, size=(250,25))
        self.indbtn = wx.Button(self, wx.ID_APPLY, "Start Indexing")
        self.timer = wx.Timer(self)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.txt, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, border=10)
        self.vsizer.Add(self.bulkrb, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, border=10)
        self.vsizer.Add(self.splitrb, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.BOTTOM, border=10)
        self.vsizer.Add(self.gauge, 0, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM,
                        border=10)
        self.vsizer.Add(self.indbtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM,
                        border = 10)

        #binders
        self.Bind(wx.EVT_BUTTON, self.RunIndexer, id=wx.ID_APPLY)
        self.Bind(wx.EVT_TIMER, self.TimerHandler)
        
        #layout sizers
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        self.vsizer.Fit(self)

    def __del__(self):
        self.timer.Stop()

    def TimerHandler(self, event):
        self.gauge.Pulse()

    def RunIndexer(self, event):
        ''' This function runs the indexer script '''
        self.timer.Start(100)
        if self.bulkrb.GetValue():
            create_index(1)
        elif self.splitrb.GetValue():
            create_index(2)

    
def dump_file():
    ''' This function searches the directory and returns the latest xml dump file'''
    files = [fil for fil in os.listdir('wiki-files') if os.path.isfile(os.path.join('wiki-files',fil))]
    #print os.listdir('wiki-files')
    print files
    return files[0]

def create_index(mode):
    ''' The create_index function is used to create the index of words for the Wiktionary. The
    function operates in two modes.\n\nMode '1':\nBulk Index -> The big and complete XML file
    is parsed and index of both word and he corresponding content of wikipage called the meaning.
    \n\nMode '2':\nSplit Index -> The files are split into smaller chunks and the words and the
    filenames which contain them are indexed
    '''
    try:
        mode = int(mode)
    except:
        return 'Error! Input correct mode'
    
    # check wether a index exists
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    # create a indexer object
    ix = index.create_in("indexdir", MySchema)
    ix = index.open_dir("indexdir")
    
    if mode == 1: # Bulk Index
        # Some function globals
        page_count = 0
        writ = False
        xmlstr = ''
        #Open the dump file
        bzfile = bz2.BZ2File(os.path.join('wiki-files',dump_file()))
        #f = codecs.open('list.txt', encoding='utf-8', mode='w')
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
                #f.write(title+'\n')
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
        except:
            print "File commited already"
        bzfile.close()
        #f.close()
    
    elif mode == 2: # Split Index
        # read all the file in the bits folder
        if len(os.listdir("chunks")) < 1:
            return 'Error! Run Splitter first!'
        for fil in os.listdir("chunks"):
            # check the object is a file and not folder
            if os.path.isfile(os.path.join("chunks",fil)):
                # create a writer to write index
                writer = ix.writer()
                # open the bz2 file for reading
                bzfile = bz2.BZ2File(os.path.join("chunks",fil))
                # get line by line
                for line in bzfile:
                    # if "title" is found index it
                    if "<title>" in line:
                        soup = BeautifulSoup.BeautifulSoup(line)
                        utitle = soup.find('title').text
                        ufile = unicode(fil, 'utf-8')
                        writer.add_document(word=utitle, meaning=ufile)
                # commit once each file is done
                writer.commit()
                print fil+'-> Indexed'

if __name__ == "__main__":
    create_index(raw_input("Enter your option [1. bulk index 2. split index]: "))
