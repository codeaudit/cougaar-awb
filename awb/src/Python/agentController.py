import sys
import re
import urllib
import random as r
import time
import os
import signal
import thread
import httplib

from wxPython.wx import *
from wxPython.ogl import *
from wxPython.lib.dialogs import wxMultipleChoiceDialog


# ----------------
# AWB Generic mods
from probeDLG import ProbeDlg
from ctrlDLG import CtrlDlg
from societyReader import SocietyReader
from agentCanvas import AgentCanvas
from informationPanel import InformationPanel

# -----------------
#~ from societyVisualModel import *
#~ from PollingServices.ServletDataReceiver import *


#~ from insertion_dialog import *
from csmarter_events import *
from eventFactory import EventFactory

from servletProperties import ServletProperties
from globalConstants import *
import images

import zoomer as z


#---------------------------------------------------------------------
#~ GLOBAL VARS
CLOSE_SOCIETY_BTN_ID = 701
GLOBAL_WIDGET_ID_BASE = 10
#----------------------------------------------------------------------
# This creates some pens and brushes that the OGL library uses.

wxOGLInitialize()

class AgentControllerViewer(wxPanel):
    def __init__(self, parent, frame, log):
        wxPanel.__init__(self, parent, -1)
        self.society = None
        self.hierarchy = None
        self.URL = None
        self.log = log
        self.frame = frame
        self.printData = wxPrintData()
        self.printData.SetPaperId(wxPAPER_LETTER)
        self.heatRange  = {50:"PURPLE", 100:"BLUE", 125:"SEA GREEN", 150:"ORANGE", 1000:"RED" }
#--------
        self.box = wxBoxSizer(wxVERTICAL)
        self.canvas = AgentCanvas(self, frame, log)
        self.box.Add(self.canvas, 1, wxGROW)
        subbox = wxBoxSizer(wxHORIZONTAL)

# ------
        self.ctrlSocietyButtonID =  GLOBAL_WIDGET_ID_BASE+1
        self.ctrlSocietyButton = wxButton(self, self.ctrlSocietyButtonID , "Start")

        EVT_BUTTON(self, self.ctrlSocietyButtonID, self.OnStartSociety)
        self.ctrlSocietyButton.SetBackgroundColour("BLACK")
        self.ctrlSocietyButton.SetForegroundColour("WHITE")
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.ctrlSocietyButton , flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)


        # ------
        self.viewSocietyButton = wxButton(self, GLOBAL_WIDGET_ID_BASE+2, "View Agents")
        EVT_BUTTON(self, GLOBAL_WIDGET_ID_BASE+2, self.OnViewSociety)
        self.viewSocietyButton.SetBackgroundColour("BLUE")
        self.viewSocietyButton.SetForegroundColour("YELLOW")
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.viewSocietyButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)


        # ------

        EVT_AGENT_TASK_COUNT(self, self.AgentTaskCountUpdate)

        # ------
        # ------
        self.ZoomPlusButton = wxButton(self, GLOBAL_WIDGET_ID_BASE+3, "+")
        EVT_BUTTON(self, GLOBAL_WIDGET_ID_BASE+3, self.OnZoomPlus)
        self.ZoomPlusButton.SetBackgroundColour(wxGREEN)
        self.ZoomPlusButton.SetForegroundColour(wxWHITE)

        subbox.Add(self.ZoomPlusButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)

       # ------
        self.ZoomMinusButton = wxButton(self, GLOBAL_WIDGET_ID_BASE+4, "-")
        EVT_BUTTON(self, GLOBAL_WIDGET_ID_BASE+4, self.OnZoomMinus)
        self.ZoomMinusButton.SetBackgroundColour(wxRED)
        self.ZoomMinusButton.SetForegroundColour(wxWHITE)
        subbox.Add(self.ZoomMinusButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)
       # ------
        #~ self.viewServletButton = wxButton(self, 15, "Servlet Options")
        #~ EVT_BUTTON(self, 15, self.viewServletOptions)
        #~ self.viewServletButton.SetBackgroundColour(wxBLACK)
        #~ self.viewServletButton.SetForegroundColour(wxWHITE)
        #~ self.viewSocietyButton.SetDefault()
        #~ subbox.Add(self.viewServletButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)

        # ------
        self.testServletButton = wxButton(self, GLOBAL_WIDGET_ID_BASE+5, "Agent Probes")
        EVT_BUTTON(self, GLOBAL_WIDGET_ID_BASE+5, self.AgentTaskCountUpdate)
        self.testServletButton.SetBackgroundColour(wxCYAN)
        self.testServletButton.SetForegroundColour(wxBLACK)
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.testServletButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)

        #~ EVT_SOCIETYCONTROLLER_TEST(self, self.EventUpdate)
        self.box.Add(subbox, 0, wxGROW)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.bg_bmp = images.getGridBGBitmap()
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)


    def OnEraseBackground(self, evt):
        pass

    def AgentTaskCountUpdate(self, evt):
            print >> sys.stdout, "AgentTaskCountUpdate"
            if self.societyReader is not None:
                #~ print >> sys.stdout, "..."
                uniqueObjects = self.societyReader.readUniqueObjects(self.HOST, self.PORT)
                for o in uniqueObjects.keys():

                    self.computeHeat(o, uniqueObjects[o])
                #~ info = InformationPanel (140, 300, self.canvas, information=uniqueObjects)
                #~ self.canvas.addShape(info,     100, 100, wxBLACK_PEN, wxBrush("LIGHT STEEL BLUE", wxSOLID), '   unique Objects', "Yellow"  )
                #~ dc = wxClientDC(self.canvas)
                #~ self.canvas.PrepareDC(dc)
                #~ self.canvas.Redraw(dc)
            else: print >> sys.stdout, "WTF???"

    def OnZoomPlus(self, evt):
        if self.canvas.getSocietyStatus() == "active":
            print "OnZoomPlus"
            currentLevel = z.getLevel() + 1
            z.setLevel(currentLevel)
            self.canvas.OrganizeAgents(boxWidth=z.viewLevelData[currentLevel]["BOXWIDTH"],
            boxHeight=z.viewLevelData[currentLevel]["BOXHEIGHT"],
            widthspacing=z.viewLevelData[currentLevel]["WIDTHSPACING"],
            heightspacing= z.viewLevelData[currentLevel]["HEIGHTSPACING"],
            fontSize=z.viewLevelData[currentLevel]["FONTSIZE"])
        else:
            self.ErrorWindow()

    def OnZoomMinus(self, evt):
        if self.canvas.getSocietyStatus() == "active":
            print "OnZoomMinus"
            currentLevel = z.getLevel() - 1
            z.setLevel(currentLevel)
            self.canvas.OrganizeAgents(boxWidth=z.viewLevelData[currentLevel]["BOXWIDTH"],
            boxHeight=z.viewLevelData[currentLevel]["BOXHEIGHT"],
            widthspacing=z.viewLevelData[currentLevel]["WIDTHSPACING"],
            heightspacing= z.viewLevelData[currentLevel]["HEIGHTSPACING"],
            fontSize=z.viewLevelData[currentLevel]["FONTSIZE"])
        else:
            self.ErrorWindow()

    def OnStartSociety(self, evt):
        """
        We are limited to localhost currently!!!
        """
        self.NODE = None
        win = CtrlDlg(self,wxNewId(), self.log, "Start a Society", size=wxSize(400, 300),style = wxDEFAULT_DIALOG_STYLE)
        win.CenterOnScreen()
        val = win.ShowModal()
        if val != wxID_OK:
            return
        print "OK::", self.NODE
        rtn = self.startNode()
        if (rtn):
            self.ctrlSocietyButton.SetBackgroundColour("WHITE")
            self.ctrlSocietyButton.SetForegroundColour("BLACK")
            self.ctrlSocietyButton.SetLabel("Stop")
            EVT_BUTTON(self, self.ctrlSocietyButtonID, self.OnStopSociety)

    def OnStopSociety(self, evt):
        #~ signal.signal(signal.SIGINT|signal.SIG_DFL, self.spawnPID)
        if sys.platform[:3] in ('win', 'os2'):
            print 'must use WMI, Win32.all extensions'
        self.ctrlSocietyButton.SetBackgroundColour("BLACK")
        self.ctrlSocietyButton.SetForegroundColour("WHITE")
        self.ctrlSocietyButton.SetLabel("Start")
        EVT_BUTTON(self, self.ctrlSocietyButtonID , self.OnStartSociety)

    def OnViewSociety(self, evt):
        agentList = []
        self.URL = None
        self.HOST = None
        self.PORT = None
        win = ProbeDlg(self,wxNewId(), self.log, "Society Ping", size=wxSize(400, 300),style = wxDEFAULT_DIALOG_STYLE)
        win.CenterOnScreen()
        val = win.ShowModal()
        if val == wxID_OK:
            self.log.WriteText("URLDlg OK\n")
            self.log.WriteText(self.URL)
            #~ print "read...", self.URL, "host==", self.HOST,"port==", self.PORT
            societyreader = SocietyReader(self.URL)
            self.societyReader = societyreader
            #~ print "societyreader:", societyreader
            agentList = societyreader.readAgents()
            if agentList is None:
                dlg = wxMessageDialog(self.frame, "Society not up as yet. Try again in a few seconds",
                          'Non-fatal Error', wxOK|wxICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                self.log.WriteText(str(agentList))
                self.canvas.CreateSociety(agentList)
                self.canvas.OrganizeAgents()

        else:
            self.log.WriteText("URLDlg Cancel\n")
        #~ print "Society Viewed"

    #~ def viewSociety(self, generator_file):
        """
        TODO
        """

        #~ print "creating society from  %s" % generator_file ### DEBUG -- remove this!
        #~ return ULHierarchy(uri='file:'+str(generator_file))
    def startNode(self):
        try:
            cip = os.environ['COUGAAR_INSTALL_PATH']
            execstring = cip+os.sep+'bin'+os.sep+'XSLNode'
            self.spawnPID = os.spawnv(os.P_NOWAIT,execstring, (execstring, self.NODE));
            #~ print 'spawned...',execstring , ' ID=', self.spawnPID
        except KeyError:
            dlg = wxMessageDialog(self.frame, "set 'COUGAAR_INSTALL_PATH' as an environmental variable",
                          'Fatal Error', wxOK|wxICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        return True


    def computeHeat(self, agent, value):
        print "computeHeat:", agent, 'value:',value
        shape = self.canvas.shapeDict[str(agent)]
        # turn on the right color
        #~ color = self.computeColor(value)
        shape.SetBrush(wxBrush(self.computeColor(value), wxSOLID))
        dc = wxClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        self.canvas.Redraw(dc)

    def computeColor(self, agentValue):
        red = green = blue = 0
        agentValue = int(agentValue)
        agentValue = agentValue * 2
        if agentValue < 256:
            red = 0; green = agentValue; blue = 255 - agentValue
        elif  256 <= agentValue < 512:
            red = agentValue - 256; green = 255; blue = 0
        elif 512 <= agentValue  < 767:
            red = 255; green = 766 - agentValue; blue = 0
        else:
            red = 255; green = 0; blue = 0
        return wxColour(red, green, blue)

    def loadFromURL(self, aURL):
        file = urllib.urlopen(aURL)
        #~ self.log.WriteText(aURL+"\n\n")
        #~ for line in self.file.readlines():
            #~ self.log.WriteText(line)
        society =  SocietyFactory(uri='hierarchy.xml').parse()
        if society is not None:
            #~ print society
            self.hierarchy = MilitaryHierarchy(society)
            self.canvas.CreateSocieties(self.hierarchy)
            self.canvas.OrganizeAgents()



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

    def loadSociety(self, generator_file):
        """
        This wants to be nicely integrated with the GUI, such that
        When you select the file, an animation starts (similar to a busy watch cursor) and when the society is
        complete, an wxEvent is sent to the GUI. see exmaples in other parts of the application.
        use SocietyFactoryServer instead of SocietyFactory
        """
        m = re.compile('\.', re.IGNORECASE).split(str(generator_file))
        baseName = str(m[0])
        #~ print "creating society from  %s" % baseName ### DEBUG -- remove this!
        self.log.WriteText("file:" + generator_file)
        return SocietyFactory("file:" + generator_file).parse()
#----------------------------------------------------------------------

    def OnCloseSociety(self,evt):
        if self.canvas.getSocietyStatus() == "active":
            self.canvas.MySocietyInit()
            print "Society Closed"
        else:
            self.ErrorWindow()
        #~ pass


    def viewServletOptions(self, evt):
        if self.canvas.getSocietyStatus() == "active":
            win = ServletProperties(self.canvas, -1, "Servlet Properties", size=wxSize(300, 400),style = wxDEFAULT_DIALOG_STYLE)
            win.CenterOnScreen()
            val = win.ShowModal()
        else:
            self.ErrorWindow()
        #~ pass
    def testServletPolling(self, evt):
        s = ServletDataReceiver("localhost", 8888)
        thread_id = thread.start_new_thread( s.serve, ())
        self.ServletPoller()
    def ServletPoller(self):
        agentMap = dict.fromkeys(self.hierarchy.getAgents(), -1)
        aPeer = xmlrpclib.Server('http://localhost:8888')
        data = aPeer.initServerMethods(agentMap)
        limit = 0
        for agent in agentMap.iterkeys():
                limit += 1
                if limit > 500: break
                tasks = aPeer.getGeneratedData(agent)
                #~ print "iteration:", limit, agent,  tasks
                evt = AgentTaskCountEvent((agent, tasks))
                wxPostEvent(self, evt)


    def _ServletPoller(self):
            pass
    #~ def PlayRedraw(self, name):
        #~ shape = self.canvas.shapeDict[name]
        #~ shape.SetBrush(wxBrush(COLOURDB[r.randint(0, len(COLOURDB)) % len(COLOURDB )], wxCROSSDIAG_HATCH))
        #~ dc = wxClientDC(self.canvas)
        #~ self.canvas.PrepareDC(dc)
        #~ self.canvas.Redraw(dc)

    def ErrorWindow(self):
        #~ def __init__(self, parent, ID, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        win = ServerNotRunning(self.canvas, -1, "Server Inactive", pos=wxDefaultPosition, size=wxSize(500, 100), style = wxDEFAULT_DIALOG_STYLE)
                         #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME
        win.CenterOnScreen()
        val = win.ShowModal()



#----------------------------------------------------------------------



#----------------------------------------------------------------------
class RoundedRectangleShape(wxRectangleShape):
    def __init__(self, w=0.0, h=0.0):
        wxRectangleShape.__init__(self, w, h)
        self.SetCornerRadius(-0.3)

#----------------------------------------------------------------------
class MyEvtHandler(wxShapeEvtHandler):
    def __init__(self, frame, log):
        wxShapeEvtHandler.__init__(self)
        self.log = log
        self.statbarFrame = frame

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        print shape.__class__, shape.GetClassName()
        canvas = shape.GetCanvas()
        dc = wxClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
            print shape.GetX(), shape.GetY()
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Redraw(dc)

        #~ self.UpdateStatusBar(shape)

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        self.base_OnEndDragLeft(x, y, keys, attachment)
        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)
        #~ self.UpdateStatusBar(shape)


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):

        self.base_OnSizingEndDragLeft(pt, x, y, keys, attch)
        #~ self.UpdateStatusBar(self.GetShape())


    def OnMovePost(self, dc, x, y, oldX, oldY, display):

        self.base_OnMovePost(dc, x, y, oldX, oldY, display)
        #~ self.UpdateStatusBar(self.GetShape())

    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        self.log.WriteText("RIGHTCLICK in Event Handler: %s\n" % self.GetShape())
        shape = self.GetShape()
        print shape.__class__, shape.GetClassName()
        # if it's an information panel, then delete it on right click...
        canvas = shape.GetCanvas()
        dc = wxClientDC(canvas)
        canvas.PrepareDC(dc)
        FacetPropertiesID = shape.GetClientData() + " Properties"

        win = FacetProperties(shape, canvas, -1, FacetPropertiesID, size=wxSize(300, 400),style = wxDEFAULT_DIALOG_STYLE)
                         #style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME

        win.CenterOnScreen()
        if win.ShowModal() == wxID_OK:
            self.log.WriteText("You pressed OK\n")
        else:
            self.log.WriteText("You pressed Cancel\n")


class ServerNotRunning(wxDialog):
    def __init__(self, parent, ID, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_DIALOG_STYLE):
        pre = wxPreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wxBoxSizer(wxVERTICAL)
        label = wxStaticText(self, -1, "The Society is inactive")
        sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
        box = wxBoxSizer(wxHORIZONTAL)
        btn = wxButton(self, wxID_OK, " OK ")
        btn.SetDefault()
        btn.SetHelpText("The OK button completes the dialog")
        box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
        sizer.AddSizer(box, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
#----------------------------------------------------------------------

class __Cleanup:
    cleanup = wxOGLCleanUp
    def __del__(self):
        self.cleanup()

# when this module gets cleaned up then wxOGLCleanUp() will get called
__cu = __Cleanup()

overview = """\
The Object Graphics Library is a library supporting the creation and
manipulation of simple and complex graphic images on a canvas.

"""
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = AgentControllerViewer(nb,frame,  log)
    return win

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])