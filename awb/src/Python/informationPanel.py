import sys
import re
import urllib
import random as r
import time
import os
import thread
import httplib

from wxPython.wx import *
from wxPython.lib.dialogs import wxMultipleChoiceDialog

from globalConstants import *
import images

import zoomer as z
import wx
import wx.lib.ogl as ogl

#----------------------------------------------------------------------
class InformationPanel(ogl.DividedShape):
    def __init__(self, width, height, canvas, information=None):
        ogl.DividedShape.__init__(self, width, height)
        if information is None:
                region = ogl.ShapeRegion()
                region.SetText('no uniqueObjects')
                region.SetProportions(0.0, 0.2)
                region.SetFormatMode(FORMAT_CENTRE_HORIZ)
                self.AddRegion(region)
        else:
                i = 0
                for key in information.iterkeys():
                        print "uniqueObjects:", key,":", information[key]
                        region = ogl.ShapeRegion()
                        region.SetText(str(key)+":"+str(information[key]))
                        region.SetProportions(0.0, 0.2)
                        region.SetFormatMode(FORMAT_CENTRE_HORIZ)
                        self.AddRegion(region)
                        i += 1
                        print 'region', "-", i, key,":", information[key]
                self.SetRegionSizes()
                self.ReformatRegions(canvas)


    def ReformatRegions(self, canvas=None):
        rnum = 0
        if canvas is None:
            canvas = self.GetCanvas()
        dc = wx.ClientDC(canvas)  # used for measuring
        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        self.base_OnSizingEndDragLeft(pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()

#----------------------------------------------------------------------