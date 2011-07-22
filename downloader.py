#!/usr/bin/python

'''
Wiktionary dump data can be downloaded from the wikimedia site.

This script is to automatically look for the latest dump and dowmload it.
'''
import os
import bz2
import re
import codecs

import wx
import wx.lib.delayedresult as delayedresult
import urllib2


class DownloadDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)
        self.txt = wx.StaticText(self, -1, "Module Under development :)",
                                 style = wx.ALIGN_LEFT)
        # the sizers
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.vsizer.Add(self.txt, 0,
                        wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM,
                        border=10)
        # layout sizers
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(1)
        self.vsizer.Fit(self)
        


if __name__ == '__main__':
    print 'This file is not supposed to be run directly.'
