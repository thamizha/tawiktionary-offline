# -*- coding: utf-8 -*-
'''
The gui.py script creates the Graphical User Interface for the wikitionary
to enter the query input and meaning output.
'''

import os
import wx

from parser import *

class MainWindow(wx.Frame):
    '''  This class defines the basis of the GUI of the entire application '''
    def __init__(self,parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(300,-1))

        #Widgets
        # 1. textbox 2. button 3. textarea
        self.SearchBox = wx.TextCtrl(self, value=u"தேடு சொல்லை தட்டச்சு செய்யவும்")
        self.SearchButton = wx.Button(self, label=u"தேடு")
        self.ResultBox = wx.TextCtrl(self, size=(300,-1), style=wx.TE_MULTILINE)

        #Events
        self.Bind(wx.EVT_BUTTON, self.SearchIt,self.SearchButton)

        #sizers for placemnt
        self.hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hsizer.Add(self.SearchBox, 1, wx.EXPAND)
        self.hsizer.Add(self.SearchButton, 0, wx.EXPAND)

        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.hsizer, 0, wx.EXPAND)
        self.vsizer.Add(self.ResultBox, 1, wx.GROW)

        #layout sizers
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        self.vsizer.Fit(self)

        self.Show(True)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainWindow(None, "taWiktionary - Offline")
    app.MainLoop()

    
