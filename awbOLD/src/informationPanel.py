import sys
import re
import urllib
import random as r
import time
import os
import thread
import httplib

from wxPython.wx import *
from wxPython.ogl import *
from wxPython.lib.dialogs import wxMultipleChoiceDialog

from globalConstants import *
import images

import zoomer as z


#----------------------------------------------------------------------
class InformationPanel(wxDividedShape):
    def __init__(self, width, height, canvas, information=None):
        wxDividedShape.__init__(self, width, height)
        if information is None:
                region = wxShapeRegion()
                region.SetText('no uniqueObjects')
                region.SetProportions(0.0, 0.2)
                region.SetFormatMode(FORMAT_CENTRE_HORIZ)
                self.AddRegion(region)

        else:
                print "information", information
                for key in information.iterkeys():
                        region = wxShapeRegion()
                        region.SetText(str(key)+":"+str(information[key]))
                        region.SetProportions(0.0, 0.2)
                        region.SetFormatMode(FORMAT_CENTRE_HORIZ)
                        self.AddRegion(region)
                self.SetRegionSizes()
                self.ReformatRegions(canvas)


    def ReformatRegions(self, canvas=None):
        rnum = 0
        if canvas is None:
            canvas = self.GetCanvas()
        dc = wxClientDC(canvas)  # used for measuring
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