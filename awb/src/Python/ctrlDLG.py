import sys
import re
import os

from wxPython.wx import *
from wxPython.help import *

import images
import pickle

#---------------------------------------------------------------------------


NODE_TXTCTRL_ID = 701

class CtrlDlg(wxDialog):
    def OnSetFocus(self, evt):
        print "OnSetFocus"
        evt.Skip()
    def OnKillFocus(self, evt):
        print "OnKillFocus"
        evt.Skip()

    def __init__(self, parent, ID, log, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        pre = wxPreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        self.parent = parent
        self.log = log

 #~ ------------------------------
        nodeLbl = wxStaticText(self, -1, "Node")
        default = "enter/select node to run"
        self.nodeTxtCtrl = wxTextCtrl(self, NODE_TXTCTRL_ID, default, size=(300, -1), style=wxTE_PROCESS_ENTER )

        EVT_TEXT_ENTER(self, self.nodeTxtCtrl.GetId(), self.OnOk)

        self.bg_bmp = images.getGridBGBitmap()
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        #---------------------------------
        # button fixtures
        bBrowseID = wxNewId()
        bBrowse = wxButton(self, bBrowseID, "browse")
        bBrowse.SetBackgroundColour("BLACK")
        bBrowse.SetForegroundColour("WHITE")

        EVT_BUTTON(self, bBrowse.GetId(), self.OnBrowse)

        bOk = wxButton(self, wxID_OK, "OK")
        bOk.SetDefault()
        EVT_BUTTON(self, bOk.GetId(), self.OnOk)
        bCan = wxButton(self, wxID_CANCEL, "Cancel")
        EVT_BUTTON(self, bCan.GetId(), self.OnCancel)

        bsizer = wxBoxSizer(wxHORIZONTAL)
        bsizer.Add(bBrowse, 0, wxGROW|wxALL, 4)
        bsizer.Add(bOk, 0, wxGROW|wxALL, 4)
        bsizer.Add(bCan, 0, wxGROW|wxALL, 4)

        sizer = wxFlexGridSizer(cols=3, hgap=6, vgap=6)
        sizer.AddMany([nodeLbl, self.nodeTxtCtrl, (0,0),
                        (0,0),bsizer,(0,0),])
        border = wxBoxSizer(wxVERTICAL)
        border.Add(sizer, 0, wxALL, 25)



        self.SetSizer(border)
        self.SetAutoLayout(True)
# ----------------------------------------------


    def OnBrowse(self, evt):
        fileDialog = wxFileDialog(self, message="Choose a node xml file", wildcard = "*.xml", style=wxOPEN  )
        if fileDialog.ShowModal() == wxID_OK:
           self.nodeTxtCtrl.SetValue( fileDialog.GetPath())
        fileDialog.Destroy()

    def OnOk(self, evt):
        self.log.WriteText('OnOk: %s, %s\n' % (self.nodeTxtCtrl.GetValue(),  evt.GetId()))
        self.parent.NODE = self.nodeTxtCtrl.GetValue()
        self.SetReturnCode(wxID_OK)
        self.Destroy()


    def OnCancel(self, evt):
        self.SetReturnCode(wxID_CANCEL)
        self.Destroy()
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
          dc = wxClientDC(self.GetClientWindow())

        # tile the background bitmap
        sz = self.GetClientSize()
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        x = 0
        while x < sz.width:
            y = 0
            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h
            x = x + w


#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = URLDlg(nb, log)
    return win

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])