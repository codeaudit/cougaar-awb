# CONVERTED2DOT5 = TRUE

import sys
import re
import urllib
import random as r
import time
import os
import math
import thread
import httplib

import wx
import wx.lib.ogl as ogl
import wx.lib.dialogs
import zoomer as z

#----------------------------------------------------------------------


class AgentCanvas(ogl.ShapeCanvas):

    def __init__(self, parent, frame, log):

        ogl.ShapeCanvas.__init__(self, parent)
        self.log = log
        self.parent = parent
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wxWHITE)
        self.status = "inactive"
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.AgentInfoDict = {}
        self.shapeDict = {}
        self.shapes = []
        self.save_gdi = []

        #~ self.CreateSociety()
        #~ self.OrganizeAgents()
        self.SetScrollbars(20, 20, z.MAXWIDTH/20, z.MAXWIDTH/20)

        #~ self.agentBmp = earthImage.getBitmap()
        #~ mask = wxMaskColour(self.agentBmp, wxColour(red=254, green=254, blue=254))
        #~ self.agentBmp.SetMask(mask)
        wx.EVT_WINDOW_DESTROY(self, self.OnDestroy)
        #~ EVT_RIGHT_UP(self, self.OnRightClick)

    def MySocietyInit(self):
        self.OrganizeAgents()              # Redraw the nodes hidden
        self.shapeDict.clear()             # Clear dictionary list
        del self.shapes[0:]                # Delete the shapes list
        del self.diagram                    # delete the diagram
        self.diagram = ogl.Diagram()     #make a new diagram
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        # Reset the society
        self.status = "inactive"
    def getSocietyStatus(self):
        return self.status
    def setSocietyActive(self):
        self.status = "active"
    def CreateSociety(self, agentList,
            boxWidth= z.viewLevelData[2]["BOXWIDTH"],
            boxHeight=z.viewLevelData[2]["BOXHEIGHT"],
            ):
        self.diagram.RemoveAllShapes()

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
            ogl.RectangleShape(w,h), x,y, wx.BLACK_PEN,
            wx.Brush("GREY", wx.SOLID),
            str(agent),
            "BLACK"
            )
            #~ s = wxBitmapShape()
            #~ s.SetBitmap(self.agentBmp)
            #~ self.addShape(s, x, y, None, None, str(agent), "YELLOW")

    def addShape(self, shape, x, y, pen, brush, text, textColour):
        FontParameters = wx.Font(10, wx.DEFAULT,wx.NORMAL, wx.NORMAL)
        print "SHAPE==>", shape
        shape.SetDraggable(True, True)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if textColour:    shape.SetTextColour(textColour)
        if text:
            shape.AddText(text)
            shape.SetFormatMode(ogl.FORMAT_CENTRE_VERT)
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

    def OrganizeAgents(self,# level=z.ZEROLEVEL, maxWidth=z.MAXWIDTH,
        boxWidth=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXWIDTH"],
        boxHeight=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["BOXHEIGHT"],
        widthspacing=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["WIDTHSPACING"],
        heightspacing= z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["HEIGHTSPACING"],
        fontSize=z.viewLevelData[z.DEFAULT_ZOOMLEVEL]["FONTSIZE"]):
        newfont = wx.Font(fontSize, wx.DEFAULT,wx.NORMAL, wx.NORMAL)
        self.Refresh(True) 
        for shape in self.shapes:
            shape.SetFont(newfont)
            shape.SetWidth(boxWidth)
            shape.SetHeight(boxHeight)
        dc = wx.ClientDC(self)
        self.PrepareDC(dc)
#        self.CreateConnections(dc)

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
                        line = ogl.LineShape()
                        line.SetCanvas(self)
                        line.SetPen(wx.BLACK_PEN)
                        line.SetBrush(wx.BLACK_BRUSH)

                        line.MakeLineControlPoints(2)
                        fromShape.AddLine(line, toShape)
                        self.diagram.AddShape(line)
                        line.Show(True)
                        fromShape.Move(dc, fromShape.GetX(), fromShape.GetY())
        self.Redraw(dc)

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

    


class MyEvtHandler(ogl.ShapeEvtHandler):
    def __init__(self, frame, log):
        ogl.ShapeEvtHandler.__init__(self)
        self.log = log
        self.statbarFrame = frame

    #~ def UpdateStatusBar(self, shape):
        #~ x, y = shape.GetX(), shape.GetY()
        #~ width, height = shape.GetBoundingBoxMax()
        #~ self.statbarFrame.SetStatusText("Pos: (%d, %d)  Size: (%d, %d)" %
                                        #~ (x, y, width, height))

    def OnLeftClick(self, x, y, keys = 0, attachment = 0):
        shape = self.GetShape()
        #~ print "CLICK: X,Y >>>", x,y
        self.log.WriteText("LEFTCLICK in Event Handler: shaoe class %s name %s\n" % (str(shape.__class__), self.GetShape().GetClassName()))
        #~ print shape.__class__, shape.GetClassName()
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
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)
        #~ self.UpdateStatusBar(shape)


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        #~ self.UpdateStatusBar(self.GetShape())


    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
        #~ self.UpdateStatusBar(self.GetShape())

    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        self.log.WriteText("RIGHTCLICK in Event Handler: %s\n" % self.GetShape())
        TODO = ''' centre the object on the canvas'''


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