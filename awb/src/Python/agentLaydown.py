#!/bin/env python
#----------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: agentLaydown.py,v 1.4 2004-11-02 17:01:56 damoore Exp $
#  <copyright>
#  Copyright 2002 BBN Technologies, LLC
#  under sponsorship of the Defense Advanced Research Projects Agency (DARPA).
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the Cougaar Open Source License as published by
#  DARPA on the Cougaar Open Source Website (www.cougaar.org).
#
#  THE COUGAAR SOFTWARE AND ANY DERIVATIVE SUPPLIED BY LICENSOR IS
#  PROVIDED 'AS IS' WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS OR
#  IMPLIED, INCLUDING (BUT NOT LIMITED TO) ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND WITHOUT
#  ANY WARRANTIES AS TO NON-INFRINGEMENT.  IN NO EVENT SHALL COPYRIGHT
#  HOLDER BE LIABLE FOR ANY DIRECT, SPECIAL, INDIRECT OR CONSEQUENTIAL
#  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE OF DATA OR PROFITS,
#  TORTIOUS CONDUCT, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
#  PERFORMANCE OF THE COUGAAR SOFTWARE.
# </copyright>
# CONVERTED2DOT5 = TRUE

import wx
from wx.lib.rcsizer import RowColSizer
#from wx import  events
import images
from gizmo import Gizmo
import gizmoImages
import thread
import os
import cPickle
import math
from types import *

from ACMEPy.society import Society
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from societyViewer import SocietyViewer
from csmarter_events import *
from insertion_dialog import *
from cougaar_DragAndDrop import *

#----------------------------------------------------------------------

DISTRO_EVENLY = 0
SPECIFY_NUM = 1
DISTRO_BY_FACET = 2
SAME_DISTRO = 3

class AgentLaydownPanel(wx.Panel):

  def __init__( self, parent, frame, log ):
    wx.Panel.__init__( self, parent, -1 )
    self.log = log
    self.frame = frame # top-level frame that contains this wx.Panel
    self.frame.agentSocietyOpen = 0
    self.openingHnaMap = False
    self.agentSocietyFile = None   # String
    self.societyHnaFile = None     # String
    self.tempMappedSociety = None  # Society
    self.tempAgentSociety = None   # Society
    self.itemGrabbed = False
    self.currentViewer = None      # SocietyViewer
    self.facetClipboard = None     # List
    self.labelEditActivated = True

    ### static controls:

    sizer = RowColSizer()
    btnBox = wx.BoxSizer(wx.HORIZONTAL)

    openAgentListBtnId = wx.NewId()
    self.openAgentListButton = wx.Button(self, openAgentListBtnId, "Open Agent List")
    wx.wx.EVT_BUTTON(self, openAgentListBtnId, self.OnOpenAgentList)
    self.openAgentListButton.SetBackgroundColour(wx.BLUE)
    self.openAgentListButton.SetForegroundColour(wx.WHITE)
    self.openAgentListButton.SetDefault()
    btnBox.Add(self.openAgentListButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.BOTTOM, border=10)

    closeAgentSocietyBtnId = wx.NewId()
    self.closeAgentSocietyButton = wx.Button(self, closeAgentSocietyBtnId, "Close Agent List")
    wx.wx.EVT_BUTTON(self, closeAgentSocietyBtnId, self.OnCloseAgentSociety)
    self.closeAgentSocietyButton.Enable(False)
    btnBox.Add(self.closeAgentSocietyButton, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.BOTTOM, border=10)

    sizer.Add(btnBox, pos=(1,1),  flag=wx.ALIGN_CENTER, colspan=2)

    hnaBox = wx.BoxSizer(wx.HORIZONTAL)

    openHnaBtnId = wx.NewId()
    self.openHnaButton = wx.Button(self, openHnaBtnId, "Open HNA Map")
    wx.wx.EVT_BUTTON(self, openHnaBtnId, self.OnOpenHnaMap)
    hnaBox.Add(self.openHnaButton, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.BOTTOM, border=10)

    saveHnaBtnId = wx.NewId()
    self.saveHnaButton = wx.Button(self, saveHnaBtnId, "Save HNA Map")
    wx.wx.EVT_BUTTON(self, saveHnaBtnId, self.OnSaveHnaMap)
    self.saveHnaButton.Enable(False)
    hnaBox.Add(self.saveHnaButton, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.BOTTOM, border=10)

    closeHnaBtnId = wx.NewId()
    self.closeHnaButton = wx.Button(self, closeHnaBtnId, "Close HNA Map")
    wx.wx.EVT_BUTTON(self, closeHnaBtnId, self.OnCloseHnaMap)
    self.closeHnaButton.Enable(False)
    hnaBox.Add(self.closeHnaButton, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.BOTTOM, border=10)

    sizer.Add(hnaBox, pos=(1,3), flag=wx.ALIGN_RIGHT, colspan=3)

    self.il = wx.ImageList(16,16)
    self.societyImage   = self.il.Add(images.getSocietyBitmap())
    self.hostImage      = self.il.Add(images.getHostBitmap())
    self.nodeImage      = self.il.Add(images.getNodeBitmap())
    self.agentImage     = self.il.Add(images.getAgentBitmap())
    self.componentImage = self.il.Add(images.getComponentBitmap())
    self.argumentImage  = self.il.Add(images.getArgumentBitmap())
    self.questionImage  = self.il.Add(images.getQuestionBitmap())

    societyLabel = wx.StaticText(self, -1, "Agent List:")
    sizer.Add(societyLabel, flag=wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
                  border=5, pos=(2, 1))

    self.agentViewerTotalLabel = wx.StaticText(self, -1, "Total Agents: 0")
    sizer.Add(self.agentViewerTotalLabel, flag = wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
                  border=5, pos=(2, 2))

    agentViewerID = wx.NewId()
    self.frame.agentViewer = SocietyViewer(self, agentViewerID, 'agentViewer', size=(200, 100),
                                 style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_MULTIPLE, log=self.log, inclComponents=False)
    print "Society Viewer (__init__):", self.frame.agentViewer
    agentDropTarget = CougaarDropTarget(self.frame.agentViewer, self.log, self.frame)
    self.frame.agentViewer.SetDropTarget(agentDropTarget)
    sizer.Add(self.frame.agentViewer, flag=wx.EXPAND, pos=(3,1), rowspan=2, colspan=2)
    wx.wx.EVT_LEFT_DOWN(self.frame.agentViewer, self.OnLeftDown)

    spinnerBox = wx.BoxSizer(wx.VERTICAL)

    buildHnaMapID = wx.NewId()
    self.buildHnaMapButton = wx.Button(self, buildHnaMapID, "Build HNA Map...")
    wx.wx.EVT_BUTTON(self, buildHnaMapID, self.OnBuildHnaMap)
    spinnerBox.Add(self.buildHnaMapButton, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    distroAgentsID = wx.NewId()
    self.distroAgentsButton = wx.Button(self, distroAgentsID, "Distribute Agents")
    wx.EVT_BUTTON(self, distroAgentsID, self.OnDistroAgents)
    self.distroAgentsButton.Enable(False)
    spinnerBox.Add(self.distroAgentsButton, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    inclNodesID = wx.NewId()
    self.inclNodesCheckbox = wx.CheckBox(self, inclNodesID, "Include Nodes from Agent List")
    wx.EVT_CHECKBOX(self, inclNodesID, self.OnInclNodesChecked)
    spinnerBox.Add(self.inclNodesCheckbox, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=7)

    ignoreHostFacetsId = wx.NewId()
    self.ignoreHostFacetsCheckbox = wx.CheckBox(self, ignoreHostFacetsId, "Ignore Host Facets")
    wx.EVT_CHECKBOX(self, ignoreHostFacetsId, self.OnIgnoreHostFacetsChecked)
    spinnerBox.Add(self.ignoreHostFacetsCheckbox, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=7)
    self.ignoreHostFacetsCheckbox.Enable(False)

    rbID = wx.NewId()
    rbLabel = "Select method of agent distribution"
    buttonTitles = ["Distribute evenly", "Specify number per host", "Distribute by facet", "Maintain same distribution        "]
    self.rb = wx.RadioBox(self, rbID, rbLabel, wx.DefaultPosition, (-1, 110), buttonTitles, 1, wx.RA_SPECIFY_COLS)
    self.rb.EnableItem(SAME_DISTRO, False)
    wx.EVT_RADIOBOX(self, rbID, self.OnEvtRadioBox)
    spinnerBox.Add(self.rb, 0, wx.ALL, 5)

    # Add the agent per node selection box
    staticBoxTitle = wx.StaticBox( self, -1, "" )
    staticBox = wx.StaticBoxSizer( staticBoxTitle, wx.VERTICAL )
    innerBox = wx.BoxSizer(wx.VERTICAL)

    self.agentSpinnerLabel = wx.StaticText(self, -1, "Select initial number\nof agents per host")
    innerBox.Add(self.agentSpinnerLabel, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    agentSpinnerID = wx.NewId()
    self.agentSpinner = wx.SpinCtrl(self, agentSpinnerID, "1", size=wx.Size(50, -1), min=1, max=1000)
    self.agentSpinner.Enable(False)
    innerBox.Add(self.agentSpinner, flag=wx.ALIGN_CENTER_HORIZONTAL)

    staticBox.AddSizer(innerBox, 0, wx.ALIGN_CENTER)
    spinnerBox.AddSizer(staticBox, 0, wx.ALIGN_CENTER)

    # Add the node per host selection box
    staticBoxTitle = wx.StaticBox( self, -1, "" )
    staticBox = wx.StaticBoxSizer( staticBoxTitle, wx.VERTICAL )
    innerBox = wx.BoxSizer(wx.VERTICAL)

    self.nodeSpinnerLabel = wx.StaticText(self, -1, "Select initial number\nof nodes per host")
    innerBox.Add(self.nodeSpinnerLabel, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    nodeSpinnerID = wx.NewId()
    self.nodeSpinner = wx.SpinCtrl(self, nodeSpinnerID, "1", size=wx.Size(50, -1), min=1, max=100)
    innerBox.Add(self.nodeSpinner, flag=wx.ALIGN_CENTER_HORIZONTAL)

    staticBox.AddSizer(innerBox, 0, wx.ALIGN_CENTER)
    spinnerBox.AddSizer(staticBox, 0, wx.ALIGN_CENTER)

    # Add the "system busy" image
    lesImages = [gizmoImages.catalog[i].getBitmap() for i in gizmoImages.index]
    self.gizmo = Gizmo(self, -1, lesImages, size=(36, 36), frameDelay = 0.1)
    self.Bind(EVT_UPDATE_SOCIETY, self.OnUpdate)
    spinnerBox.Add(self.gizmo, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

    sizer.Add(spinnerBox, pos=(3,3),  flag=wx.ALIGN_CENTER, rowspan=2, colspan=1)

    hnaMapLabel = wx.StaticText(self, -1, "HNA Map:")
    sizer.Add(hnaMapLabel, flag=wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
                  border=5, pos=(2, 4))

    self.laydownViewerTotalLabel = wx.StaticText(self, -1, "Total Agents: 0")
    sizer.Add(self.laydownViewerTotalLabel, flag = wx.BOTTOM | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT,
                  border=5, pos=(2, 5))

    laydownViewerID = wx.NewId()
    self.frame.laydownViewer = SocietyViewer(self, laydownViewerID, 'laydownViewer', size=(200, 100),
                                 style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_MULTIPLE, log=self.log, inclComponents=False)
    laydownDropTarget = CougaarDropTarget(self.frame.laydownViewer, self.log, self.frame)
    self.frame.laydownViewer.SetDropTarget(laydownDropTarget)
    wx.EVT_LEFT_DOWN(self.frame.laydownViewer, self.OnLeftDown)

    sizer.Add(self.frame.laydownViewer, flag=wx.EXPAND, pos=(3,4), rowspan=2, colspan=2)

    ### Event handlers for various
    wx.EVT_TREE_BEGIN_LABEL_EDIT(self, agentViewerID, self.OnBeginLabelEdit) #fired by call to wx.TreeCtrl.EditLabel()
    wx.EVT_TREE_BEGIN_LABEL_EDIT(self, laydownViewerID, self.OnBeginLabelEdit) #fired by call to wx.TreeCtrl.EditLabel()
    wx.EVT_TREE_END_LABEL_EDIT(self, agentViewerID, self.OnEndLabelEdit) #fired by call to wx.TreeCtrl.EditLabel()
    wx.EVT_TREE_END_LABEL_EDIT(self, laydownViewerID, self.OnEndLabelEdit) #fired by call to wx.TreeCtrl.EditLabel()
    wx.EVT_TREE_SEL_CHANGED(self.frame.agentViewer, agentViewerID, self.OnSelChanged)
    wx.EVT_TREE_SEL_CHANGED(self.frame.laydownViewer, laydownViewerID, self.OnSelChanged)
    wx.EVT_TREE_SEL_CHANGING(self.frame.agentViewer, agentViewerID, self.OnSelChanging)
    wx.EVT_TREE_SEL_CHANGING(self.frame.laydownViewer, laydownViewerID, self.OnSelChanging)
    wx.EVT_RIGHT_DOWN(self.frame.agentViewer, self.OnRightDown)  # emits a wx.MouseEvent
    wx.EVT_RIGHT_DOWN(self.frame.laydownViewer, self.OnRightDown)  # emits a wx.MouseEvent
    wx.EVT_RIGHT_UP(self.frame.agentViewer, self.OnRightUp)  # emits a wx.MouseEvent
    wx.EVT_RIGHT_UP(self.frame.laydownViewer, self.OnRightUp)  # emits a wx.MouseEvent
    wx.EVT_LEFT_UP(self.frame.agentViewer, self.OnLeftUp)  # emits a wx.MouseEvent
    wx.EVT_LEFT_UP(self.frame.laydownViewer, self.OnLeftUp)  # emits a wx.MouseEvent
    wx.EVT_MOTION(self.frame.laydownViewer, self.OnMotion)  # emits a wx.MouseEvent
    wx.EVT_MOTION(self.frame.agentViewer, self.OnMotion)  # emits a wx.MouseEvent

    ###

    self.bg_bmp = images.getGridBGBitmap()
    wx.EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

    sizer.AddSpacer(10,10, pos=(1,6)) # adds a constant size space along the right edge
    sizer.AddSpacer(10,10, pos=(5,1)) # adds a constant size space along the bottom
    sizer.AddGrowableCol(1) # makes rule styled text box and Society Viewer expand to the right on window resize
    sizer.AddGrowableCol(4) # makes rule styled text box and Society Viewer expand to the right on window resize
    sizer.AddGrowableRow(3) # makes Society Viewer expand downward on window resize

    self.SetSizer(sizer)
    self.SetAutoLayout(True)

  #------------------------------------------------------------
  ### event callbacks

  def OnOpenSociety(self, event):
    if self.currentViewer == self.frame.agentViewer:
      self.openAgentList()
    else:
      self.openHnaMap()

  def OnOpenAgentList(self, evt):
    self.openAgentList()
    self.currentViewer = self.frame.agentViewer
    self.frame.currentTree = self.currentViewer

  def openAgentList(self):
    self.frame.openSocietyFile(self, "agentSociety")
    if self.frame.mappedSocietyOpen:
      self.distroAgentsButton.Enable(True)

  def OnOpenHnaMap(self, event):
    self.openHnaMap()
    self.currentViewer = self.frame.laydownViewer
    self.frame.currentTree = self.currentViewer

  def openHnaMap(self):
    self.openingHnaMap = True
    self.frame.openSocietyFile(self, "mappedSociety")

  def openTempAgentSociety(self):
    self.frame.agentSociety = Society("TempSociety", "Auto-Create")
    tempHost = self.frame.agentSociety.add_host("TempHost", "Auto-Create")
    tempNode = tempHost.add_node("TempNode", "Auto-Create")
    self.frame.agentViewer.UpdateControl(self.frame.agentSociety)
    self.frame.agentViewer.expandNodes()
    self.frame.enableAgentSocietySaveMenuItems()
    self.frame.agentSocietyOpen = True

  def StartAnimation(self):
    self.gizmo.Start()

  def StopAnimation(self):
    self.gizmo.Rest()

  #------------------------------------------------------------

  def OnSaveHnaMap(self, event):
    self.frame.saveSociety("mappedSociety")

  def OnCloseAgentSociety(self, evt):
    self.resetAgentSociety()
    self.frame.closeSociety("agentSociety")
    self.agentViewerTotalLabel.SetLabel('Total Agents: 0')
    self.distroAgentsButton.Enable(False)
    if self.inclNodesCheckbox.IsChecked():
      self.checkInclNodes(False)

  def OnCloseHnaMap(self, evt):
    self.resetMappedSociety(True)  # 'True' means save the agents
    self.laydownViewerTotalLabel.SetLabel('Total Agents: 0')
    self.currentViewer.removeDisplayedFacet('host', 'all')
    self.currentViewer.removeDisplayedFacet('node', 'all')
    self.currentViewer.removeDisplayedFacet('agent', 'all')
    # Remove text elements from TreeItemLabel objects
    self.currentViewer.clearAllLabels(self.currentViewer.GetRootItem())
    #~ self.currentViewer.clearAllLabels()  # this one doesn't work
    self.frame.closeSociety("mappedSociety")
    self.distroAgentsButton.Enable(False)
    self.frame.societyEditor.enableButton("getHnaMapButton", False)

  def OnUpdate(self, event):
    #self.log.WriteText("Stop time: %s\n" % time.ctime())
    self.StopAnimation()
    self.frame.server.Stop()
    if self.openingHnaMap:
      self.frame.mappedSociety = event.msg
      if self.frame.mappedSociety:
        self.frame.mappedSociety.isDirty = False
        self.UpdateControl(self.frame.mappedSociety)
        self.frame.enableHnaSaveMenuItems()
        if self.frame.agentSocietyOpen:
          self.distroAgentsButton.Enable(True)
        else:
          # Open a temp society in agentViewer as a holding area for unassigned nodes & agents
          self.openTempAgentSociety()
        self.frame.societyEditor.enableButton("getHnaMapButton")
    else:
      self.frame.agentSociety = event.msg
      if self.frame.agentSociety:
        self.frame.agentSociety.isDirty = False
        self.UpdateControl(self.frame.agentSociety)
        self.frame.enableAgentSocietySaveMenuItems()

  def UpdateControl(self, society):
    if society == self.frame.mappedSociety or society == self.tempMappedSociety:
      self.frame.laydownViewer.UpdateControl(society)
      self.laydownViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.laydownViewer.society.countAgents()))
      if society == self.frame.mappedSociety:
        self.frame.mappedSocietyOpen = 1
        self.openingHnaMap = False  # reset
    elif society == self.frame.agentSociety or society == self.tempAgentSociety:
      print "Society Viewer",  self.frame.agentViewer
      self.frame.agentViewer.UpdateControl(society)
      self.frame.agentViewer.expandEntireSociety()
      self.agentViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.agentViewer.society.countAgents()))
      self.frame.agentSocietyOpen = 1
    if self.frame.agentSocietyOpen and self.frame.mappedSocietyOpen:
      self.setSpinnerValue()
      if self.frame.agentSociety.name == self.frame.mappedSociety.name:
        # This is necessary when we open the same society in both viewers...we must be
        # able to drag and drop entities from one viewer to the other and recognize
        # the entities as being from outside the drop target society.  We need this to
        # determine if the entity is a real duplicate or simply a temporary duplicate
        # (moving within the same society).  The below name change will be transparent
        # to the user.
        self.frame.agentSociety.rename(self.frame.agentSociety.name + "_SRC")

  #--------------------------------------------------------------------------------------------------

  def OnBuildHnaMap(self, event):
    self.societyName = None
    self.numHostsToCreate = None
    self.hostNamePrefix = None
    self.hostNameSeqStart = None
    self.numNodesToCreate = None
    self.nodeNamePrefix = None
    self.nodeNameSeqStart = None
    self.resetMappedSociety()  # empty the Undo buffer
    # Get user input using a dialog box
    CreateHnaMapDialog(self, self.frame.mappedSociety)  # populates the variables listed above

    # Now create hosts and/or nodes, and/or allocate nodes to hosts
    successful = False
    if self.societyName is None or len(self.societyName) == 0:
      self.societyName = "HNA_Society"  # default value
    if self.numHostsToCreate is not None and self.numHostsToCreate > 0:
      if self.frame.mappedSociety is None:
        self.frame.mappedSociety = Society(self.societyName)
      hostNameSeq = str(self.hostNameSeqStart)

      # Create the hosts
      for i in range(self.numHostsToCreate):
        hostName = str(self.hostNamePrefix + hostNameSeq)
        self.frame.mappedSociety.add_host(Host(hostName, 'AUTO-BUILT'))
        if len(hostNameSeq) > 0:
          hostNameSeq = self.nextSeq(hostNameSeq)
      successful = True
    if self.numNodesToCreate is not None and self.numNodesToCreate > 0:
      # If we want to create nodes but there's not society with hosts yet, create a society and add one host
      if self.frame.mappedSociety is None:
        self.frame.mappedSociety = Society(self.societyName)
      nodeNameSeq = str(self.nodeNameSeqStart)
      numHosts = self.frame.mappedSociety.countHosts()
      if numHosts == 0:
        # if there are no hosts, create one
        self.frame.mappedSociety.add_host(Host('host1', 'AUTO-BUILT'))
        numHosts = 1

      # Now create the nodes
      # First, establish the number of nodes we want on each host before we start doubling up
      numUncreatedNodes = self.numNodesToCreate
      nodePopulationCount = 0
      while numUncreatedNodes > 0:
        for index in range(numHosts):
          if index == 0:
            nodePopulationCount += 1
          host = self.frame.mappedSociety.get_host(index)
          if host.countNodes() < nodePopulationCount:
            nodeName = str(self.nodeNamePrefix + nodeNameSeq)
            host.add_node(Node(nodeName, 'AUTO-BUILT'))
            numUncreatedNodes -= 1
            if numUncreatedNodes <= 0:
              break
            if len(nodeNameSeq) > 0:
              nodeNameSeq = self.nextSeq(nodeNameSeq)
      successful = True
    if successful:
      self.UpdateControl(self.frame.mappedSociety)
      self.frame.mappedSocietyOpen = True
      self.frame.enableHnaSaveMenuItems()
      self.frame.societyEditor.enableButton("getHnaMapButton")
      if self.frame.agentSocietyOpen:
        if self.frame.agentSociety.countAgents() > 0 or \
            (self.inclNodeCheckbox.IsChecked() and self.frame.agentSociety.countNodes() > 0):
          self.distroAgentsButton.Enable(True)

  def nextSeq(self, seqChar):
    # Sequence could be digits (1, 2, 3, ...), or
    # letters (A, B, C, ... Z, AA, AB, ... AZ, BA, BB, etc.)
    # seqChar is type 'string'
    needsDash = False
    useLowerCase = False
    if seqChar is None:
      return "0"
    if seqChar[0] == "-":
      seqChar = seqChar[1:]  # strip off the dash
      needsDash = True  # so we can add it back later
    if seqChar.isdigit():
      width = len(seqChar)
      newSeqChar = str(int(seqChar) + 1).zfill(width)
    else:
      newSeqChar = ''
      index = -1
      for i in range(len(seqChar)):
        newChar = chr(ord(seqChar[index]) + 1)
        if newChar == '[':
          newChar = 'A'
        elif newChar == '{':
          newChar = 'a'
          useLowerCase = True
        newSeqChar = newChar + newSeqChar
        if newChar.upper() == 'A':
          if len(seqChar) > (i + 1):  # if there's a previous char
            index -= 1
          else:
            if useLowerCase:
              addChar = 'a'
            else:
              addChar = 'A'
            newSeqChar = addChar + newSeqChar
            break
        else:
          newSeqChar = seqChar[:index] + newSeqChar
          break
    if needsDash:
      # add the dash back in if there was one
      newSeqChar = "-" + newSeqChar
    return newSeqChar

  #--------------------------------------------------------------------------------------------------

  def OnDistroAgents(self, event):
    #Save a copy of the current view to allow "undo"
    # First, if we're already working with a copy, assume the user is making an
    # additional allocation from a newly opened society to the same mappedSociety
    # previously allocated to.  Make the copy mappedSociety the permanent mappedSociety,
    # then save that in the undoBuffer, essentially making previous edits permanent
    if len(self.frame.undoBuffer) > 0 and self.tempMappedSociety is not None:
      self.frame.undoBuffer.pop()  # remove current contents in prep for new
      self.resetAgentSociety()
      self.resetMappedSociety()
    self.tempMappedSociety = self.frame.mappedSociety.clone()
    self.tempAgentSociety = self.frame.agentSociety.clone()
    self.frame.undoBuffer.insert(0, [self, [self.frame.laydownViewer, self.frame.mappedSociety],
                                                   [self.frame.agentViewer, self.frame.agentSociety]])
    self.frame.mainmenu.Enable(self.frame.UNDO, True)

    # Check the 'Include Nodes' checkbox to see if we'll be moving nodes or agents
    includeNodes = self.inclNodesCheckbox.IsChecked()

    if self.rb.GetSelection() == DISTRO_BY_FACET:
      FacetDistroDialog(self, self.tempAgentSociety, self.tempMappedSociety, includeNodes)
    else:
      entitiesPerHost = 0  # entities could be either nodes or agents
      nodesPerHost = 0  # only used when entities are agents
      if includeNodes:
        entitiesPerHost = self.nodeSpinner.GetValue()
      else:
        entitiesPerHost = self.agentSpinner.GetValue()
        nodesPerHost = self.nodeSpinner.GetValue()
        if not self.validInput(nodesPerHost):  # ensure it's an int greater than zero
          return
      if not self.validInput(entitiesPerHost):  # ensure it's an int greater than zero
        return
      self.hostIndex = 0
      self.hostOffset = 0  # need this because some hosts may be excluded
      self.entityIndex = 0
      self.entityOffset = 0  # need this because some entities may be excluded
      # update count of agents in agentSociety and hosts in mappedSociety:
      onlyIfIncluded = True
      hostCount = self.tempMappedSociety.countHosts(onlyIfIncluded)

      self.entityList = []  # a list of the things (nodes or agents) that we're allocating
      if includeNodes:
        self.entityList = self.tempAgentSociety.get_node_list(onlyIfIncluded)  # get the list of nodes to allocate
      else:
        self.entityList = self.tempAgentSociety.get_agent_list(False, onlyIfIncluded)  # get the list of agents to allocate
      entityCount = len(self.entityList)
      if entityCount == 0:
        return

      # User elects to evenly distribute entities
      if self.rb.GetSelection() == DISTRO_EVENLY:
        # Figure out how many entities to put on each host
        grossEntitiesPerHost, numEntitiesUnassigned = divmod(entityCount, hostCount)
        while self.hostIndex - self.hostOffset < numEntitiesUnassigned: # e.g., let's say 10 entities are unassigned
          if includeNodes:
            self.allocateNodes(grossEntitiesPerHost + 1, entityCount, None)  # add an extra entity to the first 10 hosts (0-9)
          else:
            self.allocateAgents(grossEntitiesPerHost + 1, nodesPerHost, entityCount)  # add an extra agent to the first 10 hosts (0-9)
        else:  # allocate agents to remaining hosts (after the first 10)
          while self.hostIndex - self.hostOffset < hostCount and self.entityIndex - self.entityOffset < entityCount:
            if includeNodes:
              self.allocateNodes(grossEntitiesPerHost, entityCount, None)
            else:
              self.allocateAgents(grossEntitiesPerHost, nodesPerHost, entityCount)

      # User elects to specify number of entities per host
      elif self.rb.GetSelection() == SPECIFY_NUM:
        hostsNeeded, numEntitiesUnassigned = divmod(entityCount, entitiesPerHost)
        if numEntitiesUnassigned > 0:
          hostsNeeded += 1
        if hostsNeeded > hostCount:
          # we ran out of hosts before running out of entities
          entityCount = entitiesPerHost * hostCount  # limit the number of entities allocated
        else:
          hostCount = hostsNeeded  # we'll only use this many hosts
        while self.hostIndex - self.hostOffset < hostCount and self.entityIndex - self.entityOffset < entityCount:
          if includeNodes:
            self.allocateNodes(entitiesPerHost, entityCount, None)
          else:
            self.allocateAgents(entitiesPerHost, nodesPerHost, entityCount)

      # User elects to maintain current distribution of nodes (only works when "incl nodes" is checked)
      elif self.rb.GetSelection() == SAME_DISTRO:
        if self.tempAgentSociety.countHosts() > self.tempMappedSociety.countHosts(onlyIfIncluded):
          msg = "To maintain current Node distribution, the HNA Map must contain at least as many hosts as the Agent List."
          dlg = wx.MessageDialog(self, msg, "Unable to comply", wx.OK | wx.ICON_EXCLAMATION)
          dlg.ShowModal()
          return
        for host in self.tempAgentSociety.each_host():
          entitiesPerHost = host.countNodes(onlyIfIncluded)
          # Note that, below, we are transferring host facets along with the node(s):
          self.allocateNodes(entitiesPerHost, entityCount, host.get_facets())

    self.UpdateControl(self.tempMappedSociety)  # update the treeCtrl
    self.frame.laydownViewer.expandEntireSociety()
    self.UpdateControl(self.tempAgentSociety)
    if includeNodes and self.tempAgentSociety.countNodes() == 0:
      self.distroAgentsButton.Enable(False)
    elif not includeNodes and self.tempAgentSociety.countAgents() == 0:
      self.distroAgentsButton.Enable(False)

  def allocateNodes(self, numNodesPerHost, nodeCount, facetList):
    host = None
    while host is None or host.isExcluded:
      # cycle through hosts till we find one that's not excluded
      if host is not None:
        self.hostIndex += 1
        self.hostOffset += 1
      host = self.tempMappedSociety.get_host(self.hostIndex)
      # bring over facets from the original host to the host to which the nodes are allocated
      if facetList is not None and len(facetList) > 0 and not self.ignoreHostFacetsCheckbox.IsChecked():
        host.add_facets(facetList)
    i = 0
    while i < numNodesPerHost and self.entityIndex - self.entityOffset < nodeCount:
      node = self.entityList[self.entityIndex]
      while node.isExcluded:
        # cycle through nodes till we find one that's not excluded
        self.entityIndex += 1
        self.entityOffset += 1
        node = self.entityList[self.entityIndex]
      mappedNode = None
      if self.tempMappedSociety.has_node(node.name):
        # don't bring the node, but check its agents...bring 'em if not already there
        mappedNode = self.tempMappedSociety.get_node(node.name)
        for agent in node.each_agent():
          if not agent.isExcluded and not self.tempMappedSociety.has_agent(agent.name):
            mappedNode.add_agent(agent.clone(False, mappedNode))
      else:
        # bring the node, but only bring those agents not already there
        mappedNode = node.clone(False, host)
        for agent in mappedNode.each_agent():
          if self.tempMappedSociety.has_agent(agent.name) or agent.isExcluded:
            mappedNode.delete_agent(agent)
            if agent.isExcluded:
              # Find a node in agentSociety called localnode and put the excluded agent there.
              localnode = node.parent.get_node_by_name('localnode')
              if localnode is None:
                # if there isn't one, create it
                newNodeName = 'localnode-' + node.parent.name
                localnode = node.parent.add_node(newNodeName)
              isTempDupe = True
              localnode.add_agent(agent, None, isTempDupe)
        host.add_node(mappedNode)
      self.tempAgentSociety.remove_node(node)
      i += 1
      self.entityIndex += 1
      if i >= (numNodesPerHost):
        break
    self.hostIndex += 1

  def allocateAgents(self, numAgentsPerHost, nodesPerHost, agentCount):
    host = None
    onlyIfIncluded = True
    while host is None or host.isExcluded:
      if host is not None:
        self.hostIndex += 1
        self.hostOffset += 1
      host = self.tempMappedSociety.get_host(self.hostIndex)
    for i in range(nodesPerHost - host.countNodes(onlyIfIncluded)):
      # Add one or more nodes if we need 'em
      node = host.add_node(host.name + "_NODE_" + str(i))
    nodeList = host.get_nodes(onlyIfIncluded)
    i = 0
    while i < numAgentsPerHost and self.entityIndex < agentCount:
      for node in nodeList:
        agent = self.entityList[self.entityIndex]
        if not self.tempMappedSociety.has_agent(agent.name) and not agent.isExcluded:
          # only bring the agent if it's not already in the mappedSociety
          node.add_agent(agent.clone(False, node))
        if not agent.isExcluded:
          self.tempAgentSociety.remove_agent(agent)
        i += 1
        self.entityIndex += 1
        if i >= (numAgentsPerHost):
          break
    self.hostIndex += 1

  def validInput(self, anInputValue):
    if type(anInputValue) != IntType or anInputValue <= 0:
      dlg = wx.MessageDialog(self, 'Agents per Host and Nodes per Host values must be integers greater than zero.',
              'Input Error', wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      return False
    return True

  #--------------------------------------------------------------------------------------------------

  def OnInclNodesChecked(self, event):
    if self.inclNodesCheckbox.IsChecked():
      self.checkInclNodes()
    else:
      self.checkInclNodes(False)

  #--------------------------------------------------------------------------------------------------

  def OnIgnoreHostFacetsChecked(self, event):
      pass

  #--------------------------------------------------------------------------------------------------

  def OnEvtRadioBox(self, event):
    if self.rb.GetSelection() == DISTRO_EVENLY:
      self.agentSpinner.Enable(False)
      if self.inclNodesCheckbox.IsChecked():
        self.nodeSpinner.Enable(False)
    elif self.rb.GetSelection() == SPECIFY_NUM:
      if self.inclNodesCheckbox.IsChecked():
        self.nodeSpinner.Enable(True)
      else:
        self.agentSpinner.Enable(True)
    elif self.rb.GetSelection() == DISTRO_BY_FACET:
      self.agentSpinner.Enable(False)
    elif self.rb.GetSelection() == SAME_DISTRO:
      self.agentSpinner.Enable(False)
      self.nodeSpinner.Enable(False)

  #--------------------------------------------------------------------------------------------------

  def OnSize(self, event):
    w,h = self.GetClientSizeTuple()
    self.list.SetDimensions(0, 0, w, h)

  #--------------------------------------------------------------------------------------------------

  def OnSelChanging(self, event):
    self.frame.editMenu.Enable(16, False)

  #--------------------------------------------------------------------------------------------------

  def OnSelChanged(self, event):
    # Turns out that OnSelChanged event is issued before OnRightDown and OnRightUp,
    # so to ensure we've got currentViewer, currentTree, and currentItem properly set,
    # we'd better set them here.
    #~ print "OnSelChanged"  # debug
    self.currentViewer = event.GetEventObject()
    self.frame.currentTree = self.currentViewer
    self.currentItem = event.GetItem()
    if self.currentItem.IsOk():
      if self.currentViewer.GetItemTextColour(self.currentItem) != wx.WHITE:
        self.currentViewer.removeHighlighting(self.currentItem)
      self.entityObj = self.getEntityObj()
      if not self.entityObj:
        event.Skip()
        return

      name = self.entityObj.name
      self.log.WriteText("Selected item: %s   " % name)
      self.log.WriteText("Rule: %s\n" % self.entityObj.rule)
      #~ self.log.WriteText("Selected item:  ")  # prg debug
      #~ self.log.WriteText(str(self.entityObj))  # prg debug
      #~ self.log.WriteText("\n")  # prg debug
      self.frame.editMenu.Enable(16, True)
    event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnRightDown(self, event):
    #~ print "OnRightDown"  # debug
    self.currentViewer = event.GetEventObject()
    self.frame.currentTree = self.currentViewer
    pt = event.GetPosition();
    item, flags = self.currentViewer.HitTest(pt)
    if item:
      self.currentViewer.SelectItem(item)
    # 'event' is an instance of wx.MouseEvent
    # NOTE: It seems that we need to catch and handle this event.  Without it, we
    # must double-right click on a tree item to get the wx.EVT_RIGHT_UP event to fire.
    #~ event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnRightUp(self, event):
    self.currentViewer = event.GetEventObject()  # may not need this here
    self.frame.currentTree = self.currentViewer  # may not need this here
    pt = event.GetPosition();
    item, flags = self.currentViewer.HitTest(pt)
    if item.IsOk():  # need this to prevent sys crash when tree has no items
      self.entityObj = self.currentViewer.GetPyData(item)
    else:
      self.entityObj = None
    if item.IsOk() or self.currentViewer.isEmptyTree():
      menu = self.SetMenu()
      self.currentViewer.PopupMenu(menu, pt)
      menu.Destroy()
    event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnLeftDown(self, event):
    self.itemGrabbed = False  # reset
    self.currentViewer = event.GetEventObject()
    self.frame.currentTree = self.currentViewer
    pt = event.GetPosition();
    item, flags = self.currentViewer.HitTest(pt)
    self.itemGrabbed = (flags == 16 or flags == 64 or flags == 2112 or \
                        flags == 4112 or flags == 4160)
    # wx.Python is not selecting an item till LeftUp, but there is no LeftUp when
    # we're dragging, leaving nothing selected during the drag.  The next
    # couple lines of code force a selection (Windows only).
    if wx.Platform == '__WXMSW__':
      if self.itemGrabbed:
        self.currentViewer.SelectItem(item)
    if item.IsOk():  # need this to prevent sys crash when tree has no items
      self.entityObj = self.currentViewer.GetPyData(item)
    event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnLeftUp(self, event):
    #~ # Need the following line to ensure that currentViewer changes to the drop target viewer
    #~ # when dragging from the other viewer.
    #~ self.currentViewer = event.GetEventObject()
    event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnMotion(self, event):
    if event.Dragging() and event.LeftIsDown() and self.itemGrabbed:
      self.currentViewer = event.GetEventObject()
      self.currentViewer.isDragSource = True
      selectedItemList = self.currentViewer.GetSelections()
      if len(selectedItemList) > 0:
        draggedItemList = []
        # Ensure all the objects selected are of the same type by comparing
        # their class with the class of the first item in the list
        counter = 0
        for item in selectedItemList:
          itemData = self.currentViewer.GetPyData(item)
          if counter == 0:
            draggedClass = itemData.__class__
          else:
            if itemData.__class__ != draggedClass:
              if self.currentViewer.IsVisible(item):
                return
              else:
                counter += 1
                continue
          draggedItemList.append([item, itemData])
          counter += 1
        self.log.WriteText("Dragging %d items\n" % len(draggedItemList))
        self.StartDrag([self.currentViewer, draggedItemList])
      else:
        print "WARNING: Attempting to drag but no items are selected"
    event.Skip()

  #--------------------------------------------------------------------------------------------------

  def OnBeginLabelEdit(self, event):
    label = self.currentViewer.GetItemText(self.currentItem)  # get the current label
    if label.hasTextElements() and not wx.Platform == '__WXMSW__':  # if facets are showing and it's a Linux box
      event.Veto()
      errorMsg = "Cannot rename while facets are displayed.\nPlease hide facets first."
      dlg = CougaarMessageDialog(self, "error", errorMsg)
      dlg.display()

  #--------------------------------------------------------------------------------------------------

  def OnEndLabelEdit(self, event):
    # NOTE:  When user finishes editing a label, the wx.EVT_TREE_END_LABEL_EDIT event is emitted
    # twice, at least under Linux  (not sure why), and it's apparently emitted while the first event has
    # not yet finished being handled.  This causes a Seg Fault in Linux when two modal wx.Dialogs are
    # open at the same time (which happens under certain circumstances...see code below).  So the
    # instance variable 'labelEditActivated' is meant to filter out the second event if the first event is
    # still being handled.
    if self.labelEditActivated:
      self.labelEditActivated = False

      if not event.IsEditCancelled():
        oldLabel = self.currentViewer.GetItemText(self.currentItem)  # still has the old label
        newLabel = self.currentViewer.toTreeItemLabel(event.GetLabel())
        entityType = self.currentViewer.GetPyData(self.currentItem).getType()

        if not self.currentViewer.getSociety().isDupeName(entityType, event.GetLabel()):
          self.currentViewer.editLabelText(oldLabel, newLabel)
          self.log.WriteText("Old label: " + oldLabel.getItemName() + \
                             "  New label: " + newLabel.getItemName() + "\n")
        else:
          event.Veto()
          errorMsg = "An entity with the name '" + event.GetLabel() + \
            "' already exists.\nPlease choose another name or press ESC to cancel edit."
          print errorMsg  # debug
          dlg = CougaarMessageDialog(self, "error", errorMsg)
          dlg.display()

    else:
      event.Veto()

    self.labelEditActivated = True

  #--------------------------------------------------------------------------------------------------

  def SetMenu(self):

    menu = wx.Menu()
    societyImage = images.getSocietyBitmap()
    hostImage = images.getHostBitmap()
    nodeImage = images.getNodeBitmap()
    agentImage = images.getAgentBitmap()

    if self.currentViewer.isEmptyTree():
      openSocMenuId = wx.NewId()
      item = wx.MenuItem(menu, openSocMenuId, "Open Society")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)
      createSocMenuId = wx.NewId()
      item = wx.MenuItem(menu, createSocMenuId, "Create New Society")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)
      wx.EVT_MENU(self, openSocMenuId, self.OnOpenSociety)
      wx.EVT_MENU(self, createSocMenuId, self.OnCreateSociety)
      return menu

    if isinstance(self.entityObj, Society):
      # we either want to add a host or delete the society and all its subs.
      addHostMenuId = wx.NewId()
      item = wx.MenuItem(menu, addHostMenuId, "Add Host")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      summaryMenuId = wx.NewId()
      item = wx.MenuItem(menu, summaryMenuId, "View Society Summary")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      delSocMenuId = wx.NewId()
      item = wx.MenuItem(menu, delSocMenuId, "Delete This Society")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      renameSocMenuId = wx.NewId()
      item = wx.MenuItem(menu, renameSocMenuId, "Rename Society")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      showSpecFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showSpecFacetsMenuId, "Show Specified Facets")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      showFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showFacetsMenuId, "Show All Facets")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('society')) > 0:
        if self.currentViewer.getDisplayedFacets('society')[0].find('all') > -1:
          item.Enable(False)

      hideAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, hideAllFacetsMenuId, "Hide All Society Facets")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('society')) == 0:
        item.Enable(False)

      editFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, editFacetsMenuId, "View/Edit Facets")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      addFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, addFacetMenuId, "Add Facet")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      deleteFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, deleteFacetMenuId, "Delete Facet")
      item.SetBitmap(societyImage)
      menu.AppendItem(item)

      wx.EVT_MENU(self, addHostMenuId, self.OnAddHost)
      wx.EVT_MENU(self, summaryMenuId, self.OnSummary)
      wx.EVT_MENU(self, delSocMenuId, self.OnDeleteSociety)
      wx.EVT_MENU(self, renameSocMenuId, self.OnRename)
      wx.EVT_MENU(self, addFacetMenuId, self.OnAddFacet)
      wx.EVT_MENU(self, deleteFacetMenuId, self.OnDeleteFacet)
      wx.EVT_MENU(self, editFacetsMenuId, self.OnEditFacets)
      wx.EVT_MENU(self, showSpecFacetsMenuId, self.OnShowSpecifiedSocietyFacets)
      wx.EVT_MENU(self, showFacetsMenuId, self.OnShowAllSocietyFacets)
      wx.EVT_MENU(self, hideAllFacetsMenuId, self.OnHideAllSocietyFacets)
      return menu

    if isinstance(self.entityObj, Host):
      # we either want to add a node or delete the host and all its subs.
      addNodeMenuId = wx.NewId()
      item = wx.MenuItem(menu, addNodeMenuId, "Add Node")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      summaryMenuId = wx.NewId()
      item = wx.MenuItem(menu, summaryMenuId, "View Society Summary")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      renameHostMenuId = wx.NewId()
      item = wx.MenuItem(menu, renameHostMenuId, "Rename Host")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      exclHostMenuId = wx.NewId()
      if self.currentViewer == self.frame.laydownViewer:
        if self.entityObj.isExcluded:
          item = wx.MenuItem(menu, exclHostMenuId, "Include Host in Distro")
        else:
          item = wx.MenuItem(menu, exclHostMenuId, "Exclude Host from Distro")
        item.SetBitmap(hostImage)
        menu.AppendItem(item)

      if "enclave" in self.currentViewer.getDisplayedFacets('host'):
        enclaveFacetMenuText = "Hide Enclave Facet"
      else:
        enclaveFacetMenuText = "Show Enclave Facet"
      showEncFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, showEncFacetMenuId, enclaveFacetMenuText)
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      if "service" in self.currentViewer.getDisplayedFacets('host'):
        serviceFacetMenuText = "Hide Service Facet"
      else:
        serviceFacetMenuText = "Show Service Facet"
      showServFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, showServFacetMenuId, serviceFacetMenuText)
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      showSpecFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showSpecFacetsMenuId, "Show Specified Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      showAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showAllFacetsMenuId, "Show All Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('host')) > 0:
        if self.currentViewer.getDisplayedFacets('host')[0].find('all') > -1:
          item.Enable(False)

      hideAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, hideAllFacetsMenuId, "Hide All Host Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('host')) == 0:
        item.Enable(False)

      editFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, editFacetsMenuId, "View/Edit Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      addFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, addFacetMenuId, "Add Facet")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      deleteFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, deleteFacetMenuId, "Delete Facet")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      copyFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, copyFacetsMenuId, "Copy Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      pasteFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, pasteFacetsMenuId, "Paste Facets")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)
      if self.facetClipboard is None or len(self.facetClipboard) == 0:
        item.Enable(False)

      delHostMenuId = wx.NewId()
      item = wx.MenuItem(menu, delHostMenuId, "Delete This Host")
      item.SetBitmap(hostImage)
      menu.AppendItem(item)

      wx.EVT_MENU(self, addNodeMenuId, self.OnAddNode)
      wx.EVT_MENU(self, summaryMenuId, self.OnSummary)
      wx.EVT_MENU(self, delHostMenuId, self.OnDeleteEntity)
      wx.EVT_MENU(self, renameHostMenuId, self.OnRename)
      wx.EVT_MENU(self, showEncFacetMenuId, self.OnShowEnclaveFacet)
      wx.EVT_MENU(self, showServFacetMenuId, self.OnShowServiceFacet)
      wx.EVT_MENU(self, hideAllFacetsMenuId, self.OnHideAllHostFacets)
      wx.EVT_MENU(self, addFacetMenuId, self.OnAddFacet)
      wx.EVT_MENU(self, deleteFacetMenuId, self.OnDeleteFacet)
      wx.EVT_MENU(self, showAllFacetsMenuId, self.OnShowAllHostFacets)
      wx.EVT_MENU(self, editFacetsMenuId, self.OnEditFacets)
      wx.EVT_MENU(self, exclHostMenuId, self.OnExcludeEntity)
      wx.EVT_MENU(self, copyFacetsMenuId, self.OnCopyFacets)
      wx.EVT_MENU(self, pasteFacetsMenuId, self.OnPasteFacets)
      wx.EVT_MENU(self, showSpecFacetsMenuId, self.OnShowSpecifiedHostFacets)
      return menu

    if isinstance(self.entityObj, Node):
      # we either want to add a agent or delete the node and all its subs.
      addAgentMenuId = wx.NewId()
      item = wx.MenuItem(menu, addAgentMenuId, "Add Agent")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      renameNodeMenuId = wx.NewId()
      item = wx.MenuItem(menu, renameNodeMenuId, "Rename Node")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      unassignNodeMenuId = wx.NewId()
      item = wx.MenuItem(menu, unassignNodeMenuId, "Unassign Node")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)
      if self.currentViewer == self.frame.agentViewer:
        item.Enable(False)

      exclNodeMenuId = wx.NewId()
      if self.entityObj.isExcluded:
        item = wx.MenuItem(menu, exclNodeMenuId, "Include Node in Distro")
      else:
        item = wx.MenuItem(menu, exclNodeMenuId, "Exclude Node from Distro")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      roleFacetMenuId = wx.NewId()
      if "role" in self.currentViewer.getDisplayedFacets('node'):
        roleFacetMenuText = "Hide Role Facet"
      else:
        roleFacetMenuText = "Show Role Facet"
      item = wx.MenuItem(menu, roleFacetMenuId, roleFacetMenuText)
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      showSpecFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showSpecFacetsMenuId, "Show Specified Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      showAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showAllFacetsMenuId, "Show All Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('node')) > 0:
        if self.currentViewer.getDisplayedFacets('node')[0].find('all') > -1:
          item.Enable(False)

      hideAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, hideAllFacetsMenuId, "Hide All Node Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('node')) == 0:
        item.Enable(False)

      editFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, editFacetsMenuId, "View/Edit Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      addFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, addFacetMenuId, "Add Facet")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      deleteFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, deleteFacetMenuId, "Delete Facet")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      copyFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, copyFacetsMenuId, "Copy Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      pasteFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, pasteFacetsMenuId, "Paste Facets")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)
      if self.facetClipboard is None or len(self.facetClipboard) == 0:
        item.Enable(False)

      delNodeMenuId = wx.NewId()
      item = wx.MenuItem(menu, delNodeMenuId, "Delete This Node")
      item.SetBitmap(nodeImage)
      menu.AppendItem(item)

      wx.EVT_MENU(self, addAgentMenuId, self.OnAddAgent)
      wx.EVT_MENU(self, delNodeMenuId, self.OnDeleteEntity)
      wx.EVT_MENU(self, renameNodeMenuId, self.OnRename)
      wx.EVT_MENU(self, unassignNodeMenuId, self.OnUnassign)
      wx.EVT_MENU(self, roleFacetMenuId, self.OnShowRoleFacet)
      wx.EVT_MENU(self, hideAllFacetsMenuId, self.OnHideAllNodeFacets)
      wx.EVT_MENU(self, addFacetMenuId, self.OnAddFacet)
      wx.EVT_MENU(self, deleteFacetMenuId, self.OnDeleteFacet)
      wx.EVT_MENU(self, editFacetsMenuId, self.OnEditFacets)
      wx.EVT_MENU(self, showAllFacetsMenuId, self.OnShowAllNodeFacets)
      wx.EVT_MENU(self, exclNodeMenuId, self.OnExcludeEntity)
      wx.EVT_MENU(self, copyFacetsMenuId, self.OnCopyFacets)
      wx.EVT_MENU(self, pasteFacetsMenuId, self.OnPasteFacets)
      wx.EVT_MENU(self, showSpecFacetsMenuId, self.OnShowSpecifiedNodeFacets)
      return menu

    if isinstance(self.entityObj, Agent):
      # we either want to add a component or delete the agent and all its subs.
      renameAgentMenuId = wx.NewId()
      item = wx.MenuItem(menu, renameAgentMenuId, "Rename Agent")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      unassignAgentMenuId = wx.NewId()
      item = wx.MenuItem(menu, unassignAgentMenuId, "Unassign Agent")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)
      if self.currentViewer == self.frame.agentViewer:
        item.Enable(False)

      exclAgentMenuId = wx.NewId()
      if self.currentViewer == self.frame.agentViewer:
        if self.entityObj.isExcluded:
          item = wx.MenuItem(menu, exclAgentMenuId, "Include Agent in Distro")
        else:
          item = wx.MenuItem(menu, exclAgentMenuId, "Exclude Agent from Distro")
        item.SetBitmap(agentImage)
        menu.AppendItem(item)

      showSpecFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showSpecFacetsMenuId, "Show Specified Facets")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      showAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, showAllFacetsMenuId, "Show All Facets")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('agent')) > 0:
        if self.currentViewer.getDisplayedFacets('agent')[0].find('all') > -1:
          item.Enable(False)

      hideAllFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, hideAllFacetsMenuId, "Hide All Agent Facets")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)
      if len(self.currentViewer.getDisplayedFacets('agent')) == 0:
        item.Enable(False)

      editFacetsMenuId = wx.NewId()
      item = wx.MenuItem(menu, editFacetsMenuId, "View/Edit Facets")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      addFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, addFacetMenuId, "Add Facet")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      deleteFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, deleteFacetMenuId, "Delete Facet")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      delAgentMenuId = wx.NewId()
      item = wx.MenuItem(menu, delAgentMenuId, "Delete This Agent")
      item.SetBitmap(agentImage)
      menu.AppendItem(item)

      wx.EVT_MENU(self, delAgentMenuId, self.OnDeleteEntity)
      wx.EVT_MENU(self, renameAgentMenuId, self.OnRename)
      wx.EVT_MENU(self, unassignAgentMenuId, self.OnUnassign)
      wx.EVT_MENU(self, hideAllFacetsMenuId, self.OnHideAllAgentFacets)
      wx.EVT_MENU(self, addFacetMenuId, self.OnAddFacet)
      wx.EVT_MENU(self, deleteFacetMenuId, self.OnDeleteFacet)
      wx.EVT_MENU(self, showAllFacetsMenuId, self.OnShowAllAgentFacets)
      wx.EVT_MENU(self, editFacetsMenuId, self.OnEditFacets)
      wx.EVT_MENU(self, exclAgentMenuId, self.OnExcludeEntity)
      wx.EVT_MENU(self, showSpecFacetsMenuId, self.OnShowSpecifiedAgentFacets)
      return menu

  #************************************************************************

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

  def GetBitmap(self, text):
    txt = str(text).lower()
    if txt == 'society':   return self.societyImage
    if txt == 'host':      return self.hostImage
    if txt == 'node':      return self.nodeImage
    if txt == 'agent':     return self.agentImage
    return self.questionImage

###

  def OnCreateSociety(self, event):
    self.newEntityName = None
    NewEntityDialog(self, "New Society:")  # assigns a value to the above variable
    if self.newEntityName is not None:
      self.createSociety()

  def OnAddHost(self, event):
    self.currentViewer.addHost(self.currentViewer.society)

  def OnAddNode(self, event):
    self.currentViewer.addNode(self.currentItem)

  def OnAddAgent(self, event):
    self.currentViewer.addAgent(self.currentItem)
    self.updateAgentCounter()

  def OnDeleteSociety(self, event):
    dlg = CougaarMessageDialog(self, "delete")
    self.KillIt = dlg.getUserInput()
    if self.KillIt == wx.ID_YES:
      society = None
      societyFile = None
      if self.currentViewer == self.frame.agentViewer:
        society = "agentSociety"
        societyFile = self.frame.agentSocietyFile
      else:
        society = "mappedSociety"
        societyFile = self.frame.societyHnaFile
      self.frame.closeSociety(society)
      # delete the XML file from disk:
      if societyFile is not None:
        os.remove(self.societyFile)

  def OnDeleteEntity(self, event):
    deletedItems = self.currentViewer.GetSelections()
    if self.currentViewer == self.frame.agentViewer or \
       self.currentViewer.GetPyData(deletedItems[0]).getType() == "agent":
      self.currentViewer.deleteEntity(deletedItems)
      self.updateAgentCounter()
    else:
      delete = True
      self.unassignEntity(delete)

  def OnRename(self, event):
    self.currentViewer.EditLabel(self.currentItem)

  def OnUnassign(self, event):
    self.unassignEntity()

  # -----------------------------------------------------------------------------

  def unassignEntity(self, delete=False):
    okToContinue = True
    selectedItems = self.currentViewer.GetSelections()

    # Verify that selected items are all of the same type
    selectedObjects = []
    for item in selectedItems:
      selectedObjects.append(self.currentViewer.GetPyData(item))
    itemsAreSameType = self.currentViewer.verifyMultiSelectTypes(selectedObjects)
    if not itemsAreSameType:
      return

    # Set up warning dialogs to warn user when he/she tries to delete an entity
    thisEntity = 'this entity'
    it = 'it'
    its = 'its'
    if len(selectedItems) > 1:
      thisEntity = 'these entities'
      it = 'them'
      its = 'their'
    if delete:
      msg = 'Deleting ' + thisEntity + ' will destroy ' + it + ', but ' + its + ' children '+ \
                '(if any)\nwill be moved to the Agent List window.\n\n' + \
                'Are you sure you want to continue?'
      dlg = CougaarMessageDialog(self, 'delete', msg)
      choice = dlg.getUserInput()
      if choice == wx.ID_NO:
        okToContinue = False

    if okToContinue:
      # Do some setup first
      # Just in case the user closed the agentSociety, check and open a new one, if nec.
      if not self.frame.agentSocietyOpen:
        self.openTempAgentSociety()
      # Is there a temp host?  If not, create one.
      self.frame.agentViewer.searchResultSet = []  # empty it out
      rootItem = self.frame.agentViewer.GetRootItem()
      tempHostItem, tempHost = self.frame.agentViewer.getItemByLabel("localhost", rootItem)
      if tempHostItem is None or not tempHostItem.IsOk():  # if the tempHost item wasn't found, add it
        tempHostItem = self.frame.agentViewer.PrependItem(rootItem, "localhost", self.hostImage)
        tempHost = self.frame.agentSociety.add_host("localhost", "Auto-Create")
        self.frame.agentViewer.SetPyData(tempHostItem, tempHost)

      # Now do the unassigning
      destParentItem = None
      for item in selectedItems:
        entity = self.currentViewer.GetPyData(item)
        if isinstance(entity, Host) or (isinstance(entity, Node) and not delete):
          destParentItem = tempHostItem
          destParentObj = self.frame.agentViewer.GetPyData(destParentItem)
          itemImage = self.nodeImage
        elif isinstance(entity, Agent) or (isinstance(entity, Node) and delete):
          destParentItem, destParentObj = self.frame.agentViewer.getItemByLabel("localnode", tempHostItem)
          itemImage = self.agentImage
          if not destParentItem or not destParentItem.IsOk():
            # looked for tempNode on tempHost but found none, so create it
            destParentItem = self.frame.agentViewer.PrependItem(tempHostItem, "localnode", self.nodeImage)
            destParentObj = tempHost.add_node("localnode", "Auto-Create")
            self.frame.agentViewer.SetPyData(destParentItem, destParentObj)
          # we've found (or created) a node
        self.currentViewer.Delete(item)  # delete from laydownViewer tree
        entity.remove_entity()  # remove from laydownViewer society model

        newItem = None
        if isinstance(entity, Host):
          for node in entity.each_node():
            destParentObj.add_entity(node)
            # add to agentViewer tree:
            nodeItem = self.frame.agentViewer.AppendItem(destParentItem, node.name, itemImage)
            self.frame.agentViewer.SetPyData(nodeItem, node)
            for agent in node.each_agent():
              newItem = self.frame.agentViewer.AppendItem(nodeItem, agent.name, self.agentImage)
              self.frame.agentViewer.SetPyData(newItem, agent)
        else:  # entity is either a Node or an Agent
          agents = []
          if isinstance(entity, Node) and not delete:  # unassigning a Node
            destParentObj.add_entity(entity)  # add to agentViewer society model
            # add to agentViewer tree:
            destParentItem = self.frame.agentViewer.AppendItem(destParentItem, entity.name, itemImage)
            self.frame.agentViewer.SetPyData(destParentItem, entity)
            agents = entity.get_agents()
          else:
            if delete:  # deleting a Node
              agents = entity.get_agents()
            elif isinstance(entity, Agent):  # unassigning an Agent
              agents.append(entity)
            for agent in agents:
              # Add to society model
              destParentObj = self.frame.agentViewer.GetPyData(destParentItem)
              destParentObj.add_agent(agent)
          for agent in agents:
            # Add to agentViewer tree:
            newItem = self.frame.agentViewer.AppendItem(destParentItem, agent.name, self.agentImage)
            self.frame.agentViewer.SetPyData(newItem, agent)
        if newItem is not None:
          self.frame.agentViewer.EnsureVisible(newItem)
      bothOfEm = True
      self.updateAgentCounter(bothOfEm)
      self.distroAgentsButton.Enable(True)

  # -----------------------------------------------------------------------------

  def OnSummary(self, event):
    SummaryDialog(self, self.currentViewer.society)

  # -----------------------------------------------------------------------------

  def OnShowEnclaveFacet(self, event):
    self.showFacet("enclave", "host")

  def OnShowServiceFacet(self, event):
    self.showFacet("service", "host")

  def OnShowRoleFacet(self, event):
    self.showFacet("role", "node")

  def OnShowSpecifiedSocietyFacets(self, event):
    facetDialog = ShowFacetSelectionDialog(self, self.currentViewer.society, 'society')
    if facetDialog.facetList:
      self.showFacet('', 'society', facetList=facetDialog.facetList)

  def OnShowAllSocietyFacets(self, event):
    self.showFacet('society-all', 'society')

  def OnShowSpecifiedHostFacets(self, event):
    facetDialog = ShowFacetSelectionDialog(self, self.currentViewer.society, 'host')
    if facetDialog.facetList:
      self.showFacet('', 'host', facetList=facetDialog.facetList)

  def OnShowAllHostFacets(self, event):
    self.showFacet('host-all', 'host')

  def OnShowSpecifiedNodeFacets(self, event):
    facetDialog = ShowFacetSelectionDialog(self, self.currentViewer.society, 'node')
    if facetDialog.facetList:
      self.showFacet('', 'node', facetList=facetDialog.facetList)

  def OnShowAllNodeFacets(self, event):
    self.showFacet('node-all', 'node')

  def OnShowSpecifiedAgentFacets(self, event):
    facetDialog = ShowFacetSelectionDialog(self, self.currentViewer.society, 'agent')
    if facetDialog.facetList:
      self.showFacet('', 'agent', facetList=facetDialog.facetList)

  def OnShowAllAgentFacets(self, event):
    self.showFacet('agent-all', 'agent')

  def OnHideAllSocietyFacets(self, event):
    self.showFacet('society-all', 'society', hideAll=True)

  def OnHideAllHostFacets(self, event):
    self.showFacet('host-all', 'host', hideAll=True)

  def OnHideAllNodeFacets(self, event):
    self.showFacet('node-all', 'node', hideAll=True)

  def OnHideAllAgentFacets(self, event):
    self.showFacet('agent-all', 'agent', hideAll=True)

  # -----------------------------------------------------------------------------

  def showFacet(self, facetType, entityType=None, update=False, hideAll=False, facetList=None, itemList = None):
    # Note: self.masterFacetList holds a list of all the 'facetType=value' pairs already specified by the user and displayed.
    updatingDroppedItem = False
    if itemList:  # indicates this is an update caused by a drag-and-drop operation
      updatingDroppedItem = True
    else:
      # Build a list of all the relevant items in the tree
      itemList = self.currentViewer.getItemList(entityType)
    facetsDisplayed = self.currentViewer.getDisplayedFacets(entityType)

    # Now either hide or show facets
    # Hide facets:
    if facetType in facetsDisplayed or hideAll:
      for item in itemList:  # for each item of the specified type (e.g., host,  node, etc.)
        label = self.currentViewer.GetItemText(item)  # label is a TreeItemLabel obj
        if hideAll:
          label.removeAllTextElements()
        else:
          label.removeTextElement(facetType)
        self.currentViewer.SetItemText(item, label)  # update the display
      if hideAll and not update:
        self.currentViewer.removeDisplayedFacet(entityType, 'all')
        self.currentViewer.masterFacetList = []  # empty it out
      elif not update:
        self.currentViewer.removeDisplayedFacet(entityType, facetType)
      if update:
        for facet in facetsDisplayed:
          # 'facet' is a String facet type
          self.displayFacet(facet, itemList)

    # Either we just added a facet to an entity or we just dropped an entity into a viewer
    # that had facets showing, so add facet display to the entity
    elif updatingDroppedItem:
      for facet in facetsDisplayed:
        # 'facet' is a String facet type
        if facet != 'specified':
          self.displayFacet(facet, itemList)
      if len(self.currentViewer.masterFacetList) > 0:
        # There are already some user-specified facets displayed.  Of the facets displayed, find those that
        # are present in the items in the itemList; display them.
        matchingItemList, facetDict = self.getMatchingFacetItems(self.currentViewer.masterFacetList, itemList)
        self.displayFacet('specified', matchingItemList, facetDict)

    # Show facets:
    else:
      # Show ALL facets.
      if facetType.endswith('all'):
        if len(facetsDisplayed) > 0:  # if some are showing already
          self.showFacet(facetType, entityType, hideAll=True)  # hide existing ones first
        self.currentViewer.addDisplayedFacet(entityType, facetType)  # just adds it to the list
        self.displayFacet(facetType, itemList)  # update the display

      else:
        # if ALL facets are currently displayed, hide them first
        for facet in facetsDisplayed:
          if facet.find('all') > -1:
            self.showFacet(facetType, entityType, hideAll=True)

        # Show user-specified facets
        if facetList:   # 'facetList' is a List of 'type=value' strings
          # Get the list of tree items that have the specified 'type=value' facet and a dictionary
          # that shows which 'type=value' facets each item has.
          matchingItemList, facetDict = self.getMatchingFacetItems(facetList, itemList)
          self.currentViewer.addDisplayedFacet(entityType, 'specified')
          self.displayFacet('specified', matchingItemList, facetDict)
          self.currentViewer.masterFacetList.extend(facetList)

        # Show only the menu-specified facet
        else:
          self.currentViewer.addDisplayedFacet(entityType, facetType)
          self.displayFacet(facetType, itemList)

  # --------------------------------------------------------------------------------

  def displayFacet(self, facetType, itemList, facetDict = None):
    for item in itemList:
      facetString = ""
      label = self.currentViewer.GetItemText(item)
      itemName = label.getItemName()
      entity = self.currentViewer.GetPyData(item)
      separator = ""
      valueList = []

      # Display user-specified facets
      if facetType == 'specified':
        if facetDict:
          # facetDict is a Dictionary where key is an item name and value is a List of 'type=value' Strings
          valueList = facetDict[itemName]

      # Display ALL facets
      elif facetType.endswith('all'):
        facetList = entity.get_facets()
        for facet in facetList:
          for facetPair in facet.each_facet_pair():
            valueList.append(facetPair)

      else:  # display only the menu-specified facet
        valueList = entity.get_facet_values(facetType)

      label.addTextElement(facetType, valueList)
      self.currentViewer.SetItemText(item, label)

  # --------------------------------------------------------------------------------

  def getMatchingFacetItems(self, facetList, itemList):
    # Returns a two-tuple consisting of a List of items that have one or more
    # of the facet types listed in facetList, and a Dictionary where the key
    # is an entity name and the value is a List of 'type=value' facet strings.

    matchingItemList = []
    facetDict = {}
    for item in itemList:
      itemAppended = False
      entity = self.currentViewer.GetPyData(item)
      itemName = self.currentViewer.GetItemText(item).getItemName()
      matchingFacetList = []
      for facet in facetList:
        facetElements = facet.split('=')
        facetType = facetElements[0]
        facetValue = facetElements[1]
        if facetValue == 'AnyValue':
          # Look for entities having this facetType
          valueList = entity.get_facet_values(facetType)
          if len(valueList) > 0:
            if not itemAppended:
              matchingItemList.append(item)
              itemAppended = True
            for value in valueList:
              matchingFacetList.append(facetType + '=' + value)
        else:
          # Look for entities with the facet pair
          if entity.has_facet(facet):
            if not itemAppended:
              matchingItemList.append(item)
              itemAppended = True
            matchingFacetList.append(facet)
      facetDict[itemName] = matchingFacetList
    return matchingItemList, facetDict


  #*******************************************************************

  def OnAddFacet(self, event):
    self.addDeleteFacet()

  #*******************************************************************

  def OnDeleteFacet(self, event):
    self.addDeleteFacet('delete')

  #*******************************************************************

  def addDeleteFacet(self, action='add'):
    entityObjList = self.currentViewer.getSelectedObjects()
    AddDeleteFacetDialog(self, self.currentViewer.society, entityObjList, action)

  #*******************************************************************

  def OnEditFacets(self, event):
    FacetDisplayDialog(self, self.log)

  #*******************************************************************

  def OnExcludeEntity(self, event):
    selectedItems = self.currentViewer.GetSelections()

    for item in selectedItems:
      entity = self.currentViewer.GetPyData(item)
      if isinstance(entity, Host) or isinstance(entity, Node) or isinstance(entity, Agent):

        if entity.isExcluded:   # re-include it

          if self.currentViewer.GetItemBackgroundColour(item) == wx.RED:
            # unmark the tree item label of the selected hosts
            self.currentViewer.SetItemBackgroundColour(item, wx.WHITE)
            self.currentViewer.SetItemTextColour(item, wx.BLACK)
          # mark the host objects as included again
          entity.isExcluded = False

        else:  # exclude it
          # mark the tree item labels of the hosts excluded
          self.currentViewer.SetItemBackgroundColour(item, wx.RED)
          self.currentViewer.SetItemTextColour(item, wx.WHITE)

          # mark the host objects as excluded so we don't give them agents
          entity.isExcluded = True
      else:
        self.log.WriteText("Exclude operation failed: can only exclude hosts, nodes, and agents")
    self.currentViewer.UnselectAll()  # removes the selection highlight so we can see item color

    self.setSpinnerValue()  # update value now that there may be fewer hosts

  #*******************************************************************

  def OnCopyFacets(self, event):
    selectedEntities = self.currentViewer.GetSelections()
    if len(selectedEntities) > 1:
      errorMsg = "Facets can only be copied from one entity at a time."
      dlg = CougaarMessageDialog(self, "error", errorMsg)
      dlg.display()
      return
    self.facetClipboard = []  # initialize it/clear it out
    for entity in selectedEntities:  # there will only be one entity
      selectedEntity = self.currentViewer.GetPyData(entity)
      # facetClipboard is a List of Facet objects
      self.facetClipboard = selectedEntity.get_facets()

  #*******************************************************************

  def OnPasteFacets(self, event):
    selectedItems = self.currentViewer.GetSelections()
    entity = None
    # Now, facetClipboard is a List of Facet objects or facet Strings
    for item in selectedItems:
      entity = self.currentViewer.GetPyData(item)
      entity.add_facets(self.facetClipboard)
    # Update the item label facet display, if it's showing:
    entityType = entity.getType()
    facetType = entityType + '-all'
    self.showFacet(facetType, entityType, True)

  #*******************************************************************

  def createSociety(self):
    newSociety = Society(str(self.newEntityName), "Hand edit")
    if self.currentViewer == self.frame.agentViewer:
      self.frame.agentSociety = newSociety
      self.frame.agentSocietyOpen = True
      self.frame.enableAgentSocietySaveMenuItems()
    elif self.currentViewer == self.frame.laydownViewer:
      self.frame.mappedSociety = newSociety
      self.frame.mappedSocietyOpen = True
      self.frame.mappedSocietySaveCounter = 0
      self.frame.enableHnaSaveMenuItems()
    newSociety.isDirty = True
    self.UpdateControl(newSociety)

  #*******************************************************************

  def getEntityObj(self, item=None):
    if item is None:
      item = self.currentItem
    return self.currentViewer.GetPyData(item)

  #----------------------------------------------------------------------

  def setSpinnerValue(self):
    if self.frame.agentSociety and self.frame.mappedSociety:
      self.minAgentsPerHost = 1
      onlyIfIncluded = True
      agentCount = self.frame.agentSociety.countAgents(onlyIfIncluded)
      hostCount = self.frame.mappedSociety.countHosts(onlyIfIncluded)
      if agentCount > 0 and hostCount > 0:
        self.minAgentsPerHost = float(agentCount) / float(hostCount)
        # Round up:
        if self.minAgentsPerHost > math.floor(self.minAgentsPerHost):
          self.minAgentsPerHost += 1
      self.agentSpinner.SetRange(int(self.minAgentsPerHost), agentCount)
      self.agentSpinner.SetValue(int(self.minAgentsPerHost))

  #----------------------------------------------------------------------

  def undo(self, lastState):
    if isinstance(lastState[1][0], SocietyViewer):
      i = 1
      while i < len(lastState):
        lastState[i][0].UpdateControl(lastState[i][1])
        lastState[i][0].expandEntireSociety()
        #~ lastState[i][0].hostFacetsDisplayed = []
        lastState[i][0].removeDisplayedFacet('host', 'all')
        #~ lastState[i][0].nodeFacetsDisplayed = []
        lastState[i][0].removeDisplayedFacet('node', 'all')
        #~ lastState[i][0].agentFacetsDisplayed = []
        lastState[i][0].removeDisplayedFacet('agent', 'all')
        i += 1
      if self.frame.agentSocietyOpen and self.frame.mappedSocietyOpen:
        self.tempAgentSociety.close()
        self.tempAgentSociety = None
        self.tempMappedSociety.close()
        self.tempMappedSociety = None
        self.distroAgentsButton.Enable(True)
      bothOfEm = True
      self.updateAgentCounter(bothOfEm)
    else:
      self.log.WriteText("Unable to undo last edit\n")

  #----------------------------------------------------------------------

  def resetAgentSociety(self):
    if self.frame.agentSociety is not None and self.tempAgentSociety is not None:
      self.frame.agentSociety.close()
      self.frame.agentSociety = self.tempAgentSociety
      self.tempAgentSociety = None

  #----------------------------------------------------------------------

  def resetMappedSociety(self, saveAgents=False):
    if self.frame.mappedSociety is not None and self.tempMappedSociety is not None:
      self.frame.mappedSociety.close(saveAgents)
      self.frame.mappedSociety = self.tempMappedSociety
      self.tempMappedSociety = None

  #----------------------------------------------------------------------

  def StartDrag(self, dataList):

    # The 'dataList' argument is a list, the first element of which is a reference to the
    # viewer which is the source of the drag.  The second element is list of lists, with each
    # of the element lists containing a tree item id plus the associated entity of a
    # Cougaar society to be dragged.
    # We want to store the entity in a Dictionary (the "object closet") using entity.name as
    # the key.  Then we only want to pickle the entity name, not the whole entity obj.
    sourceViewer = dataList[0]
    treeItemList = dataList[1]
    # Make a new list of just the item name strings to send to the target
    itemNameList = []
    for item in treeItemList:
      entityObj = item[1]
      itemNameList.append(entityObj.name)  # assemble list of entity names to drag
      self.frame.objCloset[entityObj.name] = item[1]  # store associated obj in the closet
    # Pickle the object first...results in a String obj
    dataString = cPickle.dumps(itemNameList)

    # Create the object that will be dragged & dropped (and which will contain the
    # Cougaar entity we want to move or copy).
    dataObj = wx.CustomDataObject(wx.CustomDataFormat("CougaarComponent"))
    dataObj.SetData(dataString)

    # Create the drop source and begin the drag and drop operation
    sourceViewer.setDropResult(0)  # reset
    dragSource = wx.DropSource(self)
    dragSource.SetData(dataObj)
    self.frame.setDragSource(sourceViewer)
    result = dragSource.DoDragDrop(wx.Drag_DefaultMove)
    altResult = sourceViewer.getDropResult()
    if altResult == wx.DragNone:
      result = altResult
    sourceViewer.isDragSource = False

    # Tell the drag source what to do with the object that was dragged
    if result == wx.DragMove:
      self.log.WriteText("DragDrop completed: %d item(s) moved\n" % len(treeItemList))  # debug
      for itemData in treeItemList:
        item = itemData[0]
        entity = itemData[1]
        if entity.has_changed_parent():
          entity.delete_from_prev_parent()  # delete object from the underlying society model
        sourceViewer.Delete(item) # delete item from the tree
      numAgents = sourceViewer.society.countAgents()
      if numAgents == 0:
        self.distroAgentsButton.Enable(False)
      if sourceViewer == self.frame.agentViewer:
        sourceViewer.parent.agentViewerTotalLabel.SetLabel('Total Agents: ' + str(numAgents))
      else:
        sourceViewer.parent.laydownViewerTotalLabel.SetLabel('Total Agents: ' + str(numAgents))

    elif result == wx.DragCopy:
      self.log.WriteText("Item copied\n")
    elif result == wx.DragError:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drag & Drop Error\n")
    elif result == wx.DragNone:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drop Rejected\n")
    elif result == wx.DragCancel:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drag Cancelled")
    else:
      self.log.WriteText("Drag & Drop totally hosed")

  #----------------------------------------------------------------------

  def checkInclNodes(self, checked=True):
    if checked:
      self.rb.SetLabel("Select method of node distribution")
      self.distroAgentsButton.SetLabel("Distribute Nodes")
      self.agentSpinner.Enable(False)
      self.rb.EnableItem(SAME_DISTRO, True)
      if self.rb.GetSelection() == DISTRO_EVENLY:
        self.nodeSpinner.Enable(False)
      if self.frame.agentSocietyOpen and self.frame.mappedSocietyOpen:
        if self.tempAgentSociety is not None and self.tempAgentSociety.countNodes() > 0:
          self.distroAgentsButton.Enable(True)
        elif self.frame.agentSociety is not None and self.frame.agentSociety.countNodes() > 0:
          self.distroAgentsButton.Enable(True)
    else:  # uncheck
      self.inclNodesCheckbox.SetValue(False)
      self.rb.SetLabel("Select method of agent distribution")
      self.distroAgentsButton.SetLabel("Distribute Agents")
      self.nodeSpinner.Enable(True)
      if self.rb.GetSelection() == SPECIFY_NUM:
        self.agentSpinner.Enable(True)
      elif self.rb.GetSelection() == SAME_DISTRO:
        self.rb.SetSelection(DISTRO_EVENLY)
      self.rb.EnableItem(SAME_DISTRO, False)
      if self.frame.agentSocietyOpen and self.frame.mappedSocietyOpen:
        if self.tempAgentSociety is not None and self.tempAgentSociety.countAgents() == 0:
          self.distroAgentsButton.Enable(False)
        elif self.frame.agentSociety is not None and self.frame.agentSociety.countAgents() == 0:
          self.distroAgentsButton.Enable(False)
    self.ignoreHostFacetsCheckbox.Enable(checked)

  #--------------------------------------------------------------------------------------

  def updateAgentCounter(self, updateBothCounters=False):
    if updateBothCounters:
      self.agentViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.agentViewer.society.countAgents()))
      self.laydownViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.laydownViewer.society.countAgents()))
    else:
      if self.currentViewer == self.frame.agentViewer:
        self.agentViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.agentViewer.society.countAgents()))
      else:
        self.laydownViewerTotalLabel.SetLabel('Total Agents: ' + str(self.frame.laydownViewer.society.countAgents()))

#*******************************************************************

class CreateHnaMapDialog:

  def __init__(self, parent, society):
    self.win = wx.Dialog(parent, -1, "Create New HNA Map", size=wx.Size(400, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
    ###---------------------------------------------------
    self.parent = parent
    self.currentSociety = society
    sizer = wx.BoxSizer(wx.VERTICAL)

    societyBox = wx.BoxSizer(wx.HORIZONTAL)
    societyNameLabel = wx.StaticText(self.win, -1, "Current HNA society name:")
    societyBox.Add(societyNameLabel, flag=wx.ALIGN_CENTER | wx.ALL, border=5)

    societyNameID = wx.NewId()
    societyName = ""
    hostPrefix = "HOST"
    hostSeq = "001"
    if self.currentSociety is not None:
      # A society is already open in the laydownViewer
      societyName = self.currentSociety.name
      self.societyNameText = wx.TextCtrl(self.win, societyNameID, societyName, size=(150,-1), style=wx.TE_READONLY)
      if self.currentSociety.countHosts() > 0:
        lastHostName = self.currentSociety.get_host(-1).name
        hostPrefix, hostSeq = self.splitName(lastHostName)
        width = len(hostSeq)
        if width > 0:  # increment it to get the next sequence number available
          hostSeq = str(int(hostSeq) + 1).zfill(width)
    else:
      self.societyNameText = wx.TextCtrl(self.win, societyNameID, societyName, size=(150,-1))
    societyBox.Add(self.societyNameText, 1, wx.ALIGN_CENTER | wx.ALL, 5)

    sizer.AddSizer(societyBox, 0, wx.ALIGN_CENTER)

    # ******************
    #      Host Creation
    # ******************
    # Add the number of hosts spinner control
    staticBoxTitle = wx.StaticBox(self.win, -1, "Host Creation")
    staticBox = wx.StaticBoxSizer(staticBoxTitle, wx.VERTICAL)
    innerBox = wx.BoxSizer(wx.VERTICAL)

    numHostsLabel = wx.StaticText(self.win, -1, "Specify number of hosts to create")
    innerBox.Add(numHostsLabel, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    numHostsSpinnerID = wx.NewId()
    self.numHostsSpinner = wx.SpinCtrl(self.win, numHostsSpinnerID, "1", size=wx.Size(50, -1), min=0, max=500)
    innerBox.Add(self.numHostsSpinner, flag=wx.ALIGN_CENTER_HORIZONTAL)

    # Add text boxes
    # Host names
    hostNameLabel = wx.StaticText(self.win, -1, "Host names:")
    innerBox.Add(hostNameLabel, 0, wx.ALIGN_CENTRE|wx.TOP, 5)

    # host name prefix
    hostNameBox = wx.BoxSizer(wx.HORIZONTAL)
    prefixLabel = wx.StaticText(self.win, -1, "Prefix:")
    hostNameBox.Add(prefixLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    hostPrefixID = wx.NewId()
    self.hostPrefix = wx.TextCtrl(self.win, hostPrefixID, hostPrefix, size=(150,-1))
    hostNameBox.Add(self.hostPrefix, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    # host name sequence number
    hostSeqLabel = wx.StaticText(self.win, -1, "Sequence begins at:")
    hostNameBox.Add(hostSeqLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    hostSeqID = wx.NewId()
    self.hostSeq = wx.TextCtrl(self.win, hostSeqID, hostSeq, size=(50,-1))
    hostNameBox.Add(self.hostSeq, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    innerBox.AddSizer(hostNameBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    staticBox.AddSizer(innerBox, 0, wx.ALIGN_CENTER)
    sizer.AddSizer(staticBox, 0, wx.ALIGN_CENTER|wx.TOP, 15)

    # Disable host creation checkbox
    addHostCheckboxID = wx.NewId()
    self.addHostCheckbox = wx.CheckBox(self.win, addHostCheckboxID, 'Do not create hosts')
    wx.EVT_CHECKBOX(self.win, addHostCheckboxID, self.OnDisableHostCreation)
    sizer.Add(self.addHostCheckbox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    # ******************
    #      Node Creation
    # ******************
    # Add the number of nodes spinner control
    staticBoxTitle = wx.StaticBox(self.win, -1, "Node Creation")
    staticBox = wx.StaticBoxSizer(staticBoxTitle, wx.VERTICAL)
    innerBox = wx.BoxSizer(wx.VERTICAL)

    numNodesLabel = wx.StaticText(self.win, -1, "Specify number of nodes to create")
    innerBox.Add(numNodesLabel, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=10)

    numNodesSpinnerID = wx.NewId()
    self.numNodesSpinner = wx.SpinCtrl(self.win, numNodesSpinnerID, "1", size=wx.Size(50, -1), min=0, max=500)
    innerBox.Add(self.numNodesSpinner, flag=wx.ALIGN_CENTER_HORIZONTAL)

    # Add text boxes
    # Node names
    nodeNameLabel = wx.StaticText(self.win, -1, "Node names:")
    innerBox.Add(nodeNameLabel, 0, wx.ALIGN_CENTRE|wx.TOP, 5)

    # node name prefix
    nodeNameBox = wx.BoxSizer(wx.HORIZONTAL)
    prefixLabel = wx.StaticText(self.win, -1, "Prefix:")
    nodeNameBox.Add(prefixLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    nodePrefixID = wx.NewId()
    self.nodePrefix = wx.TextCtrl(self.win, nodePrefixID, "NODE", size=(150,-1))
    nodeNameBox.Add(self.nodePrefix, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    # node name sequence number
    nodeSeqLabel = wx.StaticText(self.win, -1, "Sequence begins at:")
    nodeNameBox.Add(nodeSeqLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    nodeSeqID = wx.NewId()
    self.nodeSeq = wx.TextCtrl(self.win, nodeSeqID, "-A", size=(50,-1))
    nodeNameBox.Add(self.nodeSeq, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    innerBox.AddSizer(nodeNameBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    staticBox.AddSizer(innerBox, 0, wx.ALIGN_CENTER)
    sizer.AddSizer(staticBox, 0, wx.ALIGN_CENTER|wx.TOP, 30)

    # Disable node creation checkbox
    addNodeCheckboxID = wx.NewId()
    self.addNodeCheckbox = wx.CheckBox(self.win, addNodeCheckboxID, 'Do not create nodes')
    wx.EVT_CHECKBOX(self.win, addNodeCheckboxID, self.OnDisableNodeCreation)
    sizer.Add(self.addNodeCheckbox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    # Add a spacer
    spacer = wx.StaticText(self.win, -1, " ")
    sizer.Add(spacer, 0, wx.ALL, 7)

    # buttons
    box = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_HELP, "Help")
    box.Add(btn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
    wx.EVT_BUTTON(self.win, wx.ID_HELP, self.OnHelp)
    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)
    self.win.CenterOnParent()

    val = self.win.ShowModal()
    if val == wx.ID_OK:
      # If user clicks 'OK', set the following variable values in the parent window:
      self.parent.societyName = self.societyNameText.GetValue()
      self.parent.numHostsToCreate = self.numHostsSpinner.GetValue()
      self.parent.hostNamePrefix = self.hostPrefix.GetValue()
      self.parent.hostNameSeqStart = self.hostSeq.GetValue()
      self.parent.numNodesToCreate = self.numNodesSpinner.GetValue()
      self.parent.nodeNamePrefix = self.nodePrefix.GetValue()
      self.parent.nodeNameSeqStart = self.nodeSeq.GetValue()

  def splitName(self, name):
    # Separates a name that consists of a prefix and a sequence number and
    # returns each as a tuple
    for i in range(len(name)):
      if name[i:].isdigit():
        return name[:i], name[i:]

  def OnDisableHostCreation(self, event):
    if self.addHostCheckbox.IsChecked():
      self.numHostsSpinner.SetValue(0)
      self.numHostsSpinner.Enable(False)
      self.hostPrefix.Enable(False)
      self.hostSeq.Enable(False)
    else:
      self.numHostsSpinner.SetValue(1)
      self.numHostsSpinner.Enable(True)
      self.hostPrefix.Enable(True)
      self.hostSeq.Enable(True)

  def OnDisableNodeCreation(self, event):
    if self.addNodeCheckbox.IsChecked():
      self.numNodesSpinner.SetValue(0)
      self.numNodesSpinner.Enable(False)
      self.nodePrefix.Enable(False)
      self.nodeSeq.Enable(False)
    else:
      self.numNodesSpinner.SetValue(1)
      self.numNodesSpinner.Enable(True)
      self.nodePrefix.Enable(True)
      self.nodeSeq.Enable(True)

  def OnHelp(self, event):
    text = '''Create a new or edit an existing HNA society by adding hosts
and/or nodes.  To create hosts, choose the number of hosts to
create, then choose the naming scheme by selecting a prefix
and a starting sequence number to be appended to the prefix.
To create nodes, do likewise.  To create hosts only, check the
"Do not create nodes" checkbox.  Similarly, to create nodes
only, check the "Do not create hosts" checkbox.

If only nodes are created and there are no existing hosts, a
single host will be automatically created and all nodes will be
allocated to that host.'''
    helpDialog = wx.MessageDialog(self.win, text, style = wx.CAPTION | wx.OK |
         wx.THICK_FRAME | wx.ICON_INFORMATION)
    helpDialog.ShowModal()

#*******************************************************************

class FacetDisplayDialog:

  def __init__(self, parent, log, ID = -1, title = 'View/Edit Facets',
                    pos=wx.DefaultPosition, size=(300,300),
                    style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME):
    self.parent = parent
    self.log = log
    self.selectedItemList = []
    self.changesToMake = []
    self.EDIT = 0
    self.DELETE = 1
    self.ADD = 2

    self.win = wx.Dialog(self.parent, -1, title, pos, size, style)

    # Create a wx.ListCtrl
    tID= wx.NewId()
    self.list = wx.ListCtrl(self.win, tID, wx.DefaultPosition, (300,-1), wx.LC_REPORT | wx.LC_EDIT_LABELS)
    # Now add facets to the list
    entity = self.parent.entityObj
    self.list.InsertColumn(0, "Facets on " + entity.name)
    self.list.SetColumnWidth(0, 270)
    index = 0
    for facet in entity.each_facet():
      for text in facet.each_facet_pair():
        self.list.InsertStringItem(index, text)  # add text of the facet to the list
        index += 1

    charSize = self.list.GetCharHeight()
    numLines = self.list.GetItemCount()
    if numLines < 4:
      numLines = 4  # establish a minimum size of 4 lines
    desiredHeight = charSize * numLines
    self.list.SetSize((300, desiredHeight))

    sizer = wx.BoxSizer(wx.VERTICAL)  # the overall sizer for the whole panel

    btnBox = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.win, wx.ID_OK, "  OK  ")
    btn.SetDefault()
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.Add(self.list, 1, wx.EXPAND | wx.ALIGN_TOP | wx.ALIGN_CENTER) # add the wx.ListCtrl at the top
    sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)  # add buttons at the bottom

    wx.EVT_LIST_ITEM_SELECTED(self.win, tID, self.OnItemSelected)
    wx.EVT_LIST_ITEM_DESELECTED(self.win, tID, self.OnItemDeselected)
    wx.EVT_LIST_COL_RIGHT_CLICK(self.win, tID, self.OnColRightClick)
    wx.EVT_LIST_END_LABEL_EDIT(self.win, tID, self.OnEndLabelEdit)
    wx.EVT_LIST_ITEM_RIGHT_CLICK(self.win, tID, self.OnItemRightClick)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)
    self.win.CenterOnParent()

    val = self.win.ShowModal()

    if val == wx.ID_OK:
      # Make all the changes to the underlying society obj.
      # Format of 'change' list is:
      # change[0]: EDIT, DELETE, or ADD
      # change[1]: the underlying obj associated w/ the current item, or,
      #                   if ADD, the parent of the obj to be added
      # change[2]: name of the attribute involved (for EDIT), or,
      #                    for ADD, the obj to be added, or, for DELETE on a Facet,
      #                    the key for the key/value pair to be deleted (just the key or the key/value pair?)
      # change[3]: new value for the attribute (for EDIT only)
      facetType = ''
      for change in self.changesToMake:
        action = change[0]
        entity = change[1]
        if action == self.EDIT:
          oldFacetValue = change[2]
          newFacetValue = change[3]
          entity.replace_facet(oldFacetValue, newFacetValue)
        elif action == self.DELETE:
          key = change[2]
          entity.remove_facet(key)
        else:  # action == self.ADD
          facet = change[2]
          entity.add_facet(facet)
      if len(self.changesToMake) > 0:  # if there were changes to process
        #~ facetType = 'all'
        entityType = entity.getType()
        facetType = entityType + '-all'
        updateFacetCurrentlyDisplayed = True  # indicates some facets are already displayed
        self.parent.showFacet(facetType, entityType, updateFacetCurrentlyDisplayed)

    self.changesToMake = []  # empty it out
    self.win.Destroy()

  #--------------------------------------------------------------------

  def OnItemSelected(self, event):
    self.selectedItemList.append(str(event.GetLabel()))

  def OnItemDeselected(self, event):
    self.selectedItemList.remove(str(event.GetLabel()))

  def OnColRightClick(self, event):
    pt = event.GetPoint();
    self.processRightClick(pt, "add")
    event.Skip()

  def OnItemRightClick(self, event):
    pt = event.GetPoint();
    self.processRightClick(pt)
    event.Skip()

  def processRightClick(self, point, action=None):
    menu = self.SetMenu(action)
    self.list.PopupMenu(menu, point)
    menu.Destroy()

  def OnEndLabelEdit(self, event):
    listItemInfo = event.GetItem()
    oldLabel = self.list.GetItemText(listItemInfo.m_itemId)
    newLabel = str(event.GetLabel())
    if newLabel:  # if the label was actually changed:
      #~ self.log.WriteText("Old label: " + oldLabel + "  New label: " + newLabel + "\n")
      change = [self.EDIT, self.parent.entityObj, oldLabel, newLabel]
      self.changesToMake.append(change)

  def OnDeleteFacet(self, event):
    itemsToDelete = self.selectedItemList[:] # make a copy, because selectedItemList will chg
    for item in itemsToDelete:
      # First add to list of changes to make to society model
      change = [self.DELETE, self.parent.entityObj, item]
      self.changesToMake.append(change)
      # Then delete it from the list
      self.list.DeleteItem(self.list.FindItem(-1, item))

  #------------------------------------------------------------------------------------------------

  def OnAddFacet(self, event):
    self.newFacets = None
    selectedObjList = []  # AddDeleteFacetDialog constructor requires a List arg for this
    selectedObjList.append(self.parent.entityObj)
    AddDeleteFacetDialog(self, self.parent.currentViewer.society, selectedObjList)
    # Don't update the obj, just display the added facets in the facet display panel
    if self.newFacets is not None and len(self.newFacets) > 0:
      for facet in self.newFacets:
        change = [self.ADD, self.parent.entityObj, str(facet)]
        self.changesToMake.append(change)
        self.list.InsertStringItem(self.list.GetItemCount(), facet)

  #------------------------------------------------------------------------------------------------

  def OnCopyFacet(self, event):
    self.parent.facetClipboard = self.selectedItemList

  #--------------------------------------------------------------------

  def SetMenu(self, action=None):

    menu = wx.Menu()

    addFacetMenuId = wx.NewId()
    item = wx.MenuItem(menu, addFacetMenuId, "Add Facet")
    menu.AppendItem(item)
    if action != "add":
      deleteFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, deleteFacetMenuId, "Delete Facet")
      menu.AppendItem(item)
      copyFacetMenuId = wx.NewId()
      item = wx.MenuItem(menu, copyFacetMenuId, "Copy Facet")
      menu.AppendItem(item)
      wx.EVT_MENU(self.win, deleteFacetMenuId, self.OnDeleteFacet)
      wx.EVT_MENU(self.win, copyFacetMenuId, self.OnCopyFacet)
    wx.EVT_MENU(self.win, addFacetMenuId, self.OnAddFacet)
    return menu

#*******************************************************************

class AddDeleteFacetDialog:

  def __init__(self, parent, society, entityList, action='add'):
    self.parent = parent
    self.society = society
    self.entityList = entityList  # the entity object(s) to which facets are being added
    self.action = action
    self.APPLY_TO_SELECTED_ENTITY_ONLY = 0
    label = "Add Facets"
    if action == 'delete':
      label = "Delete Facets"

    daddy = None
    if isinstance(self.parent, FacetDisplayDialog):
      daddy = self.parent.win
      self.laydownPanel = self.parent.parent  # if this dialog is invoked from the FacetDisplayDialog ('add' only)
    elif isinstance(self.parent, AgentLaydownPanel):
      daddy = self.parent
      self.laydownPanel = self.parent  # if this dialog is invoked from the currentViewer right-click menu
    self.dlg = wx.Dialog(daddy, -1, label, size=wx.Size(350, 200))

    # Ensure selected entity objects are of the same type (e.g., all Hosts or all Nodes or all Agents, etc.)
    itemsAreSameType = self.laydownPanel.currentViewer.verifyMultiSelectTypes(self.entityList)
    if itemsAreSameType:
      self.entityType = self.entityList[0].getType()
      # Populate the facet type drop down box with actual facet types from
      # the society in use, augmented by a few standard types.
      stdFacetList = []
      if self.entityType == 'host' and action == 'add':
        stdFacetList = ['enclave', 'group', 'service', 'uriname']
      elif self.entityType == 'node' and action == 'add':
        stdFacetList = ['role', 'service']
      elif self.entityType == "agent" and action == 'add':
        stdFacetList = ['role']
      facetList = self.society.getAllFacetKeys(self.entityType)
      for stdFacet in stdFacetList:
        if stdFacet not in facetList:
          facetList.append(stdFacet)

      sizer = wx.BoxSizer(wx.VERTICAL)

      msg = '''Build facets for the current entity by selecting (or entering)
a facet type on the left and a facet value on the right.  Click
Add or Delete after building each facet, then OK to make
the change, or Cancel to discard.'''
      label = wx.StaticText(self.dlg, -1, msg)
      sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      typeSizer = wx.BoxSizer(wx.VERTICAL)

      typeLabel = wx.StaticText(self.dlg, -1, "Facet Type:")
      typeSizer.Add(typeLabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

      typeComboId = wx.NewId()
      defaultValue = ''
      if len(facetList) > 0:
        defaultValue = facetList[0]
      self.typeCombo = wx.ComboBox(self.dlg, typeComboId, defaultValue, wx.DefaultPosition, wx.Size(150, -1),
                        facetList, wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER)
      wx.EVT_COMBOBOX(self.dlg, typeComboId, self.OnComboBoxSelection)
      wx.EVT_TEXT_ENTER(self.dlg, typeComboId, self.OnComboBoxTextEntry)
      typeSizer.Add(self.typeCombo, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

      valueSizer = wx.BoxSizer(wx.VERTICAL)

      valueLabel = wx.StaticText(self.dlg, -1, "Facet Value:")
      valueSizer.Add(valueLabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

      valueComboId = wx.NewId()
      valueList = self.getValueList()
      defaultItem = ""
      if len(valueList) > 0:
        defaultItem = valueList[0]
      self.valueCombo = wx.ComboBox(self.dlg, valueComboId, defaultItem, wx.DefaultPosition, wx.Size(150, -1),
                        valueList, wx.CB_DROPDOWN)
      valueSizer.Add(self.valueCombo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

      comboSizer = wx.BoxSizer(wx.HORIZONTAL)
      comboSizer.Add(typeSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
      comboSizer.Add(valueSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
      sizer.Add(comboSizer, 0, wx.ALIGN_CENTER)

      rbID = wx.NewId()
      if self.entityType == 'society':
        pluralEntityType = 'societies'
      else:
        pluralEntityType = self.entityType + 's'
      actionWord = 'Add '
      preposition = 'to '
      if action == 'delete':
        actionWord = 'Delete '
        preposition = 'from '
      buttonTitles = [actionWord + 'only ' + preposition + 'the selected ' + self.entityType, \
                            actionWord + preposition + 'all ' + pluralEntityType]
      self.rb = wx.RadioBox(self.dlg, rbID, '', wx.DefaultPosition, (-1, 60), buttonTitles, 2, wx.RA_SPECIFY_ROWS)
      if isinstance(self.parent, FacetDisplayDialog) or self.entityType == "society":
        self.rb.Enable(False)
      sizer.Add(self.rb, 0, wx.ALIGN_CENTER | wx.ALL, 5)

      addBtnId = wx.NewId()
      btnLabel = 'Add'
      if action == 'delete':
        btnLabel = 'Delete'
      addButton = wx.Button(self.dlg, addBtnId, btnLabel)
      addButton.SetDefault()
      wx.EVT_BUTTON(self.dlg, addBtnId, self.OnAdd)
      sizer.Add(addButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

      facetListPaneId = wx.NewId()
      self.facetListPane = wx.TextCtrl(self.dlg, facetListPaneId, size=(250, 100), style=wx.TE_MULTILINE)
      sizer.Add(self.facetListPane, 1, wx.ALIGN_CENTER | wx.ALL, 5)

      btnBox = wx.BoxSizer(wx.HORIZONTAL)
      btn = wx.Button(self.dlg, wx.ID_OK, "  OK  ")
      btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      btn = wx.Button(self.dlg, wx.ID_CANCEL, " Cancel ")
      btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)  # add buttons at the bottom

      self.dlg.SetSizer(sizer)
      self.dlg.SetAutoLayout(True)
      sizer.Fit(self.dlg)
      self.dlg.CenterOnParent()

      val = self.dlg.ShowModal()

      if val == wx.ID_OK:
        # Get the raw facet data
        newFacetRawString = str(self.facetListPane.GetValue()).rstrip()
        checkedRadioBtn = self.rb.GetSelection()
        # convert the facet string into a List
        newFacetList = newFacetRawString.split('\n')

        # Validate input data and send error msg if invalid
        invalidFacet = self.validateFacets(newFacetList)
        if invalidFacet:
          msg = "Invalid facet: \n\n     " + invalidFacet + "\n\n" + \
                    "Facets must at least have a facet type\n" + \
                    "followed by an equals sign, and must not\n" + \
                    "be duplicates."
          errorDlg = CougaarMessageDialog(self.dlg, "error", msg)
          errorDlg.display()

        else:
          self.parent.newFacets = newFacetList  # feedback to the calling obj
          if isinstance(self.parent, AgentLaydownPanel):
            # Add the facets to the object in the society model
            if checkedRadioBtn == self.APPLY_TO_SELECTED_ENTITY_ONLY:
              for entity in self.entityList:  # apply the change to all the selected entities
                self.executeChange(entity, newFacetList)
            else:
              for entity in self.society.each_entity(self.entityType):
                self.executeChange(entity, newFacetList)
            facetType = self.entityType + '-all'
            updateDisplayedFacet = True
            self.laydownPanel.showFacet(facetType, self.entityType, updateDisplayedFacet)

      self.dlg.Destroy()

  def getValueList(self, facetType=None):
    if facetType is None:
      facetType = self.typeCombo.GetValue()

    # Read the facet values for the specified facet type directly from the current society.
    valList = self.society.getAllFacetValues(facetType, self.entityType)

    # Now combine the existing facet values with some standard values that are commonly used
    # even though they may not appear in the current society.
    stdList = []
    if self.entityType != "agent":
      if facetType == "enclave" and self.action == 'add':
        stdList = ['CONUS', 'FWD', 'REAR', 'TRANS', '1-AD-DIVSUP', '1-AD-DIV', \
                    '1-BDE-1-AD', '2-BDE-1-AD', '3-BDE-1-AD', 'AVNBDE-1-AD', \
                    'UA-NON-CA', 'UA-1-CA', 'UA-2-CA', 'UA-3-CA']
      elif facetType == "service" and self.action == 'add':
        stdList =  ['nameserver']
      elif facetType == "role" and self.action == 'add':
        stdList =   ['CertificateAuthority', 'Management', 'NameServer', 'RootCertificateAuthority']

    elif self.entityType == "agent" and self.action == 'add':
      if facetType.startswith("is") or facetType.startswith("has"):
        return ['T', 'F']
      elif facetType.endswith('org_id') or facetType.endswith('org'):
        return self.society.get_agent_list(namesOnly=True)

    # Combine the two lists into one, eliminating dupes
    for val in stdList:
      if val not in valList:
        valList.append(val)
    return valList

  def OnComboBoxSelection(self, event):
    facetType = self.typeCombo.GetStringSelection()
    self.updateValueComboBox(facetType)
    event.Skip()

  def OnComboBoxTextEntry(self, event):
    self.updateValueComboBox()
    event.Skip()

  def updateValueComboBox(self, facetType=None):
    valueList = self.getValueList(facetType)
    # Delete old list of choices
    self.valueCombo.Clear()
    # Add new list of choices
    for value in valueList:
      self.valueCombo.Append(value)  # set choices in ComboBox
    # Finally enter a default value into the ComboBox textbox
    defaultValue = ""
    if len(valueList) > 0:
      defaultValue = valueList[0]
    self.valueCombo.SetValue(defaultValue)  # set value in textbox of ComboBox

  def OnAdd(self, event):
    facetType = self.typeCombo.GetValue().strip()
    facetValue = self.valueCombo.GetValue().strip()
    if len(facetType) == 0 or len(facetValue) == 0:
      msg = "Both Facet Type and Facet Value must\ncontain valid data prior to adding or deleting."
      errorDialog = CougaarMessageDialog(self.dlg, "error", msg)
      errorDialog.display()
      return
    newFacet = facetType + "=" + facetValue + "\n"
    self.facetListPane.AppendText(newFacet)

  def executeChange(self, entity, facetList):
    if self.action == 'add':
      entity.add_facets(facetList)
    else:  # action == 'delete'
      for facetString in facetList:
        entity.remove_facet(facetString)

  def validateFacets(self, facetList):
    facetDict = {}  # use to check for dupes
    for facet in facetList:
      if facet.find('=') < 1 or facetDict.has_key(facet):
        return facet
      facetDict[facet] = 1  # registers the fact that we've seen this facet already so we can recognize dupes
    return None

#*******************************************************************

class FacetDistroDialog:

  def __init__(self, parent, fromSociety, toSociety, inclNodes=False):
    self.parent = parent
    self.fromSociety = fromSociety
    self.toSociety = toSociety
    self.inclNodes = inclNodes
    self.dlg = wx.Dialog(self.parent, -1, 'Distribute by Facet', size=wx.Size(350, 200),
                  style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

    sizer = wx.BoxSizer(wx.VERTICAL)

    self.entityType = 'agent'
    if self.inclNodes:
      self.entityType = 'node'

    # Add intro label
    msg = 'Select method for specifying ' + self.entityType + 's to be distributed:'
    label = wx.StaticText(self.dlg, -1, msg)
    sizer.Add(label, 0, wx.ALL, 5)

    # Add radio button for distro selected entities
    msg = 'Distribute selected ' + self.entityType + 's'
    distroSelectedRadioId = wx.NewId()
    self.distroSelectedRadio = None
    if wx.Platform == '__WXMSW__':
      self.distroSelectedRadio = wx.RadioButton(self.dlg, distroSelectedRadioId, msg, style = wx.RB_SINGLE)
    else:
      self.distroSelectedRadio = wx.RadioButton(self.dlg, distroSelectedRadioId, msg, style = wx.RB_GROUP)
    wx.EVT_RADIOBUTTON(self.dlg, distroSelectedRadioId, self.OnDistroCriteriaRadioSelect)
    sizer.Add(self.distroSelectedRadio, 0, wx.ALL, 5)

    # Add radio button for distro by facet
    msg = 'Distribute ' + self.entityType + 's with the following facets:'
    distroByFacetRadioId = wx.NewId()
    self.distroByFacetRadio = None
    if wx.Platform == '__WXMSW__':
      self.distroByFacetRadio = wx.RadioButton(self.dlg, distroByFacetRadioId, msg, style = wx.RB_SINGLE)
    else:
      self.distroByFacetRadio = wx.RadioButton(self.dlg, distroByFacetRadioId, msg)
    self.distroByFacetRadio.SetValue(True)  # selected by default
    self.distroByFacet = True  # default
    wx.EVT_RADIOBUTTON(self.dlg, distroByFacetRadioId, self.OnDistroCriteriaRadioSelect)
    sizer.Add(self.distroByFacetRadio, 0, wx.ALL, 5)

    # Add the "distro from" facet selection panel
    self.facetPanel = FacetSelectionPanel(self.dlg, self.fromSociety, self.entityType)
    sizer.Add(self.facetPanel, 1, wx.GROW)

    # Add the "Distro to" section
    distroToLabel = wx.StaticText(self.dlg, -1, "\nTo the following entity:")
    sizer.Add(distroToLabel, 0, wx.ALL, 5)

    # Add the Distro To radio buttons
    # First row
    radio1Box = wx.BoxSizer(wx.HORIZONTAL)
    hostNameRadioId = wx.NewId()
    self.hostNameRadio = None
    if wx.Platform == '__WXMSW__':
      self.hostNameRadio = wx.RadioButton(self.dlg, hostNameRadioId, "Host name:  ", style = wx.RB_SINGLE)
    else:
      self.hostNameRadio = wx.RadioButton(self.dlg, hostNameRadioId, "Host name:  ", style = wx.RB_GROUP)
    self.hostNameRadio.SetValue(True)  # selected by default
    hostNameComboId = wx.NewId()
    defaultValue = ''
    hostList = []
    for host in self.toSociety.each_host():
      hostList.append(host.name)
    if len(hostList) > 0:
      defaultValue = hostList[0]
    self.hostNameCombo = wx.ComboBox(self.dlg, hostNameComboId, defaultValue, wx.DefaultPosition,
                      wx.Size(150, -1), hostList, wx.CB_DROPDOWN)
    self.hostNameCombo.SetInsertionPoint(0)
    radio1Box.Add(self.hostNameRadio, 0, wx.ALIGN_CENTER)
    radio1Box.Add(self.hostNameCombo, 0, wx.ALIGN_CENTER)
    wx.EVT_RADIOBUTTON(self.dlg, hostNameRadioId, self.OnDistroRadioSelect)

    # Second row
    radio2Box = wx.BoxSizer(wx.HORIZONTAL)
    nodeNameRadioId = wx.NewId()
    self.nodeNameRadio = None
    if wx.Platform == '__WXMSW__':
      self.nodeNameRadio = wx.RadioButton(self.dlg, nodeNameRadioId, "Node name: ", style = wx.RB_SINGLE)
    else:
      self.nodeNameRadio = wx.RadioButton(self.dlg, nodeNameRadioId, "Node name: ")
    if self.inclNodes:
      self.nodeNameRadio.Enable(False)
    nodeNameComboId = wx.NewId()
    defaultValue = ''
    nodeList = []
    for node in self.toSociety.each_node():
      nodeList.append(node.name)
    if len(nodeList) > 0:
      defaultValue = nodeList[0]
    self.nodeNameCombo = wx.ComboBox(self.dlg, nodeNameComboId, defaultValue, wx.DefaultPosition,
                      wx.Size(150, -1), nodeList, wx.CB_DROPDOWN)
    self.nodeNameCombo.SetInsertionPoint(0)
    self.nodeNameCombo.Enable(False)
    radio2Box.Add(self.nodeNameRadio, 0, wx.ALIGN_CENTER)
    radio2Box.Add(self.nodeNameCombo, 0, wx.ALIGN_CENTER)
    wx.EVT_RADIOBUTTON(self.dlg, nodeNameRadioId, self.OnDistroRadioSelect)

    # Third row
    hostFacetRadioId = wx.NewId()
    self.hostFacetRadio = None
    if wx.Platform == '__WXMSW__':
      self.hostFacetRadio = wx.RadioButton(self.dlg, hostFacetRadioId, "Host with facets shown below", style = wx.RB_SINGLE)
    else:
      self.hostFacetRadio = wx.RadioButton(self.dlg, hostFacetRadioId, "Host with facets shown below")
    wx.EVT_RADIOBUTTON(self.dlg, hostFacetRadioId, self.OnDistroRadioSelect)

    # Fourth row
    nodeFacetRadioId = wx.NewId()
    self.nodeFacetRadio = None
    if wx.Platform == '__WXMSW__':
      self.nodeFacetRadio = wx.RadioButton(self.dlg, nodeFacetRadioId, "Node with facets shown below", style = wx.RB_SINGLE)
    else:
      self.nodeFacetRadio = wx.RadioButton(self.dlg, nodeFacetRadioId, "Node with facets shown below")
    wx.EVT_RADIOBUTTON(self.dlg, nodeFacetRadioId, self.OnDistroRadioSelect)
    if self.inclNodes:
      self.nodeFacetRadio.Enable(False)

    # Put all the radio buttons in a List to streamline later processing
    self.radioList = []
    self.radioList.append(self.hostNameRadio)
    self.radioList.append(self.nodeNameRadio)
    self.radioList.append(self.hostFacetRadio)
    self.radioList.append(self.nodeFacetRadio)

    distroRadioSizer = wx.BoxSizer(wx.VERTICAL)
    distroRadioSizer.Add(radio1Box, 0, wx.ALL, 5)
    distroRadioSizer.Add(radio2Box, 0, wx.ALL, 5)
    distroRadioSizer.Add(self.hostFacetRadio, 0, wx.ALL, 5)
    distroRadioSizer.Add(self.nodeFacetRadio, 0, wx.ALL, 5)
    sizer.Add(distroRadioSizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

    # Add the "distro to" facet selection panel
    self.facetPanel2 = FacetSelectionPanel(self.dlg, self.toSociety, 'host', False)
    sizer.Add(self.facetPanel2, 1, wx.GROW)

    # Add OK and CANCEL buttons
    btnBox = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.dlg, wx.ID_OK, "  OK  ")
    btn.SetDefault()
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.dlg, wx.ID_CANCEL, " Cancel ")
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)  # add buttons at the bottom

    self.dlg.SetSizer(sizer)
    self.dlg.SetAutoLayout(True)
    sizer.Fit(self.dlg)
    self.dlg.CenterOnParent()

    val = self.dlg.ShowModal()

    if val == wx.ID_OK:
      entityType = 'agent'  # the type of entity to move (either 'agent' or 'node')
      if self.inclNodes:
        entityType = 'node'

      entitiesToMove = []  # list of agent or node objects to be distributed

      if self.distroByFacet:
        # Get list of facets to match against
        self.facetList = str(self.facetPanel.facetListPane.GetValue()).strip().split('\n')

        # Check for presence of facets to search for; display error msg if none
        if len(self.facetList) == 0 or (len(self.facetList) == 1 and len(self.facetList[0]) == 0):
          msg = 'Please add at least one facet for determining which entities should move.'
          CougaarMessageDialog(self.dlg, "error", msg).display()
          return

        # AND or OR multiple facets for determining entities to move?
        self.booleanOperation = str(self.facetPanel.rb.GetStringSelection()).strip()

        # Search agent/node to move for matching facets
        for entity in self.fromSociety.each_entity(entityType):
          if self.hasFacetMatch(entity):
            entitiesToMove.append(entity)
            #~ print entity.name + ' is a match'  #  debug

      else:  # distro selected entities
        selectedItems = self.parent.frame.agentViewer.GetSelections()
        for item in selectedItems:
          entityObj = self.parent.frame.agentViewer.GetPyData(item)
          # Note that we only use this ref to the entity obj for determining the entity type.
          # You can't use this ref to the entity obj for distribution, because
          # it's from the agentSociety, not the tempAgentSociety.  Any ref to the entity
          # being moved must come from self.fromSociety.

          if not isinstance(entityObj, Node) and not isinstance(entityObj, Agent):
            msg = '''
Only Nodes and Agents can be distributed via this method.
Please select a Node or Agent, or distribute by facet.'''
            CougaarMessageDialog(self.dlg, "error", msg).display()
            return

          itemName = self.parent.frame.agentViewer.GetItemText(item).getItemName()
          if entityType == 'node':
            entitiesToMove.append(self.fromSociety.get_node(itemName))
          else:  # entityType == 'agent'
            entitiesToMove.append(self.fromSociety.get_agent(itemName))

        itemsAreSameType = self.parent.frame.agentViewer.verifyMultiSelectTypes(entitiesToMove)
        if not itemsAreSameType:
          return

      # Determine which radio button (of the lower group) is selected
      selectedRadio = None
      for radio in self.radioList:
        if radio.GetValue():
          selectedRadio = radio

      # Now determine which entity to distro the selected entities to (if user selected that option from the radio buttons)
      if selectedRadio is self.hostFacetRadio or selectedRadio is self.nodeFacetRadio:
        # Get list of facets to match against for determining destination entity
        self.destFacetList = str(self.facetPanel2.facetListPane.GetValue()).strip().split('\n')
        # Check for presence of facets to search for; display error msg if none
        if len(self.destFacetList) == 0 or (len(self.destFacetList) == 1 and len(self.destFacetList[0]) == 0):
          msg = 'Please add at least one facet for determining a destination.'
          CougaarMessageDialog(self.dlg, "error", msg).display()
          return

      # AND or OR multiple facets for determining dest entities?
      self.destBooleanOperation = str(self.facetPanel2.rb.GetStringSelection()).strip()

      # Get destination hosts/nodes for nodes/agents being distributed
      if len(entitiesToMove) > 0:  # if there were any matches (i.e., anything to move)
        destEntityList = []
        if selectedRadio is self.hostNameRadio:
          hostname = str(self.hostNameCombo.GetValue())
          destEntityList.append(self.toSociety.get_host_by_name(hostname))
        elif selectedRadio is self.nodeNameRadio:
          nodename = str(self.nodeNameCombo.GetValue())
          destEntityList.append(self.toSociety.get_node(nodename))
        else:
          destEntityType = 'host'
          if selectedRadio is self.nodeFacetRadio:
            destEntityType = 'node'
          for destEntity in self.toSociety.each_entity(destEntityType):
            if self.hasFacetMatch(destEntity, True):
              destEntityList.append(destEntity)

        if len(destEntityList) == 1:  # if there's only one dest entity, it's pretty straightforward
          for entity in entitiesToMove:
            self.allocateEntity(entity, destEntityList[0])
        elif len(destEntityList) > 1:
          # Figure how many entities go to each dest
          entitiesPerDest, entitiesLeftOver = divmod(len(entitiesToMove), len(destEntityList))
          index = 0  # for stepping through the entitiesToMove list
          destIndex = 0  # for stepping through the destEntitiesList
          moreEntitiesToMove = len(entitiesToMove)
          while moreEntitiesToMove:
            while entitiesLeftOver:
              for i in range(entitiesPerDest + 1):
                self.allocateEntity(entitiesToMove[index], destEntityList[destIndex])
                index += 1
                moreEntitiesToMove -= 1
              entitiesLeftOver -= 1
              destIndex += 1
            for i in range (entitiesPerDest):
              self.allocateEntity(entitiesToMove[index], destEntityList[destIndex])
              index += 1
              moreEntitiesToMove -= 1
            destIndex += 1
        else:  # len(destEntityList) == 0
          msg = 'No destination entities matched your facet criteria.'
          CougaarMessageDialog(self.dlg, 'info', msg).display()
          return

      else:
        msg = 'No ' + entityType + 's matched your facet criteria.'
        CougaarMessageDialog(self.dlg, "info", msg).display()
        return

    self.dlg.Destroy()

  # --------------------------------------------------------------------

  def OnDistroCriteriaRadioSelect(self, event):
    selectedRadio = event.GetEventObject()
    if selectedRadio is self.distroSelectedRadio:
      self.distroByFacetRadio.SetValue(False)
      self.facetPanel.Disable()
      self.distroByFacet = False
    if selectedRadio is self.distroByFacetRadio:
      self.distroSelectedRadio.SetValue(False)
      self.facetPanel.Enable(True)
      self.facetPanel.rb.Disable()
      self.distroByFacet = True

  # --------------------------------------------------------------------

  def OnDistroRadioSelect(self, event):
    selectedRadio = event.GetEventObject()
    for radio in self.radioList:
      if radio is not selectedRadio:
        radio.SetValue(False)
    if selectedRadio is self.hostNameRadio:
      self.hostNameCombo.Enable(True)
      self.nodeNameCombo.Enable(False)
      self.facetPanel2.Disable()
    elif selectedRadio is self.nodeNameRadio:
      self.hostNameCombo.Enable(False)
      self.nodeNameCombo.Enable(True)
      self.facetPanel2.Disable()
    else:
      self.hostNameCombo.Enable(False)
      self.nodeNameCombo.Enable(False)
      self.facetPanel2.Enable(True)
      self.facetPanel2.rb.Disable()
      # Distribute to either hosts or nodes (default is host)
      destEntityType = 'host'
      self.facetPanel2.entityType = 'host'
      if selectedRadio is self.nodeFacetRadio:
        destEntityType = 'node'
        self.facetPanel2.entityType = 'node'
      # Populate the 'distro to' facet type and value combo boxes
      # Do the facet type combo box first
      defaultValue = ''
      facetTypeList = self.toSociety.getAllFacetKeys(destEntityType)
      if len(facetTypeList) > 0:
        defaultValue = facetTypeList[0]
      self.facetPanel2.typeCombo.Clear()
      for facetType in facetTypeList:
        self.facetPanel2.typeCombo.Append(facetType)
      self.facetPanel2.typeCombo.SetValue(defaultValue)
      # Now do the facet value combo box
      self.facetPanel2.updateValueComboBox(self.toSociety, defaultValue)

  # --------------------------------------------------------------------

  def hasFacetMatch(self, entity, useDestFacetList=False):
    # Search agent for matching facets
    hasFacetMatch = False
    listOFacets = []
    booleanOp = None
    if useDestFacetList:
      listOFacets = self.destFacetList
      booleanOp = self.destBooleanOperation
    else:
      listOFacets = self.facetList
      booleanOp = self.booleanOperation
    for facet in listOFacets:
      if entity.has_facet(facet):
        hasFacetMatch = True
        if booleanOp == "OR":
          return True
      elif booleanOp == "AND":
        return False
    if hasFacetMatch:
      return True
    return False

  # --------------------------------------------------------------------

  # Move entities to their new parent.  Entities may be nodes or agents.
  #
  def allocateEntity(self, entity, destEntity):
    if isinstance(destEntity, Host) and isinstance(entity, Agent):
      # if we're trying to put an agent onto a host:
      node = destEntity.get_node(0)  # add agent to the first node
      if not node:  # if no node was found, create one and add it to the society model
        node = destEntity.add_node(destEntity.name + "_NODE_0")
      node.add_entity(entity)  # add agent to the society model
    else:
      # if we're trying to put an agent onto a node or a node onto a host:
      destEntity.add_entity(entity)  # add it to society model

    # Finally, delete moved entity from its previous parent...
    if entity.has_changed_parent():   # should always be True here
      entity.delete_from_prev_parent()  # delete object from the underlying society model


#*******************************************************************

class ShowFacetSelectionDialog:

  def __init__(self, parent, society, entityType):
    self.parent = parent
    self.society = society
    self.entityType = entityType
    self.facetList = None
    self.dlg = wx.Dialog(self.parent, -1, 'Select Facets to Show', size=wx.Size(350, 200),
                  style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

    sizer = wx.BoxSizer(wx.VERTICAL)

    # Add intro label
    msg = 'Select ' + self.entityType + ' facets to show:'
    label = wx.StaticText(self.dlg, -1, msg)
    sizer.Add(label, 0, wx.ALL, 5)

    # Add the "distro from" facet selection panel
    self.facetPanel = FacetSelectionPanel(self.dlg, self.society, self.entityType, addWildcard=True)
    sizer.Add(self.facetPanel, 1, wx.GROW)

    # Add OK and CANCEL buttons
    btnBox = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.dlg, wx.ID_OK, "  OK  ")
    btn.SetDefault()
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.dlg, wx.ID_CANCEL, " Cancel ")
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)  # add buttons at the bottom

    self.dlg.SetSizer(sizer)
    self.dlg.SetAutoLayout(True)
    sizer.Fit(self.dlg)
    self.dlg.CenterOnParent()

    val = self.dlg.ShowModal()

    if val == wx.ID_OK:
      self.facetList = str(self.facetPanel.facetListPane.GetValue()).strip().split('\n')

      # Check for presence of facets to search for; display error msg if none
      if len(self.facetList) == 0 or (len(self.facetList) == 1 and len(self.facetList[0]) == 0):
        msg = 'Please add at least one facet for determining which entities should move.'
        CougaarMessageDialog(self.dlg, "error", msg).display()
        return

      # Doesn't make sense to specify 'AnyValue' as a value for a facet type and to also specify that facet
      # type with a specific value, so we'll check for that and filter out the more specific specification.
      # Also, filter out dupes.
      errorCheckDict = {}
      facetsToRemove = []
      facetTypesToRemove = []
      numFacets = len(self.facetList)
      for facet in self.facetList:
        facetElements = facet.split('=')
        facetType = facetElements[0]
        facetValue = facetElements[1]
        if errorCheckDict.has_key(facetType):   # already saw this facetType before
          if errorCheckDict[facetType] == facetValue or errorCheckDict[facetType] == 'AnyValue':
            # Found facet that's a dupe or too specific (has a previous spec of 'AnyValue')
            facetsToRemove.append(facet)
          elif facetValue == 'AnyValue':
            errorCheckDict[facetType] = 'AnyValue'
            # Found facetType that's too specific (just got same facetType w/ value of 'AnyValue')
            facetTypesToRemove.append(facetType)  # mark the prev value for removal
        else:
          # key's not present, so add it
          errorCheckDict[facetType] = facetValue

      # Trash facetTypes that were dupes or were specific values when a prev 'AnyValue' was specified
      for facet in facetsToRemove:
        self.facetList.remove(facet)

      # Now remove the facetTypes that have both a specific value and an 'AnyValue'
      facetsToRemove = []  # clear it out for reuse
      for facet in self.facetList:
        for facetType in facetTypesToRemove:
          if facet.startswith(facetType) and not facet.endswith('AnyValue'):
            facetsToRemove.append(facet)  # keep the 'AnyValue' version and trash the others

      # Now do the final flush of items that are too specific
      for facet in facetsToRemove:
        self.facetList.remove(facet)

      # AND or OR multiple facets for determining entities to move?
      self.booleanOperation = str(self.facetPanel.rb.GetStringSelection()).strip()

    else:
      self.facetList = None

    self.dlg.Destroy()


#*******************************************************************

class FacetSelectionPanel(wx.Panel):

  def __init__(self, parent, society, entityType, enableControls=True, addWildcard=False):
    #~ wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
    wx.Panel.__init__(self, parent, -1)
    self.society = society
    self.entityType = entityType
    self.addWildcard = addWildcard

    sizer = wx.BoxSizer(wx.VERTICAL)

    # Add facet type combo box
    typeSizer = wx.BoxSizer(wx.VERTICAL)

    typeLabel = wx.StaticText(self, -1, "Facet Type:")
    typeSizer.Add(typeLabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    typeComboId = wx.NewId()
    defaultValue = ''
    facetList = self.society.getAllFacetKeys(self.entityType)
    if len(facetList) > 0:
      defaultValue = facetList[0]
    self.typeCombo = wx.ComboBox(self, typeComboId, defaultValue, wx.DefaultPosition, wx.Size(150, -1),
                      facetList, wx.CB_DROPDOWN)
    self.typeCombo.SetInsertionPoint(0)
    wx.EVT_COMBOBOX(self, typeComboId, self.OnComboBoxSelection)
    wx.EVT_TEXT_ENTER(self, typeComboId, self.OnComboBoxTextEntry)
    typeSizer.Add(self.typeCombo, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

    # Add facet value combo box
    valueSizer = wx.BoxSizer(wx.VERTICAL)

    valueLabel = wx.StaticText(self, -1, "Facet Value:")
    valueSizer.Add(valueLabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    valueComboId = wx.NewId()
    valueList = self.getValueList(self.society, self.typeCombo.GetValue())
    defaultItem = ""
    if len(valueList) > 0:
      defaultItem = valueList[0]
    self.valueCombo = wx.ComboBox(self, valueComboId, defaultItem, wx.DefaultPosition, wx.Size(150, -1),
                      valueList, wx.CB_DROPDOWN)
    self.valueCombo.SetInsertionPoint(0)
    valueSizer.Add(self.valueCombo, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    comboSizer = wx.BoxSizer(wx.HORIZONTAL)
    comboSizer.Add(typeSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
    comboSizer.Add(valueSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
    sizer.Add(comboSizer, 0, wx.ALIGN_CENTER)

    addSizer = wx.BoxSizer(wx.HORIZONTAL)

    # Add 'AND/OR' radio box
    rbID = wx.NewId()
    rbLabel = "Combine multiple facets using:"
    buttonTitles = ["AND                           ", "OR"]
    self.rb = wx.RadioBox(self, rbID, rbLabel, wx.DefaultPosition, (-1, -1), buttonTitles, len(buttonTitles), wx.RA_SPECIFY_ROWS)
    self.rb.Enable(False)
    addSizer.Add(self.rb, 0, wx.ALL, 5)

    # Add 'ADD' button
    addBtnId = wx.NewId()
    self.addButton = wx.Button(self, addBtnId, 'Add')
    wx.EVT_BUTTON(self, addBtnId, self.OnAdd)
    addSizer.Add(self.addButton, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    sizer.Add(addSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    # Add text area for holding selected facets
    facetListPaneId = wx.NewId()
    self.facetListPane = wx.TextCtrl(self, facetListPaneId, size=(250, 50), style=wx.TE_MULTILINE)
    sizer.Add(self.facetListPane, 1, wx.ALIGN_CENTER | wx.ALL, 5)
    wx.EVT_TEXT(self, facetListPaneId, self.OnTextChange)

    if not enableControls:
      self.Disable()

    self.SetSizer(sizer)
    self.SetAutoLayout(True)
    sizer.Fit(self)

  # --------------------------------------------------------------------

  def updateValueComboBox(self, society, facetType=None):
    valueList = self.getValueList(society, facetType)
    # Delete old list of choices
    self.valueCombo.Clear()
    # Add new list of choices
    for value in valueList:
      self.valueCombo.Append(value)  # set choices in ComboBox
    # Finally enter a default value into the ComboBox textbox
    defaultValue = ""
    if len(valueList) > 0:
      defaultValue = valueList[0]
    self.valueCombo.SetValue(defaultValue)  # set value in textbox of ComboBox

  # --------------------------------------------------------------------

  def getValueList(self, society, facetType):
    if facetType is None:
      facetType = self.typeCombo.GetValue()
    # Read the facet values for the specified facet type directly from the current society.
    valueList = society.getAllFacetValues(facetType, self.entityType)
    if self.addWildcard and len(valueList) > 0:
      valueList.insert(0, 'AnyValue')
    return valueList

  # --------------------------------------------------------------------

  def OnComboBoxSelection(self, event):
    facetType = self.typeCombo.GetStringSelection()
    self.updateValueComboBox(self.society, facetType)
    event.Skip()

  # --------------------------------------------------------------------

  def OnComboBoxTextEntry(self, event):
    self.updateValueComboBox(self.society)
    event.Skip()

  # --------------------------------------------------------------------

  def OnAdd(self, event):
    facetType = self.typeCombo.GetValue()
    facetValue = self.valueCombo.GetValue()
    if len(facetType) == 0 or len(facetValue) == 0:
      msg = "Both Facet Type and Facet Value must\ncontain valid data prior to adding."
      errorDialog = CougaarMessageDialog(self, "error", msg)
      errorDialog.display()
      return
    newFacet = facetType + "=" + facetValue + "\n"
    self.facetListPane.AppendText(newFacet)
    if self.facetListPane.GetNumberOfLines() > 2:
      self.rb.Enable(True)

  # --------------------------------------------------------------------

  def OnTextChange(self, event):
    # We only want the AND/OR radio box enabled if there are two or more
    # facets in the facetListPane.
    if self.hasMultipleLinesOfText():
      self.rb.Enable(True)
    else:
      self.rb.Disable()

  # --------------------------------------------------------------------

  def hasMultipleLinesOfText(self):
    # This kabuki dance is req'd because a newline char (and, hence, a line) exists
    # even in an empty multi-line wx.TextControl.  Also, if you delete a line of text
    # using the Delete or Backspace key but don't specifically delete the newline
    # char, it remains, adding a line with no text.  This method counts the number
    # of lines that contain useful text (defined as at least 3 chars, including an
    # equals sign).  Three chars is the min length because a facet is at least 'a=b'.
    numLines = self.facetListPane.GetNumberOfLines()
    if numLines < 2:
      return False
    else:
      for lineNo in range(numLines):
        # Don't count any line that's 'empty' or that doesn't contain an equals sign ('=')
        if self.facetListPane.GetLineLength(lineNo) < 3 or str(self.facetListPane.GetLineText(lineNo)).find('=') == -1:
          numLines -= 1
      if numLines < 2:  # test for 2 lines again
        return False
      return True

#*******************************************************************

class SummaryDialog:

  def __init__(self, parent, society):
    self.dlg = wx.Dialog(parent, -1, 'Society Summary',
                  style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

    sizer = wx.BoxSizer(wx.VERTICAL)

    label = wx.StaticText(self.dlg, -1, 'Society name: %s' % society.name)
    sizer.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    counterSizer = wx.BoxSizer(wx.VERTICAL)

    msg = 'Hosts:   %d\nNodes:  %d\nAgents: %d' % (society.countHosts(), society.countNodes(), society.countAgents())
    label = wx.StaticText(self.dlg, -1, msg)
    counterSizer.Add(label, 0, wx.ALL, 5)
    sizer.Add(counterSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    hostNodeSizer = wx.BoxSizer(wx.VERTICAL)

    nameLen = society.get_longest_hostname()
    spacer = ' ' * (nameLen)
    msg = 'Hosts:' + spacer + 'Number of Nodes:'
    label = wx.StaticText(self.dlg, -1, msg)
    hostNodeSizer.Add(label, 1, wx.ALL, 5)

    msg = ''
    for host in society.each_host():
      # Adjust spacing to account for hostnames of different lengths while
      # keeping node numbers aligned.  Works a little, but not real well.
      spacer = (nameLen + 16 - len(host.name)) * ' '
      msg = msg + host.name + spacer + str(len(host.nodelist)) + '\n'
    label = wx.StaticText(self.dlg, -1, msg)
    hostNodeSizer.Add(label, 0, wx.ALL, 5)

    sizer.Add(hostNodeSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

    # Add CLOSE button
    btn = wx.Button(self.dlg, wx.ID_OK, "Close")
    btn.SetDefault()

    sizer.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 5)  # add buttons at the bottom

    self.dlg.SetSizer(sizer)
    self.dlg.SetAutoLayout(True)
    sizer.Fit(self.dlg)
    self.dlg.CenterOnParent()

    self.dlg.ShowModal()
    self.dlg.Destroy()

#*******************************************************************

def runApp( frame, nb, log ):
    win = AgentLaydownPanel( frame, nb, log )
    return win
def runTest(frame, nb, log):
    win = runApp( frame, nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
<H2>The CSMARTer Agent Laydown Editor ...</H2>
<P>
Enter some useful text is here.
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])
