import sys


from wxPython.wx import *
from wxPython.ogl import *
from societyVisualModel import *
#~ from societyController import *

class ServletProperties(wxDialog):
    def __init__(self, parent, ID, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        #~ TheSociety.getFacetDepth(facetinfo.GetClientData())
        pre = wxPreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        
        startXposition = 35
        startYposition = 330
        bOk = wxButton(self, wxID_OK, "OK", wxPoint(startXposition, startYposition), wxSize(100, 30))
        #~ EVT_BUTTON(self, b.GetId(), self.OnPressOk)
        bOk.SetDefault()

        startXposition = 165
        startYposition = 330
        bCan = wxButton(self, wxID_CANCEL, "Cancel", wxPoint(startXposition, startYposition), wxSize(100, 30))

        
    def OnPressOk(self, event):
        print "You clicked OK" 