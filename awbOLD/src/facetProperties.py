import sys


from wxPython.wx import *
from wxPython.ogl import *
from societyVisualModel import *
#~ from societyController import *

class FacetProperties(wxDialog):
    def __init__(self, facetinfo, parent, ID, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        #~ TheSociety.getFacetDepth(facetinfo.GetClientData())
        pre = wxPreDialog()
        print "parent:", parent
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this
        
        textcolor = facetinfo.GetTextColour()
        sizer = wxBoxSizer(wxVERTICAL)
        RBOX1 = wxNewId()
        borderSize = 10


        startXposition = 10
        startYposition = 10
        label = wxStaticText(self, -1, "Information",pos=(startXposition,startYposition))
        
        startXposition = 70
        startYposition = 17
        line = wxStaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wxLI_HORIZONTAL)        
        
        startXposition = 15
        startYposition = 30
        label = wxStaticText(self, -1, "Name: " + facetinfo.GetClientData(),pos=(startXposition,startYposition))
        
        startXposition = 15
        startYposition = 50
        label = wxStaticText(self, -1, "Status: RUNNING" ,pos=(startXposition,startYposition))
        
        startXposition = 15
        startYposition = 70
        label = wxStaticText(self, -1, "Type:" ,pos=(startXposition,startYposition))
        
        startXposition = 10
        startYposition = 90
        label = wxStaticText(self, -1, "View",pos=(startXposition,startYposition))
        
        startXposition = 40
        startYposition = 97
        line = wxStaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wxLI_HORIZONTAL)        

        startXposition = 15
        startYposition = 110
        depthList = ['Show Children', 'Hide Children']
        rb = wxRadioBox(self, RBOX1, "Depth", wxPoint(startXposition,startYposition), wxDefaultSize, depthList, 2, wxRA_SPECIFY_ROWS)
        EVT_RADIOBOX(self, RBOX1, self.EvtRadioBox)  #  RADIO BOX EVENT

        
        startXposition = 140
        startYposition = 110
        
        self.hmc = wxStaticText(self, -1, "How Many Children?" ,pos=(startXposition,startYposition))
        
        startXposition = 140
        startYposition = 130
        depthList = ['all', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen']
        self.cb = wxComboBox(self, 500, "show...", wxPoint(startXposition,startYposition), wxSize(95, -1), depthList[0:parent.TheSociety.getDepth(facetinfo.GetClientData())] , wxCB_DROPDOWN)#|wxTE_PROCESS_ENTER)
        EVT_COMBOBOX(self, 500, self.EvtComboBox)#  COMBO BOX EVENT

        startXposition = 10
        startYposition = 180
        label = wxStaticText(self, -1, "Messages",pos=(startXposition,startYposition))

        startXposition = 65
        startYposition = 187
        line = wxStaticLine(self, -1, pos=(startXposition,startYposition), size=(size.GetWidth()-startXposition-borderSize,1), style=wxLI_HORIZONTAL)

        startXposition = 35
        startYposition = 330
        bOk = wxButton(self, wxID_OK, "OK", wxPoint(startXposition, startYposition), wxSize(100, 30))
        #~ EVT_BUTTON(self, b.GetId(), self.OnPressOk)
        bOk.SetDefault()

        startXposition = 165
        startYposition = 330
        bCan = wxButton(self, wxID_CANCEL, "Cancel", wxPoint(startXposition, startYposition), wxSize(100, 30))

        if self.ShowModal() == wxID_OK:
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