import sys


import wx
import wx.lib.ogl as ogl
from societyVisualModel import *
#~ from societyController import *

class ServletProperties(wx.Dialog):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        #~ TheSociety.getFacetDepth(facetinfo.GetClientData())
        # wx 2.5 Note: is this still required, 
        # AWB note: is this still used? Referenced in:
        # agentController.py
        # societyController.py

        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        
        startXposition = 35
        startYposition = 330
        bOk = wx.Button(self, wx.ID_OK, "OK", wx.Point(startXposition, startYposition), wx.Size(100, 30))
        self.Bind(wx.EVT_BUTTON, self.OnPressOk)
        bOk.SetDefault()

        startXposition = 165
        startYposition = 330
        bCan = wx.Button(self, wx.ID_CANCEL, "Cancel", wx.Point(startXposition, startYposition), wx.Size(100, 30))

        
    def OnPressOk(self, event):
        print "You clicked OK" 