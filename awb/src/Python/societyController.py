import sys
import re
import urllib
import random as r
import time
import os
import thread
import httplib

#from wxPython.wx import *
#from wxPython.ogl import *
#from wxPython.lib.dialogs import wxMultipleChoiceDialog
import wx
import wx.lib.ogl as ogl
from wx.lib.dialogs import wxMultipleChoiceDialog

from ACMEPy.society import Society
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from ACMEPy.component import Component
from ACMEPy.argument import Argument
from ACMEPy.parameter import *
from ACMEPy.Ultralog.organisations import *
from ACMEPy.society_factory2 import SocietyFactory

from societyVisualModel import *
from PollingServices.ServletDataReceiver import *


from insertion_dialog import *
from csmarter_events import *
from societyViewer import SocietyViewer
from eventFactory import EventFactory
from cougaar_DragAndDrop import *
from urlDlg import URLDlg
from facetProperties import FacetProperties
from servletProperties import ServletProperties
from globalConstants import *
import images

import zoomer as z
from PollingServices import *
CONVERTED2DOT5 = True
#---------------------------------------------------------------------
#~ GLOBAL VARS
CLOSE_SOCIETY_BTN_ID = 701
#----------------------------------------------------------------------
# This creates some pens and brushes that the OGL library uses.
# is this right?
wx.OGLInitialize()

class SocietyController(wx.Panel):
    def __init__(self, parent, frame, log):
        wx.Panel.__init__(self, parent, -1)
        self.society = None
        self.hierarchy = None
        self.URL = None
        self.log = log
        self.frame = frame
        self.printData = wx.PrintData()
        self.printData.SetPaperId(wx.PAPER_LETTER)
        self.heatRange  = {50:"PURPLE", 100:"BLUE", 125:"SEA GREEN", 150:"ORANGE", 1000:"RED" }
#--------
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.canvas = SocietyControllerCanvas(self, frame, log)
        self.box.Add(self.canvas, 1, wx.GROW)
        subbox = wx.BoxSizer(wx.HORIZONTAL)
        # ----- new experimental code

        self.openSocietyButton = wx.Button(self, 10, "Open Society")
#        EVT_BUTTON(self, 10, self.OnOpenSociety)
        self.Bind(wx.EVT_BUTTON, self.OnOpenSociety, self.openSocietyButton)

        self.openSocietyButton.SetBackgroundColour(wx.BLUE)
        self.openSocietyButton.SetForegroundColour(wx.WHITE)
        self.openSocietyButton.SetDefault()
        subbox.Add(self.openSocietyButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)

        # ------
        self.viewSocietyButton = wx.Button(self, 11, "View Society")
#        EVT_BUTTON(self, 11, self.OnViewSociety)
        self.Bind(wx.EVT_BUTTON, self.OnViewSociety, self.viewSocietyButton)
        self.viewSocietyButton.SetBackgroundColour(wx.GREEN)
        self.viewSocietyButton.SetForegroundColour(wx.WHITE)
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.viewSocietyButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)
        #~ EVT_SOCIETYCONTROLLER_TEST(self, self.EventUpdate)
        EVT_AGENT_TASK_COUNT(self, self.AgentTaskCountUpdate)
        self.Bind(EVT_AGENT_TASK_COUNT,self.AgentTaskCountUpdate )
        # ------
        self.closeSocietyButton = wx.Button(self, CLOSE_SOCIETY_BTN_ID, "Close Society")
#        EVT_BUTTON(self, CLOSE_SOCIETY_BTN_ID, self.OnCloseSociety)
        self.Bind(wx.EVT_BUTTON, self.OnCloseSociety, self.closeSocietyButton)
        self.closeSocietyButton.SetBackgroundColour(wx.BLACK)
        self.closeSocietyButton.SetForegroundColour(wx.WHITE)
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.closeSocietyButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)
        #~ EVT_SOCIETYCONTROLLER_TEST(self, self.EventUpdate)

        # ------
        self.ZoomPlusButton = wx.Button(self, 12, "+")
#        EVT_BUTTON(self, 12, self.OnZoomPlus)
        self.Bind(wx.EVT_BUTTON, self.OnZoomPlus, self.ZoomPlusButton)
        self.ZoomPlusButton.SetBackgroundColour(wx.GREEN)
        self.ZoomPlusButton.SetForegroundColour(wx.WHITE)

        subbox.Add(self.ZoomPlusButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)

       # ------
        self.ZoomMinusButton = wx.Button(self, 13, "-")
#        EVT_BUTTON(self, 13, self.OnZoomMinus)
        self.Bind(wx.EVT_BUTTON, self.OnZoomMinus, self.ZoomMinusButton)
        self.ZoomMinusButton.SetBackgroundColour(wx.RED)
        self.ZoomMinusButton.SetForegroundColour(wx.WHITE)
        subbox.Add(self.ZoomMinusButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)
       # ------
        self.viewServletButton = wx.Button(self, 15, "Servlet Options")
#        EVT_BUTTON(self, 15, self.viewServletOptions)
        self.Bind(wx.EVT_BUTTON, self.viewServletOptions, self.viewServletButton)
        self.viewServletButton.SetBackgroundColour(wx.BLACK)
        self.viewServletButton.SetForegroundColour(wx.WHITE)
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.viewServletButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)

        # ------
        self.testServletButton = wx.Button(self, 16, "Task Probe")
#        EVT_BUTTON(self, 16, self.testServletPolling)
        self.Bind(wx.EVT_BUTTON, self.testServletPolling, self.testServletButton)
        self.testServletButton.SetBackgroundColour(wx.CYAN)
        self.testServletButton.SetForegroundColour(wx.BLACK)
        #~ self.viewSocietyButton.SetDefault()
        subbox.Add(self.testServletButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=20)

        #~ EVT_SOCIETYCONTROLLER_TEST(self, self.EventUpdate)
        self.box.Add(subbox, 0, wx.GROW)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.bg_bmp = images.getGridBGBitmap()
#        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    def OnEraseBackground(self, evt):
        pass
    def AgentTaskCountUpdate(self, evt):
        print 'AgentTaskCountUpdate', evt.msg[0], ' (task count = ',evt.msg[1], ')'
        #~ def PlayRedraw(self, name):
        limit = 0
        #~ for i in self.canvas.shapeDict.iterkeys():
                #~ limit += 1
                #~ if limit > 5: break
                #~ print 'self.canvas.shapeDict==>', i
        if not self.canvas.shapeDict.has_key(evt.msg[0]):
                print "Agent ", evt.msg[0], "not found in hierarchy... Ignoring"
                return
        shape = self.canvas.shapeDict[str(evt.msg[0])]
        # turn on the right color
        heats = self.heatRange.keys()
        heats.sort()
        for h in heats:
                if int(evt.msg[1]) <= h:
                        shape.SetBrush(wx.Brush(self.heatRange[h], wx.SOLID))
                        break
        dc = wx.ClientDC(self.canvas)
        self.canvas.PrepareDC(dc)
        self.canvas.Redraw(dc)

    def OnZoomPlus(self, evt):
        if self.canvas.getSocietyStatus() == "active":
            print "OnZoomPlus"
            currentLevel = z.getLevel() + 1
            z.setLevel(currentLevel)
            self.canvas.OrganizeLevels(boxWidth=z.viewLevelData[currentLevel]["BOXWIDTH"],
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
            self.canvas.OrganizeLevels(boxWidth=z.viewLevelData[currentLevel]["BOXWIDTH"],
            boxHeight=z.viewLevelData[currentLevel]["BOXHEIGHT"],
            widthspacing=z.viewLevelData[currentLevel]["WIDTHSPACING"],
            heightspacing= z.viewLevelData[currentLevel]["HEIGHTSPACING"],
            fontSize=z.viewLevelData[currentLevel]["FONTSIZE"])
        else:
            self.ErrorWindow()

    def OnOpenSociety(self, evt):
        """
        TODO
        """
        #self.frame.openSocietyFile(self, "controller")
        # stub code to exercise parsing and layour engine...
        fileDialog = wx.FileDialog(self, message="Choose a parseable file (*.xml", wildcard = "*.*", style=wx.OPEN  )
        if fileDialog.ShowModal() == wx.ID_OK:
            path = fileDialog.GetPath()
        fileDialog.Destroy()
        self.hierarchy = self.viewSociety(path)
        self.canvas.CreateSocieties(self.hierarchy)
        self.canvas.OrganizeLevels()
        print "Society Opened"


    def OnViewSociety(self, evt):
        win = URLDlg(self,wx.NewId(), self.log, "Society Ping", size=wx.Size(400, 300),style = wx.DEFAULT_DIALOG_STYLE)
        win.CenterOnScreen()
        val = win.ShowModal()
        if val == wx.ID_OK:
            self.log.WriteText("URLDlg OK\n")
            self.log.WriteText(self.URL)
            self.hierarchy = ULHierarchy(uri=self.URL)
            self.canvas.CreateSocieties(self.hierarchy)
            self.canvas.OrganizeLevels()

            self.log.WriteText(str(self.hierarchy))
        else:
            self.log.WriteText("URLDlg Cancel\n")
        print "Society Viewed"

    def viewSociety(self, generator_file):
        """
        TODO
        """

        #~ print "creating society from  %s" % generator_file ### DEBUG -- remove this!
        return ULHierarchy(uri='file:'+str(generator_file))

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
            self.canvas.OrganizeLevels()



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

    #~ def viewSociety(self, generator_file):
        #~ return ULHierarchy(uri='file:'+str(generator_file))

    def loadSociety(self, generator_file):
        """
        This wants to be nicely integrated with the GUI, such that
        When you select the file, an animation starts (similar to a busy watch cursor) and when the society is
        complete, an wx.Event is sent to the GUI. see exmaples in other parts of the application.
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
            win = ServletProperties(self.canvas, -1, "Servlet Properties", size=wx.Size(300, 400),style = wx.DEFAULT_DIALOG_STYLE)
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
                print "iteration:", limit, agent,  tasks
                evt = AgentTaskCountEvent((agent, tasks))
                wx.PostEvent(self, evt)


    def _ServletPoller(self):
            pass
    #~ def PlayRedraw(self, name):
        #~ shape = self.canvas.shapeDict[name]
        #~ shape.SetBrush(wx.Brush(COLOURDB[r.randint(0, len(COLOURDB)) % len(COLOURDB )], wx.CROSSDIAG_HATCH))
        #~ dc = wx.ClientDC(self.canvas)
        #~ self.canvas.PrepareDC(dc)
        #~ self.canvas.Redraw(dc)

    def ErrorWindow(self):
        #~ def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        win = ServerNotRunning(self.canvas, -1, "Server Inactive", pos=wx.DefaultPosition, size=wx.Size(500, 100), style = wx.DEFAULT_DIALOG_STYLE)
                         #style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME
        win.CenterOnScreen()
        val = win.ShowModal()



#----------------------------------------------------------------------


class SocietyControllerCanvas(wx.ShapeCanvas):

    def __init__(self, parent, frame, log):

        wx.ShapeCanvas.__init__(self, parent)
        self.log = log
        self.parent = parent
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wx.WHITE)
        self.status = "inactive"
        self.diagram = wx.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.AgentInfoDict = {}
        self.shapeDict = {}
        self.shapes = []
        self.save_gdi = []
	#~ Joe -- what is purpose of this vvvvvvvvvvvvvvvvv  ?
        self.TheSociety = mySociety() # create the society
        rRectBrush = wx.Brush("MEDIUM TURQUOISE", wx.SOLID)
        dsBrush = wx.Brush("WHEAT", wx.SOLID)
        #~ self.CreateSocieties()
        #~ self.OrganizeLevels()
        self.SetScrollbars(20, 20, z.MAXWIDTH/20, z.MAXWIDTH/20)

#        EVT_WINDOW_DESTROY(self, self.OnDestroy)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy)

    def MySocietyInit(self):
        self.TheSociety.hideAll()         # Hide all the old nodes
        self.OrganizeLevels()              # Redraw the nodes hidden
        self.shapeDict.clear()             # Clear dictionary list
        del self.shapes[0:]                # Delete the shapes list
        del self.diagram                    # delete the diagram
        self.diagram = wx.Diagram()     #make a new diagram
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        # Reset the society
        self.TheSociety.resetSociety()
        self.status = "inactive"
    def getSocietyStatus(self):
        return self.status

    def CreateSocieties(self, hierarchy,
            boxWidth= z.viewLevelData[1]["BOXWIDTH"],
            boxHeight=z.viewLevelData[1]["BOXHEIGHT"],
            ):
                rootNode = None
                self.TheSociety.ClearFacetList()
                #~ print "CreateSocieties::hierarchy", hierarchy
                #~ print "CreateSocieties::levelmap", hierarchy.levelMap
                for iter in hierarchy.levelMap.levelMap.iterkeys():
                    levelData = hierarchy.levelMap.levelMap[iter]
                    if iter == 1:
                        rootNode = str(levelData.agents[0])
                        self.TheSociety.AddNewFacet(rootNode, "SOURCEFACET", iter-1, "noparent")
                    if iter == 2:
                        for agent in levelData.agents:
                           self.TheSociety.AddNewFacet(str(agent), "HOSTFACET", iter-1, rootNode)
                    if iter == 3:
                        for agent in levelData.agents:
                           agentMetaData = hierarchy.hierarchy[agent]
                           self.TheSociety.AddNewFacet(str(agent), "NODEFACET", iter-1, agentMetaData.getSuperior())
                    if iter == 4:
                        for agent in levelData.agents:
                           agentMetaData = hierarchy.hierarchy[agent]
                           self.TheSociety.AddNewFacet(str(agent), "AGENTFACET", iter-1, agentMetaData.getSuperior())
                    if iter == 5:
                        for agent in levelData.agents:
                           agentMetaData = hierarchy.hierarchy[agent]
                           self.TheSociety.AddNewFacet(str(agent), "COMPONENTFACET", iter-1, agentMetaData.getSuperior())
                    if iter == 6:
                        for agent in levelData.agents:
                           agentMetaData = hierarchy.hierarchy[agent]
                           self.TheSociety.AddNewFacet(str(agent), "Level6", iter-1, agentMetaData.getSuperior())
                    if iter == 7:
                        for agent in levelData.agents:
                           agentMetaData = hierarchy.hierarchy[agent]
                           self.TheSociety.AddNewFacet(str(agent), "Level7", iter-1, agentMetaData.getSuperior())

                tempctr = 0
                facetList = self.TheSociety.getFacetList()
                factListLength = len(facetList)
                while (tempctr < factListLength):
                    #self.MyAddShape(wx.RectangleShape(boxWidth, boxHeight), 0, 0, wx.BLACK_PEN, wx.BLACK_BRUSH, "22", "#AA0000"
                    w = z.viewLevelData[1]["BOXWIDTH"]
                    h = z.viewLevelData[1]["BOXHEIGHT"]
                    self.MyAddShape(
                    wx.RectangleShape(w,h), 100, 100, wx.BLACK_PEN,
                    wx.Brush("WHEAT", wx.SOLID),
                    #~ facetList[tempctr].myFacetBrush,
                    facetList[tempctr].myFacetName,
                    "DARK GREEN"
                    #~ facetList[tempctr].myFacetTextColour
                    )
                    tempctr+=1
                # everything with evtFactory is toy code
                time.sleep(2)
                #~ print "Starting an event factory..."
                #~ evtFactory =  EventFactory(self.parent, self.log)
                #~ evtFactory.Start()

    def MyAddShape(self, shape, x, y, pen, brush, text, textColour):
        FontParameters = wx.Font(10, wx.DEFAULT,wx.NORMAL, wx.NORMAL)

        shape.SetDraggable(True, True)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if textColour:    shape.SetTextColour(textColour)
        if text:
            shape.AddText(text)
            shape.SetClientData(text)
            shape.SetFormatMode(FORMAT_CENTRE_VERT)
            shape.SetRegionName(text)
            # shape.SetShadowMode(SHADOW_RIGHT)
            self.diagram.AddShape(shape)
            shape.Show(True)
            shape.SetFont(FontParameters)

        evthandler = MyEvtHandler(self.frame, self.log)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        self.shapeDict[text] = shape
        #~ return shape

    def OrganizeLevels(self, level=z.ZEROLEVEL, maxWidth=z.MAXWIDTH,
        boxWidth=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXWIDTH"],
        boxHeight=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXHEIGHT"],
        widthspacing=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["WIDTHSPACING"],
        heightspacing= z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["HEIGHTSPACING"],
        fontSize=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["FONTSIZE"]):
        #~ print "organiseLevels", "boxwidth", boxWidth, 'boxhieght', 'boxheight', boxHeight
        dc = wx.ClientDC(self)
        self.PrepareDC(dc)
        self.Clear()

        facetList = self.TheSociety.getFacetList()
        facetLevelList = self.TheSociety.getFacetLevelList()
        self.ResizeBoxes(boxWidth,boxHeight,fontSize)
        self.RedrawAll(facetList)
        totalFacetCount = 0
        boxcount =0
        idx = 0
        maxLevel = 0
        while idx < len(facetLevelList):
            totalFacetCount += facetLevelList[idx]
            if facetLevelList[idx] == 0:
                maxLevel = idx+1
            idx += 1
        numberofboxes = 0
        webindex = 0
        xCoord = 0
        yCoord = 40
        TESTCOUNT = 0

        shape = self.diagram.GetShapeList()
        #~ Node Organization
        while level < maxLevel:
            numberofboxes = facetLevelList[level]
            xCoord = ((maxWidth)-((numberofboxes)*boxWidth)-((numberofboxes-1)*(widthspacing)))/(2)
            #~ Sets the brush color and the text color for each level
            while boxcount < numberofboxes:
                for i in shape:
                    if i.GetClientData() == facetList[webindex].myFacetName:
                        i.SetX(xCoord)
                        i.SetY(yCoord)
                xCoord = xCoord + boxWidth + widthspacing
                boxcount+=1
                webindex+=1
            boxcount = 0
            yCoord = yCoord + boxHeight + heightspacing
            level+=1
        self.CreateConnections(dc)
        self.status = "active"
#    def AddAtLevel(level, shape, xOrigin, YOrigin, pen, brush, text, textColor):
    def CreateConnections(self, dc):
        """
        create the network connections for rectangles
        TODO: a 'real' implementation of this specified by some external representation
        For now we will dummy up the connections a la the diagramme originally from me and then
        modified by Mike Dyson et al
        """
        connectionDirectory = self.TheSociety.getConnectionsDictionary()
        for x in range(len(self.shapes)):
            fromShape = self.shapes[x]
            #~ print "\nFrom:", fromShape.GetClientData()  ### DEBUG
            if connectionDirectory.has_key(fromShape.GetClientData()):
                for connection in connectionDirectory[fromShape.GetClientData()]:
                    #~ print connection,
                    for possibleToShape in self.shapes:
                        if str(possibleToShape.GetClientData()) == str(connection):
                                toShape = possibleToShape
                                line = wx.LineShape()
                                line.SetCanvas(self)
                                line.SetPen(wx.BLACK_PEN)
                                line.SetBrush(wx.BLACK_BRUSH)
                                line.AddArrow(ARROW_ARROW)
                                line.MakeLineControlPoints(2)
                                fromShape.AddLine(line, toShape)
                                self.diagram.AddShape(line)
                                line.Show(True)

                                # for some reason, the shapes have to be moved for the line to show up...
                                fromShape.Move(dc, fromShape.GetX(), fromShape.GetY())
        self.Redraw(dc)
    def UpdateAgentInformation(self):
        #~ self.AgentInfoDict = SocietyQuery('http://sm056:8800/agents?suffix=.', mutex)
        pass
    def RedrawAll(self, shapesToShow):
        #~ print "RedrawAll"
        shapeNames = []
        for name in shapesToShow:
            shapeNames.append(name.myFacetName)
        for i in self.diagram.GetShapeList():
            i.Show(False)
            if i.GetRegionName(0) in shapeNames:
                i.Show(True)


    def OnDestroy(self, evt):
        # Do some cleanup
        for shape in self.diagram.GetShapeList():
            if shape.GetParent() == None:
                shape.SetCanvas(None)
                shape.Destroy()
        self.diagram.Destroy()

    def ResizeBoxes(self, nWidth, nHeight, nFontSize):
        FontParameters = wx.Font(nFontSize, wx.DEFAULT,wx.NORMAL, wx.NORMAL)
        for i in self.diagram.GetShapeList():
            i.SetSize(nWidth, nHeight)
            i.SetFont(FontParameters)


    def OnBeginDragLeft(self, x, y, keys):
        self.log.write("OnBeginDragLeft: %s, %s, %s\n" % (x, y, keys))

    def OnEndDragLeft(self, x, y, keys):
        self.log.write("OnEndDragLeft: %s, %s, %s\n" % (x, y, keys))

#----------------------------------------------------------------------

#----------------------------------------------------------------------
class MyEvtHandler(wx.ShapeEvtHandler):
    def __init__(self, frame, log):
        wx.ShapeEvtHandler.__init__(self)
        self.log = log
        self.statbarFrame = frame

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        print shape.__class__, shape.GetClassName()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
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

        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)
        FacetPropertiesID = shape.GetClientData() + " Properties"

        win = FacetProperties(shape, canvas, -1, FacetPropertiesID, size=wx.Size(300, 400),style = wx.DEFAULT_DIALOG_STYLE)
                         #style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME

        win.CenterOnScreen()
        if win.ShowModal() == wx.ID_OK:
            self.log.WriteText("You pressed OK\n")
        else:
            self.log.WriteText("You pressed Cancel\n")


class ServerNotRunning(wx.Dialog):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE):
        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)
        self.this = pre.this

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, "The Society is inactive")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, wx.ID_OK, " OK ")
        btn.SetDefault()
        btn.SetHelpText("The OK button completes the dialog")
        box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.AddSizer(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
#----------------------------------------------------------------------

class __Cleanup:
    cleanup = wx.OGLCleanUp
    def __del__(self):
        self.cleanup()

# when this module gets cleaned up then wx.OGLCleanUp() will get called
__cu = __Cleanup()

overview = """\
The Object Graphics Library is a library supporting the creation and
manipulation of simple and complex graphic images on a canvas.

"""
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = SocietyController(nb,frame,  log)
    return win

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])