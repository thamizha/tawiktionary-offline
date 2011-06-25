#!/usr/bin/python

'''
This script would split the large .bz2 file into smaller .bz2 files.

The downloded wiktionary bz2 files are large in the order of MBs which would
inhibit fast searching, hence the files are split into smaller junks and
indexed using the indexer.py.
'''

import os
import bz2

import wx

def RunSplitter(event):
    '''The function gets the filename of wiktionary.xml.bz2 file as input and
    creates smallers chunks of it in a the diretory chunks.
    '''
    # Filename
    filename = 'wiki-files/tawiktionary-20110518-pages-articles.xml.bz2'
    # Check and create chunk diretory
    if not os.path.exists("chunks"):
        os.mkdir("chunks")
    # Counters
    pagecount = 0
    filecount = 1
    #open chunkfile in write mode
    chunkname = lambda filecount: os.path.join("chunks",
                                               "chunk-"+str(filecount)+
                                               ".xml.bz2")
    chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
    try:
        # Read line by line
        bzfile = bz2.BZ2File(filename)
    except Exception, ex:
        go = False
        msgdlg = wx.MessageDialog(None, str(ex),
                                  'Exception',
                                  wx.OK | wx.ICON_ERROR
                                  #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                  )
        msgdlg.ShowModal()
        msgdlg.Destroy()
    
    st = os.stat(filename)
    max = int(st.st_size/(1024*102.4))
    dlg = wx.ProgressDialog("Splitter",
                            "The large file is being split. Kindly Wait!",
                            maximum=max,
                            parent=None,
                            style=wx.PD_CAN_ABORT |
                            wx.PD_APP_MODAL |
                            wx.PD_ELAPSED_TIME |
                            #wx.PD_ESTIMATED_TIME|
                            wx.PD_REMAINING_TIME )
    go = True
    while go:
        for line in bzfile:
            chunkfile.write(line)
            # the </page> determines new wiki page
            if '</page>' in line:
                pagecount += 1
            if pagecount > 1999:
                #print chunkname() # For Debugging
                chunkfile.close()
                pagecount = 0 # RESET pagecount
                filecount += 1 # increment filename           
                chunkfile = bz2.BZ2File(chunkname(filecount), 'w')
                #update count here
                cnksize = 0
                cnkfiles = [fi for fi in os.listdir('chunks')
                            if os.path.isfile(os.path.join('chunks',fi))]
                for fi in cnkfiles:
                    cnksize += os.stat(os.path.join('chunks',fi)).st_size
                (go, skip) = dlg.Update(int(cnksize/(1024*102.4)))
        try:
            chunkfile.close()
        except:
            #print 'Files already close'
            pass
        go = False
        
        
    dlg.Destroy()

#------------------------------------------------------------------------------

    


if __name__ == '__main__':
    # When the script is self run
    # split_xml('wiki-files/tawiktionary-20110518-pages-articles.xml.bz2')
    print 'This file is not supposed to be run seperately!'
