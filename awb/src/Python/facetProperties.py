import sys


from wxPython.wx import *
from societyVisualModel import *
#~ from societyController import *
import wx
import wx.lib.ogl as ogl

CONVERTED2DOT5 = True
class FacetProperties(wx.Dialog):
    def __init__(self, facetinfo, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        #~ TheSociety.getFacetDepth(facetinfo.GetClientData())
        pre = wx.PreDialog()
        print "parent:", parent
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        
        textcolor = facetinfo.GetTextColour()
        sizer = wx.BoxSizer(wx.VERTICAL)
        RBOX1 = wx.NewId()
        borderSize = 10


        startXposition = 10
        startYposition = 10
        label = wx.StaticText(self, -1, "Information",pos=(startXposition,startYposition))
        
        startXposition = 70
        startYposition = 17
        line = wx.StaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wx.LI_HORIZONTAL)        
        
        startXposition = 15
        startYposition = 30
        label = wx.StaticText(self, -1, "Name: " + facetinfo.GetClientData(),pos=(startXposition,startYposition))
        
        startXposition = 15
        startYposition = 50
        label = wx.StaticText(self, -1, "Status: RUNNING" ,pos=(startXposition,startYposition))
        
        startXposition = 15
        startYposition = 70
        label = wx.StaticText(self, -1, "Type:" ,pos=(startXposition,startYposition))
        
        startXposition = 10
        startYposition = 90
        label = wx.StaticText(self, -1, "View",pos=(startXposition,startYposition))
        
        startXposition = 40
        startYposition = 97
        line = wx.StaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wx.LI_HORIZONTAL)        

        startXposition = 15
        startYposition = 110
        depthList = ['Show Children', 'Hide Children']
        rb = wx.RadioBox(self, RBOX1, "Depth", wx.Point(startXposition,startYposition), wx.DefaultSize, depthList, 2, wx.RA_SPECIFY_ROWS)
        self.Bind(wx.EVT_RADIOBOX,   self.EvtRadioBox, rb)
        
        
        startXposition = 140
        startYposition = 110
        
        self.hmc = wx.StaticText(self, -1, "How Many Children?" ,pos=(startXposition,startYposition))
        
        startXposition = 140
        startYposition = 130
        depthList = ['all', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen']
        self.cb = wx.ComboBox(self, 500, "show...", wx.Point(startXposition,startYposition), wx.Size(95, -1), depthList[0:parent.TheSociety.getDepth(facetinfo.GetClientData())] , wx.CB_DROPDOWN)#|wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_COMBOBOX,   self.EvtComboBox, self.cb)
        
        startXposition = 10
        startYposition = 180
        label = wx.StaticText(self, -1, "Messages",pos=(startXposition,startYposition))

        startXposition = 65
        startYposition = 187
        line = wx.StaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wx.LI_HORIZONTAL)

        startXposition = 35
        startYposition = 330
        bOk = wx.Button(self, wx.ID_OK, "OK", wx.Point(startXposition, startYposition), wx.Size(100, 30))
        #~ EVT_BUTTON(self, b.GetId(), self.OnPressOk)
        bOk.SetDefault()

        startXposition = 165
        startYposition = 330
        bCan = wx.Button(self, wx.ID_CANCEL, "Cancel", wx.Point(startXposition, startYposition), wx.Size(100, 30))

        if self.ShowModal() == wx.ID_OK:
            if self.hmc.IsEnabled():
                if self.cb.GetSelection() == 0:
                        parent.TheSociety.organizeConnections(facetinfo.GetClientData(), -1)
                        parent.OrganizeLevels()
                else:
                        parent.TheSociety.organizeConnections(facetinfo.GetClientData(), self.cb.GetSelection())
                        parent.OrganizeLevels()
            else:
                parent.TheSociety.organizeConnections(facetinfo.GetClientData(), 0)
                parent.OrganizeLevels()
            self.Destroy()
        else:
            self.Destroy()
            
    def EvtRadioBox(self, event):
        #~ self.log.WriteText('EvtRadioBox: %d\n' % event.GetInt())
        #~ print event.GetInt()
        if event.GetInt() == 1:
            self.cb.Enable(False)
            self.hmc.Enable(False)
        else:
            self.cb.Enable(True)
            self.hmc.Enable(True)
        
    def EvtComboBox(self, evt):
        self.cb = evt.GetEventObject()

        
    def OnPressOk(self, event):
        print "You clicked OK" 