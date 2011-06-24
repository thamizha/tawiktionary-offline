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
import wx.lib.delayedresult as delayedresult
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

        log_text = ("Note:\n1. Bulk Indexing takes over 1 Hour to complete and "
                    +"choose it only if you have patience.\n2. Split indexing"
                    +"is faster and only takes about 15 min. But make sure you"
                    +" have run File -> Split before running split indexing.")

        self.txt = wx.StaticText(self, -1, "Choose the method of indexing",
                                 style=wx.ALIGN_LEFT)
        self.bulkrb = wx.RadioButton(self, -1, 'Bulk Indexing', 
                                     style=wx.RB_GROUP)
        self.splitrb = wx.RadioButton(self, -1,  'Split Indexing')
        self.indbtn = wx.Button(self, -1, "Start Indexing")
        self.log = wx.TextCtrl(self, 100, log_text, size=(350,200),
                               style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.txt, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, border=10)
        self.vsizer.Add(self.bulkrb, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, border=10)
        self.vsizer.Add(self.splitrb, 0,
                        wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT|wx.BOTTOM, border=10)
        self.vsizer.Add(self.log, 0, wx.EXPAND|wx.RIGHT|wx.LEFT|wx.BOTTOM,
                        border=10)
        self.vsizer.Add(self.indbtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM,
                        border = 10)

        #binders
        self.Bind(wx.EVT_BUTTON, self.start_indexing, self.indbtn)
        
        #layout sizers
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        self.vsizer.Fit(self)

        #event globals
        self.jobID = 0
        self.abortEvent = delayedresult.AbortEvent()
        self.Bind(wx.EVT_CLOSE, self.handleClose)

    def handleClose(self, event):
        ''' Close the running threads when dialog is closed '''
        self.abortEvent.set()
        self.Destroy()

    def start_indexing(self, event):
        ''' This function is called when the "Start Indexing" button is pressed.
        '''
        self.indbtn.Enable(False)
        self.abortEvent.clear()
        self.jobID += 1

        self.log.SetValue("Starting indexing process:")
        if self.bulkrb.GetValue():
            delayedresult.startWorker(self._resultConsumer,
                                      self.create_bulk_index,
                                      wargs=(self.jobID,self.abortEvent),
                                      jobID=self.jobID)
        elif self.splitrb.GetValue():
            delayedresult.startWorker(self._resultConsumer,
                                      self.create_split_index,
                                      wargs=(self.jobID,self.abortEvent),
                                      jobID=self.jobID)

    def _resultConsumer(self, delayedResult):
        ''' Job is finished '''
        jobID = delayedResult.getJobID()
        assert jobID == self.jobID
        try:
            result = delayedResult.get()
        except Exception, exc:
            self.log.AppendText("\nException: %s"% (exc))

        # Output result
        self.log.AppendText("Indexing complete.You can now use the dictionary.")



    def dump_file(self):
        ''' This function searches the directory and returns the latest xml dump
        file.
        '''
        files = [fil for fil in os.listdir('wiki-files')
                 if os.path.isfile(os.path.join('wiki-files',fil))]
        #print os.listdir('wiki-files')
        #print files
        return files[0]

    def create_split_index(self, jobID, abortEvent):
        ''' This function creates the index for the Split files in the chunks
        directory. Split Index -> The files are split into smaller chunks and
        the words and the filenames which contain them are indexed
        '''
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        # create a indexer object
        ix = index.create_in("indexdir", MySchema)
        ix = index.open_dir("indexdir")
        
        # read all the file in the bits folder
        if len(os.listdir("chunks")) < 1:
            self.log.AppendText('Error! Run Splitter first!')
        # check if abortEvent is set
        while not abortEvent():
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
                            self.log.AppendText(utitle+'\n')
                    # commit once each file is done
                    self.log.AppendText( '\n\n'+fil+'-> Indexed' )
                    writer.commit()
        return jobID
                

    def create_bulk_index(self, jobID, abortEvent):
        ''' Bulk Index -> The big and complete XML file is parsed and index of
        both word and he corresponding content of wikipage called the meaning.
        '''
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
        bzfile = bz2.BZ2File(os.path.join('wiki-files',self.dump_file()))
        #f = codecs.open('list.txt', encoding='utf-8', mode='w')
        # create a writer to write index
        writer = ix.writer()
        # check if abortEvent is set
        while not abortEvent():
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
                    self.log.AppendText( title+'\n' )
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
                self.log.AppendText( "\n\nFile commited !!" )
        bzfile.close()
        #f.close()
        return jobID

if __name__ == "__main__":
    print 'This file is not supposed to be run separately!'
