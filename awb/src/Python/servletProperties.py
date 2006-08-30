import sys
# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: servletProperties.py,v 1.4 2006-08-30 20:45:57 damoore Exp $
#  <copyright>
#  Copyright 2002 BBN Technologies, LLC
#  under sponsorship of the Defense Advanced Research Projects Agency (DARPA).
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the Cougaar Open Source License as published by
#  DARPA on the Cougaar Open Source Website (www.cougaar.org).
#
#  THE COUGAAR SOFTWARE AND ANY DERIVATIVE SUPPLIED BY LICENSOR IS
#  PROVIDED 'AS IS' WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS OR
#  IMPLIED, INCLUDING (BUT NOT LIMITED TO) ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND WITHOUT
#  ANY WARRANTIES AS TO NON-INFRINGEMENT.  IN NO EVENT SHALL COPYRIGHT
#  HOLDER BE LIABLE FOR ANY DIRECT, SPECIAL, INDIRECT OR CONSEQUENTIAL
#  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE OF DATA OR PROFITS,
#  TORTIOUS CONDUCT, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
#  PERFORMANCE OF THE COUGAAR SOFTWARE.
# </copyright>
#

import wx
import wx.lib.ogl as ogl
#~from societyVisualModel import *
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