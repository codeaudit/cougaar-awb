import sys
import re
import urllib
import random as r
import time
import os
import math
import thread
import httplib

from wxPython.wx import *
from wxPython.ogl import *
from wxPython.lib.dialogs import wxMultipleChoiceDialog
import zoomer as z


#----------------------------------------------------------------------


class AgentCanvas(wxShapeCanvas):

    def __init__(self, parent, frame, log):

        wxShapeCanvas.__init__(self, parent)
        self.log = log
        self.parent = parent
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wxWHITE)
        self.status = "inactive"
        self.diagram = wxDiagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.AgentInfoDict = {}
        self.shapeDict = {}
        self.shapes = []
        self.save_gdi = []
        #~ self.TheSociety = mySociety() # create the society
        rRectBrush = wxBrush("MEDIUM TURQUOISE", wxSOLID)
        dsBrush = wxBrush("WHEAT", wxSOLID)
        #~ self.CreateSociety()
        #~ self.OrganizeAgents()
        self.SetScrollbars(20, 20, z.MAXWIDTH/20, z.MAXWIDTH/20)

        #~ self.agentBmp = earthImage.getBitmap()
        #~ mask = wxMaskColour(self.agentBmp, wxColour(red=254, green=254, blue=254))
        #~ self.agentBmp.SetMask(mask)
        EVT_WINDOW_DESTROY(self, self.OnDestroy)
        #~ EVT_RIGHT_UP(self, self.OnRightClick)

    def MySocietyInit(self):
        self.TheSociety.hideAll()         # Hide all the old nodes
        self.OrganizeAgents()              # Redraw the nodes hidden
        self.shapeDict.clear()             # Clear dictionary list
        del self.shapes[0:]                # Delete the shapes list
        del self.diagram                    # delete the diagram
        self.diagram = wxDiagram()     #make a new diagram
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        # Reset the society
        self.TheSociety.resetSociety()
        self.status = "inactive"
    def getSocietyStatus(self):
        return self.status

    def CreateSociety(self, agentList,
            boxWidth= z.viewLevelData[2]["BOXWIDTH"],
            boxHeight=z.viewLevelData[2]["BOXHEIGHT"],
            ):
        self.agentList = agentList
        leList = self.AutoLayout()
        i = 0
        for agent in agentList:
            x = leList[i][0]
            y = leList[i][1]
            i += 1
            print "at ", x, y
            w = z.viewLevelData[2]["BOXWIDTH"]*3
            h = z.viewLevelData[2]["BOXHEIGHT"]
            self.addShape(
            wxRectangleShape(w,h), x,y, wxBLACK_PEN,
            wxBrush("BLUE", wxSOLID),
            str(agent),
            "YELLOW"
            )
            #~ s = wxBitmapShape()
            #~ s.SetBitmap(self.agentBmp)
            #~ self.addShape(s, x, y, None, None, str(agent), "YELLOW")

    def addShape(self, shape, x, y, pen, brush, text, textColour):
        FontParameters = wxFont(10, wxDEFAULT,wxNORMAL, wxNORMAL)

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
    def removeShape(self, shape):
        self.diagram.RemoveShape(shape) # caution this seems to remove the shape from the canvas but NOT delete it
        shapes.remove(shape)

        self.self.GetShape()
        #~ self.shapeDict[text] = shape
        #~ return shape



    def OrganizeAgents(self, level=z.ZEROLEVEL, maxWidth=z.MAXWIDTH,
        boxWidth=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXWIDTH"],
        boxHeight=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXHEIGHT"],
        widthspacing=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["WIDTHSPACING"],
        heightspacing= z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["HEIGHTSPACING"],
        fontSize=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["FONTSIZE"]):
        dc = wxClientDC(self)
        self.PrepareDC(dc)
        self.Clear()
        self.CreateConnections(dc)

    def AutoLayout(self,):
        laListe = []
        radius = 200
        centreOffset = 400
        listLen = len(self.agentList)
        rightAscent = (2 * math.pi) / listLen
        for i in range (0,listLen):
                theta = rightAscent*i
                X = int(math.cos(theta) * radius) + centreOffset
                Y = int( math.sin(theta) * radius) + centreOffset
                laListe.append( [X,Y] )
        return laListe

    def CreateConnections(self, dc):
        for i in range(0, len(self.agentList)):
                this = self.agentList[i]
                those = self.agentList[i+1:len(self.agentList)]
                fromShape = self.shapeDict[this]

                for that in those:
                        toShape = self.shapeDict[that]

                        line = wxLineShape()
                        line.SetCanvas(self)
                        line.SetPen(wxBLACK_PEN)
                        line.SetBrush(wxBLACK_BRUSH)

                        line.MakeLineControlPoints(2)
                        fromShape.AddLine(line, toShape)
                        self.diagram.AddShape(line)
                        line.Show(True)
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
        FontParameters = wxFont(nFontSize, wxDEFAULT,wxNORMAL, wxNORMAL)
        for i in self.diagram.GetShapeList():
            i.SetSize(nWidth, nHeight)
            i.SetFont(FontParameters)


    def OnBeginDragLeft(self, x, y, keys):
        self.log.write("OnBeginDragLeft: %s, %s, %s\n" % (x, y, keys))

    def OnEndDragLeft(self, x, y, keys):
        self.log.write("OnEndDragLeft: %s, %s, %s\n" % (x, y, keys))



class MyEvtHandler(wxShapeEvtHandler):
    def __init__(self, frame, log):
        wxShapeEvtHandler.__init__(self)
        self.log = log
        self.statbarFrame = frame

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        #~ print "CLICK: X,Y >>>", x,y
        self.log.WriteText("LEFTCLICK in Event Handler: shaoe class %s name %s\n" % (str(shape.__class__), self.GetShape().GetClassName()))
        #~ print shape.__class__, shape.GetClassName()
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
        TODO = ''' centre the object on the canvas'''


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