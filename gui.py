# -*- coding: utf-8 -*-
'''
The gui.py script creates the Graphical User Interface for the wikitionary
to enter the query input and meaning output.
'''

import os

import wx
import wx.richtext
from wx.lib.wordwrap import wordwrap

from searcher import *
from splitter import split_xml
from indexer import create_index

class MainWindow(wx.Frame):
    '''  This class defines the basis of the GUI of the entire application '''
    def __init__(self,parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(400,-1))

        # Menu
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_FILE1, "&Split",
                        "Create smaller chunks from large XML file")
        filemenu.Append(wx.ID_FILE2, "&Index",
                        "Create the index of words and meanings for searching")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "&Exit\tAlt+F4", "Exit the program")

        helpmenu = wx.Menu()
        helpmenu.Append(wx.ID_ABOUT, "&About", "About the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(helpmenu, "&Help")
      

        self.SetMenuBar(menuBar)

        # Status bar
        self.CreateStatusBar()
        self.SetStatusText('Created By Arunmozhi')

        #Widgets
        # 1. textbox 2. button 3. textarea 4.Listbox
        self.SearchBox = wx.SearchCtrl(self, size=(200,-1),
                                       style=wx.TE_PROCESS_ENTER)
        self.ResultBox = wx.richtext.RichTextCtrl(self, size=(300,500),
                                                  style=wx.TE_MULTILINE|
                                                  wx.TE_READONLY)
        self.WordList = wx.ListBox(self, size=(160,-1))

        # Set values
        self.SearchBox.ShowCancelButton(True)
        self.ResultBox.BeginFontSize(11)
                
        #Events
        self.Bind(wx.EVT_TEXT_ENTER, self.SearchIt,self.SearchBox)
        self.Bind(wx.EVT_LISTBOX, self.ShowMeaning, self.WordList)
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.ShowAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.RunSplitter, id=wx.ID_FILE1)
        self.Bind(wx.EVT_MENU, self.RunIndexer, id=wx.ID_FILE2)
        
        #sizers for placemnt
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.Add(self.SearchBox, 1, wx.EXPAND)

        self.bsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bsizer.Add(self.WordList, 0, wx.GROW)
        self.bsizer.Add(self.ResultBox, 1, wx.GROW)
        
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.hsizer, 0, wx.EXPAND)
        self.vsizer.Add(self.bsizer, 1, wx.EXPAND)
        
        #layout sizers
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        self.vsizer.Fit(self)

        self.Show(True)

    def SearchIt(self, e):
        ''' The Searchit function gets the input from SearchBox and lists
        the Word matches in the ListBox '''
        text = self.SearchBox.GetValue()
        self.Matches = search_for(text)
        self.WordList.Set([r['word'] for r in self.Matches])
        
    def ShowMeaning(self, event):
        ''' The ShowMeaning function prints the meaning for the word selected
        for in the ListBox '''
        opted = self.Matches[event.GetSelection()]
        meaning_text = get_markup(opted['word'],opted['meaning'])
        self.ResultBox.SetValue('')
        self.ResultBox.WriteText(meaning_text)

    def ExitApp(self, e):
        ''' ExitApp closes the application '''
        self.Close(True)

    def ShowAbout(self, e):
        ''' ShowAbout function displays the About information of the application
        '''
        info = wx.AboutDialogInfo()
        info.Name = "Karthika"
        info.Version = "0.1.0"
        info.Copyright = "(c) Arunmozhi 2011"
        info.Description = wordwrap("Kathika is a offline Dictionary build "
                                    "using the Wiktionary data of the WikiMedia"
                                    "Foundation. It is build using Python with"
                                    "wxPython for the GUI. The underlying data "
                                    "is extracted from the XML dumps of the "
                                    "Wiktionary site.The indexing and searching"
                                    "is using the Whoosh Search Engine.",
                                    400, wx.ClientDC(self))
        info.WebSite = ("https://github.com/tecoholic/tawiktionary-offline",
                        "Project GitHub Page")
        info.Developers = ["Arunmozhi"]
        info.License = wordwrap("No License has been decided yet. You are free"
                                "to modify and distribute the program as per"
                                "your needs without any kind of attribution of"
                                "credits whatsoever for the original developer."
                                "But requested to maintain the resulting "
                                "software name as Karthika.",
                                400, wx.ClientDC(self))
        wx.AboutBox(info)

    def RunSplitter(self, event):
        ''' The RunSplitter function runs the splitter.py function '''
        split_xml('wiki-files/tawiktionary-latest-pages-articles.xml.bz2')

    def RunIndexer(self, event):
        ''' The RunIndexer function runs indexer.py function '''
        create_index(2)
        

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, "Karthika 0.1 - A Offline taWiktionary")
    app.MainLoop()

    
