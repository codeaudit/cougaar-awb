# CONVERTED2DOT5 = TRUE

import sys
import re
import os

import wx
from wxPython.help import *

import images
import pickle

#---------------------------------------------------------------------------
#~ URLSEQ = ['LEADER', 'HOST', 'COLON_SEP','PORT','HACK','DOLLAR','AGENT', 'REMAINDER']
URLSEQ = ['LEADER', 'HOST', 'COLON_SEP','PORT','HACK','REMAINDER']
URLITEMS = {'LEADER':'http://',
    'HOST': None,
    'COLON_SEP':':',
    'PORT': None,
    'HACK':'/',
    #~ 'DOLLAR':'$',
    #~ 'AGENT':None,
    #~ 'REMAINDER':'/hierarchy?recurse=true&allRelationships=true&format=xml&Display=',
    'REMAINDER':'/agents?suffix=.&format=xml&Display=',
    }
HOST_COMBOBOX_ID = 601
PORT_COMBOBOX_ID = 602
#~ AGENT_COMBOBOX_ID = 603
URL_COMBOBOX_ID = 604
OBJECT_STORE = 'awb.list.p'
class CECOMDlg(wx.Dialog):
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
    def __init__(self, parent, ID, log, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        self.parent = parent
        self.initParticles()
        self.log = log
        self.URLcomponents = URLcomponents()
        self.GetBookmarkedData()

 #~ ------------------------------
        urlLbl = wx.StaticText(self, -1, "Host")
        default = "enter/select host"
        if len(self.URLcomponents.hosts) > 0 :
            default = self.URLcomponents.hosts[0]
            URLITEMS['HOST'] = default
        self.cbHosts = wx.ComboBox(self, HOST_COMBOBOX_ID, default, wx.Point(-1,-1), wx.Size(90, -1),                             # wx.Point(90, 50), wx.Size(95, -1),
                        self.URLcomponents.hosts, wx.CB_DROPDOWN)

        wx.EVT_TEXT(self, self.cbHosts.GetId(), self.EvtText)
        wx.EVT_TEXT_ENTER(self, self.cbHosts.GetId(), self.EvtTextEnter)
        #~ wx.EVT_CHAR(t1, self.EvtChar)
#~ ------------------------------
        portLbl = wx.StaticText(self, -1, "Port")
        default = "enter/select port"
        if len(self.URLcomponents.ports) > 0 :
            default = self.URLcomponents.ports[0]
            URLITEMS['PORT'] = default
        self.cbPorts = wx.ComboBox(self, PORT_COMBOBOX_ID, default, wx.Point(-1,-1), wx.Size(90, -1),                             # wx.Point(90, 50), wx.Size(95, -1),
                        self.URLcomponents.ports, wx.CB_DROPDOWN)

        wx.EVT_TEXT(self, self.cbPorts.GetId(), self.EvtText)
        wx.EVT_TEXT_ENTER(self, self.cbPorts.GetId(), self.EvtTextEnter)
#~ ------------------------------
        #~ agentLbl = wx.StaticText(self, -1, "Agent")
        #~ default = "enter/select agent"
        #~ if len(self.URLcomponents.agents) > 0 :
            #~ default = self.URLcomponents.agents[0]
            #~ URLITEMS['AGENT'] = default

        #~ self.cbAgents = wx.ComboBox(self, AGENT_COMBOBOX_ID, default, wx.Point(-1,-1), wx.Size(90, -1),                             # wx.Point(90, 50), wx.Size(95, -1),
                        #~ self.URLcomponents.agents, wx.CB_DROPDOWN)

        #~ wx.EVT_TEXT(self, self.cbAgents .GetId(), self.EvtText)
        #~ wx.EVT_TEXT_ENTER(self, self.cbAgents .GetId(), self.EvtTextEnter)

#~ ------------------------------
        cbLbl = wx.StaticText(self, -1, "UL Heirarchy Servlet",  wx.Point(8, 10))

        default = ""
        if len(self.URLcomponents.urls) is 0: default = "No URLs Bookmarked"
        else: default = self.urlcomponents.urls[0]

        cb = wx.ComboBox(self, URL_COMBOBOX_ID , default, wx.Point(10, 50), wx.Size(300, -1),
                        self.URLcomponents.urls, wx.CB_DROPDOWN)
        wx.EVT_COMBOBOX(self,URL_COMBOBOX_ID , self.EvtComboBox)
        wx.EVT_TEXT(self, URL_COMBOBOX_ID , self.EvtText)
        wx.EVT_TEXT_ENTER(self, URL_COMBOBOX_ID , self.EvtTextEnter)
        wx.EVT_SET_FOCUS(cb, self.OnSetFocus)
        wx.EVT_KILL_FOCUS(cb, self.OnKillFocus)
#~ ------------------------------



        self.bg_bmp = images.getGridBGBitmap()
        wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

        bOk = wx.Button(self, wx.ID_OK, "OK")
        bOk.SetDefault()
        wx.EVT_BUTTON(self, bOk.GetId(), self.OnOk)
        bCan = wx.Button(self, wx.ID_CANCEL, "Cancel")
        wx.EVT_BUTTON(self, bCan.GetId(), self.OnCancel)

        bsizer = wx.BoxSizer(wx.HORIZONTAL)
        bsizer.Add(bOk, 0, wx.GROW|wx.ALL, 4)
        bsizer.Add(bCan, 0, wx.GROW|wx.ALL, 4)

        sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
        sizer.AddMany([urlLbl, self.cbHosts, (0,0),
                        portLbl, self.cbPorts, (0,0),
                        #~ agentLbl, self.cbAgents, (0,0),
                        cbLbl, cb,  (0,0),
                        (0,0),bsizer,(0,0),
                        ])
        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(sizer, 0, wx.ALL, 25)
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
            self.SetReturnCode(wx.ID_OK)
            self.Destroy()


    def OnCancel(self, evt):
        self.SetReturnCode(wx.ID_CANCEL)
        self.Destroy()
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
          dc = wx.ClientDC(self.GetClientWindow())

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
        #~ self.log.WriteText('EvtText: %s\n' % evt.GetString())
        if evt.GetId() == HOST_COMBOBOX_ID:URLITEMS['HOST'] = evt.GetString()
        if evt.GetId() == PORT_COMBOBOX_ID:URLITEMS['PORT'] = evt.GetString()
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
                dlg = wx.MessageDialog(self.parent, 'Need a value for '+str(i),
                          'No!', wx.OK | wx.ICON_INFORMATION)
                          #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION)
                dlg.ShowModal()
                done = False

        if done:
            s = ""
            for i in URLSEQ:
                s += URLITEMS[i]
            self.log.WriteText("formURLStrings:%s" % (s))

            if URLITEMS['HOST'] not in self.URLcomponents.hosts: self.URLcomponents.hosts.append( str(URLITEMS['HOST']) )
            if URLITEMS['PORT'] not in self.URLcomponents.ports: self.URLcomponents.ports.append( str(URLITEMS['PORT']) )
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