import sys
import re
import os

from wxPython.wx import *
from wxPython.help import *

import images
import pickle

#---------------------------------------------------------------------------

DEPTH = '&depth=-1'
URLSEQ = ['LEADER', 'HOST', 'COLON_SEP','PORT','HACK','REMAINDER', 'DEPTH']
URLITEMS = {'LEADER':'http://',
    'HOST': None,
    'COLON_SEP':':',
    'PORT': None,
    'HACK':'/',
    #~ 'DOLLAR':'$',
    #~ 'AGENT':None,
    #~ 'REMAINDER':'/hierarchy?recurse=true&allRelationships=true&format=xml&Display=',
    #~ 'REMAINDER':'/agents?suffix=.&format=xml&Display=',
    'REMAINDER':'/agents?suffix=.&depth=',
    'DEPTH':'1',
    }
HOST_COMBOBOX_ID = 601
PORT_COMBOBOX_ID = 602
#~ AGENT_COMBOBOX_ID = 603
URL_COMBOBOX_ID = 604
DEPTH_COMBOBOX_ID = 605
OBJECT_STORE = 'awb.list.p'
class ProbeDlg(wxDialog):
    def OnSetFocus(self, evt):
        print "OnSetFocus"
        evt.Skip()
    def OnKillFocus(self, evt):
        print "OnKillFocus"
        evt.Skip()
    def GetBookmarkedData(self):
        try:
            self.URLcomponents = pickle.load(open(OBJECT_STORE))
            print self.URLcomponents
        except IOError, why:
            self.log.WriteText("IO Error %s" % why)
            self.URLcomponents = URLcomponents()
    def __init__(self, parent, ID, log, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        pre = wxPreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        self.parent = parent
        self.initParticles()
        self.log = log
        self.URLcomponents = URLcomponents()
        self.GetBookmarkedData()

 #~ ------------------------------
        urlLbl = wxStaticText(self, -1, "Host")
        default = "enter/select host"
        if len(self.URLcomponents.hosts) > 0 :
            default = self.URLcomponents.hosts[0]
            URLITEMS['HOST'] = default
        self.cbHosts = wxComboBox(self, HOST_COMBOBOX_ID, default, wxPoint(-1,-1), wxSize(90, -1),                             # wxPoint(90, 50), wxSize(95, -1),
                        self.URLcomponents.hosts, wxCB_DROPDOWN)

        EVT_TEXT(self, self.cbHosts.GetId(), self.EvtText)
        EVT_TEXT_ENTER(self, self.cbHosts.GetId(), self.EvtTextEnter)
        #~ EVT_CHAR(t1, self.EvtChar)
#~ ------------------------------
        portLbl = wxStaticText(self, -1, "Port")
        default = "enter/select port"
        if len(self.URLcomponents.ports) > 0 :
            default = self.URLcomponents.ports[0]
            URLITEMS['PORT'] = default
        self.cbPorts = wxComboBox(self, PORT_COMBOBOX_ID, default, wxPoint(-1,-1), wxSize(90, -1),                             # wxPoint(90, 50), wxSize(95, -1),
                        self.URLcomponents.ports, wxCB_DROPDOWN)

        EVT_TEXT(self, self.cbPorts.GetId(), self.EvtText)
        EVT_TEXT_ENTER(self, self.cbPorts.GetId(), self.EvtTextEnter)

#~ ------------------------------
        cbLbl = wxStaticText(self, -1, "Depth",  wxPoint(8, 10))

        default = ""
        if len(self.URLcomponents.depths) is 0: default = "1"
        else: default = self.URLcomponents.depths[0]

        cb = wxComboBox(self, DEPTH_COMBOBOX_ID , default, wxPoint(10, 50), wxSize(90, -1),
                        self.URLcomponents.urls, wxCB_DROPDOWN)
        EVT_COMBOBOX(self,DEPTH_COMBOBOX_ID , self.EvtComboBox)
        EVT_TEXT(self, DEPTH_COMBOBOX_ID , self.EvtText)
        EVT_TEXT_ENTER(self, DEPTH_COMBOBOX_ID , self.EvtTextEnter)
        EVT_SET_FOCUS(cb, self.OnSetFocus)
        EVT_KILL_FOCUS(cb, self.OnKillFocus)



        self.bg_bmp = images.getGridBGBitmap()
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        bOk = wxButton(self, wxID_OK, "OK")
        bOk.SetDefault()
        EVT_BUTTON(self, bOk.GetId(), self.OnOk)
        bCan = wxButton(self, wxID_CANCEL, "Cancel")
        EVT_BUTTON(self, bCan.GetId(), self.OnCancel)

        bsizer = wxBoxSizer(wxHORIZONTAL)
        bsizer.Add(bOk, 0, wxGROW|wxALL, 4)
        bsizer.Add(bCan, 0, wxGROW|wxALL, 4)

        sizer = wxFlexGridSizer(cols=3, hgap=6, vgap=6)
        sizer.AddMany([urlLbl, self.cbHosts, (0,0),
                        portLbl, self.cbPorts, (0,0),
                        #~ agentLbl, self.cbAgents, (0,0),
                        cbLbl, cb,  (0,0),
                        (0,0),bsizer,(0,0),
                        ])
        border = wxBoxSizer(wxVERTICAL)
        border.Add(sizer, 0, wxALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)
# ----------------------------------------------


    def initParticles(self):
        self.url = ""
        self.port = ""
        self.agent = ""
    def OnOk(self, evt):
        rtn = self.formURLStrings()
        if rtn is True:
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

    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        #~ data = cb.GetClientData(cb.GetSelection())
        #~ self.log.WriteText('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

    def EvtText(self, evt):
        #~ TODO would be neat to have number only verification on the port and depth fields
        #~ self.log.WriteText('EvtText: %s\n' % evt.GetString())
        if evt.GetId() == HOST_COMBOBOX_ID:URLITEMS['HOST'] = evt.GetString()
        if evt.GetId() == PORT_COMBOBOX_ID:URLITEMS['PORT'] = evt.GetString()
        if evt.GetId() == DEPTH_COMBOBOX_ID:URLITEMS['DEPTH'] = evt.GetString()
        #~ if evt.GetId() == AGENT_COMBOBOX_ID:URLITEMS['AGENT'] = evt.GetString()

    def EvtTextEnter(self, evt):
        self.log.WriteText('EvtTextEnter: %s, %s, %s\n' % (evt.GetString(), evt.GetEventObject(), evt.GetId()))
        obj = evt.GetEventObject()
        self.log.WriteText("EvtTextEnter:%s\n %s, %s" % (dir(obj),obj.GetLabel(), obj.GetName()))
    def EvtChar(self, event):
        self.log.WriteText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def formURLStrings(self):
        done = True
        for i in URLSEQ:
            if URLITEMS[i] is None or URLITEMS[i] is "":
                dlg = wxMessageDialog(self.parent, 'Need a value for '+str(i),
                          'No!', wxOK | wxICON_INFORMATION)
                          #wxYES_NO | wxNO_DEFAULT | wxCANCEL | wxICON_INFORMATION)
                dlg.ShowModal()
                done = False

        if done:
            s = ""
            for i in URLSEQ:
                s += URLITEMS[i]
            self.log.WriteText("formURLStrings:%s" % (s))

            if URLITEMS['HOST'] not in self.URLcomponents.hosts: self.URLcomponents.hosts.append( str(URLITEMS['HOST']) )
            if URLITEMS['PORT'] not in self.URLcomponents.ports: self.URLcomponents.ports.append( str(URLITEMS['PORT']) )
            if URLITEMS['DEPTH'] not in self.URLcomponents.depths: self.URLcomponents.depths.append( str(URLITEMS['DEPTH']) )
            pickle.dump(self.URLcomponents,open(OBJECT_STORE,'w'))
            self.parent.URL = s
            self.parent.HOST =str(URLITEMS['HOST'])
            self.parent.PORT =str(URLITEMS['PORT'])

        return done
class URLcomponents:
    def __init__(self):
        self.hosts = []
        self.ports = []
        #~ self.agents = []
        self.urls = []
        self.depths = []
    def __str__(self):
        s0 = "URL COMPONENTS\n"
        s1 = "Hosts\n"
        for i in self.hosts: s1 += str(i)+"\n"
        s1 += '\n'

        s2 = "Ports\n"
        for i in self.ports: s2 += str(i)+"\n"
        s2 += '\n'

        #~ s3 = "Agents\n"
        #~ for i in self.agents: s3 += str(i)+"\n"
        #~ s3 += '\n'

        return s0+s1 + s2

#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = URLDlg(nb, log)
    return win

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])