#!/bin/env python
#----------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: societyEditor.py,v 1.1 2004-08-25 21:14:18 damoore Exp $
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
#

from wxPython.wx import *
from wxPython.lib.rcsizer import RowColSizer
from wxPython import  events
import images
from gizmo import Gizmo
import gizmoImages

#import threading
import thread
#import Queue
import os

from ACMEPy.society import Society
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from ACMEPy.component import Component
from ACMEPy.argument import Argument
from ACMEPy.parameter import *

from insertion_dialog import *
from csmarter_events import *
from societyViewer import SocietyViewer
from societyFactoryServer import SocietyFactoryServer
from cougaar_DragAndDrop import *

#----------------------------------------------------------------------

class SocietyEditorPanel(wxPanel):
  def __init__( self, parent, frame, log ):
    wxPanel.__init__( self, parent, -1 )
    self.log = log
    sizer = RowColSizer()
    self.frame = frame # top-level frame that contains this wxPanel
    self.frame.societyOpen = 0
    self.infoFrameOpen = 0
    self.societyFile = None
    self.frame.societyFile = None
    self.itemGrabbed = False

### static controls:

    btnBox = wxBoxSizer(wxHORIZONTAL)

    self.openSocietyButton = wxButton(self, 10, "Open Society")
    EVT_BUTTON(self, 10, self.OnOpenSociety)
    self.openSocietyButton.SetBackgroundColour(wxBLUE)
    self.openSocietyButton.SetForegroundColour(wxWHITE)
    self.openSocietyButton.SetDefault()
    btnBox.Add(self.openSocietyButton, flag=wxALIGN_CENTER_VERTICAL | wxBOTTOM, border=20)

    self.saveSocietyButton = wxButton(self, 20, "Save Society")
    EVT_BUTTON(self, 20, self.OnSaveSociety)
    self.saveSocietyButton.Enable(False)
    btnBox.Add(self.saveSocietyButton, flag=wxALIGN_CENTER_VERTICAL | wxLEFT | wxBOTTOM, border=20)

    self.closeSocietyButton = wxButton(self, 15, "Close Society")
    EVT_BUTTON(self, 15, self.OnCloseSociety)
    self.closeSocietyButton.Enable(False)
    btnBox.Add(self.closeSocietyButton, flag=wxALIGN_CENTER_VERTICAL | wxLEFT | wxBOTTOM, border=20)

    nextHighlightBtnId = wxNewId()
    self.nextHighlightButton = wxButton(self, nextHighlightBtnId, "Next Highlight")
    EVT_BUTTON(self, nextHighlightBtnId, self.OnShowNextHighlight)
    self.nextHighlightButton.Enable(False)
    btnBox.Add(self.nextHighlightButton, flag=wxALIGN_CENTER_VERTICAL | wxLEFT | wxBOTTOM, border=20)

    self.getHnaMapButton = wxButton(self, 25, "Get HNA Map")
    EVT_BUTTON(self, 25, self.OnGetHnaMap)
    self.getHnaMapButton.Enable(False)
    btnBox.Add(self.getHnaMapButton, flag=wxALIGN_CENTER_VERTICAL | wxLEFT | wxBOTTOM, border=20)

    sizer.Add(btnBox, pos=(1,1),  flag=wxALIGN_LEFT|wxALIGN_CENTER_VERTICAL)

    lesImages = [gizmoImages.catalog[i].getBitmap() for i in gizmoImages.index]
    self.gizmo = Gizmo(self, -1, lesImages, size=(36, 36), frameDelay = 0.1)
    EVT_UPDATE_SOCIETY(self, self.OnUpdate)
    sizer.Add(self.gizmo, pos=(1,2), flag=wxBOTTOM | wxALIGN_RIGHT, border=20)

    self.il = wxImageList(16,16)
    self.societyImage   = self.il.Add(images.getSocietyBitmap())
    self.hostImage      = self.il.Add(images.getHostBitmap())
    self.nodeImage      = self.il.Add(images.getNodeBitmap())
    self.agentImage     = self.il.Add(images.getAgentBitmap())
    self.componentImage = self.il.Add(images.getComponentBitmap())
    self.argumentImage  = self.il.Add(images.getArgumentBitmap())
    self.questionImage  = self.il.Add(images.getQuestionBitmap())

    tID = wxNewId()
    self.frame.societyViewer = SocietyViewer(self, tID, 'societyViewer', size=(240, 100),
                               style=wxTR_HAS_BUTTONS | wxTR_EDIT_LABELS | wxTR_MULTIPLE,
                               log=self.log)
    sizer.Add(self.frame.societyViewer, flag=wxEXPAND, pos=(2,1), colspan=2)
    dropTarget = CougaarDropTarget(self.frame.societyViewer, self.log, self.frame, true)
    self.frame.societyViewer.SetDropTarget(dropTarget)

### Event handlers for various
    EVT_TREE_END_LABEL_EDIT(self, tID, self.OnEndLabelEdit) #fired by call to wxTreeCtrl.EditLabel()
    EVT_TREE_SEL_CHANGED    (self, tID, self.OnSelChanged)
    EVT_TREE_SEL_CHANGING(self, tID, self.OnSelChanging)
    EVT_RIGHT_DOWN(self.frame.societyViewer, self.OnRightClick)  # emits a wxMouseEvent
    EVT_RIGHT_UP(self.frame.societyViewer, self.OnRightUp)  # emits a wxMouseEvent
    EVT_LEFT_DOWN(self.frame.societyViewer, self.OnLeftDown)  # emits a wxMouseEvent
    EVT_LEFT_UP(self.frame.societyViewer, self.OnLeftUp)  # emits a wxMouseEvent
    EVT_MOTION(self.frame.societyViewer, self.OnMotion)  # emits a wxMouseEvent

###

    self.bg_bmp = images.getGridBGBitmap()
    EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

    sizer.AddSpacer(10,10, pos=(1,3)) # adds a constant size space along the right edge
    sizer.AddSpacer(10,10, pos=(3,1)) # adds a constant size space along the bottom
    sizer.AddGrowableCol(1) # makes rule styled text box and Society Viewer expand to the right on window resize
    sizer.AddGrowableRow(2) # makes Society Viewer expand downward on window resize

    self.SetSizer(sizer)
    self.SetAutoLayout(true)

  #*****************************************************************
  ###
  ### event callbacks
  ###

  def OnOpenSociety(self, evt):
    self.frame.openSocietyFile(self, "society")

  def StartAnimation(self):
    self.gizmo.Start()

  def StopAnimation(self):
    self.gizmo.Rest()

  #----------------------------------------------------------------------

  def OnSaveSociety(self, event):
    if not self.frame.societyOpen:
        dlg = wxMessageDialog(self, 'No society is open. You must open a society before you can save it.',
                'No Society Open', wxOK | wxICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    else:
      self.frame.saveSociety("society")

  #----------------------------------------------------------------------

  def OnCloseSociety(self, evt):
    self.frame.closeSociety("society")
    self.frame.ruleEditor.tempSociety = None
    self.frame.ruleEditor.undoTransformButton.Disable()

  #----------------------------------------------------------------------

  # If this method is called, it is guaranteed that there is a next highlighted
  # item to show.
  #
  def OnShowNextHighlight(self, event):
    viewer = self.frame.societyViewer
    item = viewer.colourisedItemsList[viewer.colourisedItemIndex]
    viewer.EnsureVisible(item)

    # Prepare to show the next highlighted item; if none, disable the button.
    self.checkForNextHighlight()

  #----------------------------------------------------------------------

  # Determines if there's another highlighted item; if not, disables the
  # button.  If so,  determines if it's already visible.  If not, exits.
  # If so, increments the colourisedItemIndex to the next non-visible
  # highlighted item.  If none, disable the button.
  #
  def checkForNextHighlight(self):
    viewer = self.frame.societyViewer
    viewer.colourisedItemIndex += 1
    if viewer.colourisedItemIndex >= len(viewer.colourisedItemsList):
      self.nextHighlightButton.Disable()
    else:
      item = viewer.colourisedItemsList[viewer.colourisedItemIndex]
      if viewer.IsVisible(item):
        self.checkForNextHighlight()

  #----------------------------------------------------------------------

  def OnGetHnaMap(self, event):
    if self.frame.societyOpen:
      self.frame.closeSociety("society")

    if self.frame.agentLaydown.tempMappedSociety is None:
      self.frame.society = self.frame.mappedSociety.clone()
    else:
      self.frame.society = self.frame.agentLaydown.tempMappedSociety.clone()

    inclNodeAgent = True
    self.frame.societyViewer.UpdateControl(self.frame.society, inclNodeAgent)
    self.frame.ruleEditor.societyName.SetValue(self.frame.society.name)
    self.frame.societyOpen = 1
    self.frame.enableSocietySaveMenuItems()
    # set nameserver
    if self.frame.society.countHosts() > 0:
      self.frame.society.set_nameserver_host(self.frame.society.get_host(0).name)
    for node in self.frame.society.each_node():
      node.updateNameServerParam(self.frame.society.get_nameserver())

  #----------------------------------------------------------------------

  def OnUpdate(self, event):
    #self.log.WriteText("Stop time: %s\n" % time.ctime())
    self.StopAnimation()
    self.frame.server.Stop()
    self.frame.society = event.msg
    if self.frame.society:
      self.frame.societyViewer.UpdateControl(self.frame.society, true)
      self.frame.enableSocietySaveMenuItems()
      self.frame.ruleEditor.societyName.SetValue(self.frame.society.name)
      for node in self.frame.society.each_node():
        node.updateNameServerParam(self.frame.society.get_nameserver())
      self.frame.society.isDirty = False
      self.frame.societyOpen = 1
      #~ print self.frame.society.to_ruby()  # debug

  def OnSize(self, event):
    w,h = self.GetClientSizeTuple()
    self.list.SetDimensions(0, 0, w, h)

  def OnSelChanging(self, event):
    self.frame.editMenu.Enable(16, False)

  def OnSelChanged(self, event):
    #~ print "SocietyEditor::OnSelChanged"
    self.currentItem = event.GetItem()
    self.frame.societyViewer.removeHighlighting(self.currentItem)
    self.entityObj = self.getEntityObj()
    if not self.entityObj:
      event.Skip()
      return

    name = self.entityObj.name
    self.log.WriteText("Selected item: %s   " % name)
    self.log.WriteText("Rule: %s\n" % self.entityObj.rule)
    self.frame.editMenu.Enable(16, True)
    event.Skip()

  def OnRightClick(self, event):
    # 'event' is an instance of wxMouseEvent
    self.x = event.GetX()
    self.y = event.GetY()
    pt = event.GetPosition();
    item, flags = self.frame.societyViewer.HitTest(pt)
    if item.IsOk():
      self.frame.societyViewer.SelectItem(item)

  def OnRightUp(self, event):
    pt = event.GetPosition();
    item, flags = self.frame.societyViewer.HitTest(pt)
    if item.IsOk():  # need this to prevent sys crash when tree has no items
      #~ itemText = self.frame.societyViewer.GetItemText(item).getAllText()
      self.entityObj = self.frame.societyViewer.GetPyData(item)
      #self.log.WriteText("OnRightUp: %s\n" % itemText)
    else:
      self.entityObj = None
    if item.IsOk() or self.frame.societyViewer.isEmptyTree():
      menu = self.SetMenu()
      self.PopupMenu(menu, pt)
      menu.Destroy()
    event.Skip()

  def OnLeftDown(self, event):
    self.itemGrabbed = False  # reset
    self.frame.societyViewer = event.GetEventObject()
    pt = event.GetPosition();
    item, flags = self.frame.societyViewer.HitTest(pt)
    self.itemGrabbed = (flags == 16 or flags == 64 or flags == 2112 or \
                        flags == 4112 or flags == 4160)
    if item:  # need this to prevent sys crash when tree has no items
      self.entityObj = self.frame.societyViewer.GetPyData(item)
    event.Skip()

  def OnLeftUp(self, event):
    event.Skip()

  def OnMotion(self, event):  # multi drag & drop
    if event.Dragging() and event.LeftIsDown() and self.itemGrabbed:
      self.frame.societyViewer = event.GetEventObject()
      self.frame.societyViewer.isDragSource = True
      pt = event.GetPosition();
      item, flags = self.frame.societyViewer.HitTest(pt)
      selectedItemList = self.frame.societyViewer.GetSelections()
      if len(selectedItemList) == 0:
        self.frame.societyViewer.SelectItem(item)
        selectedItemList.append(item)
      self.log.WriteText("Dragging %d item(s)\n" % len(selectedItemList))  # debug
      draggedItemList = []
      # Ensure all the objects selected are of the same type by comparing
      # their class with the class of the first item in the list
      counter = 0
      for item in selectedItemList:
        itemData = self.frame.societyViewer.GetPyData(item)
        if counter == 0:
          draggedClass = itemData.__class__
        else:
          if itemData.__class__ != draggedClass:
            return
        if not isinstance(itemData, Agent) or (isinstance(itemData, Agent) and not itemData.isNodeAgent()):
          # This ensures we can't move a node agent off its node
          draggedItemList.append([item, itemData])
        counter += 1
      self.StartDrag([self.frame.societyViewer, draggedItemList])
    event.Skip()

  def OnEndLabelEdit(self, event):
    oldLabel = self.frame.societyViewer.GetItemText(self.currentItem) # still has the old label
    newLabel = self.frame.societyViewer.toTreeItemLabel(event.GetLabel())
    if newLabel:  # if the label was actually changed:
      #self.log.WriteText("Old label: " + oldLabel + "  New label: " + newLabel)
      self.frame.societyViewer.editLabelText(oldLabel, newLabel)

  def SetMenu(self):

    tID1 = 0
    tID2 = 1
    tID3 = 2
    tID4 = 3
    tID5 = 4
    tID6 = 5
    tID7 = 6
    tID8 = 7
    tID9 = 8
    tID10 = 9
    tID11 = 10
    tID12 = 11
    tID13 = 12
    tID14 = 13
    tID15 = 14
    tID16 = 15
    tID17 = 16
    tID18 = 17
    tID19 = 18
    tID20 = 19
    tID21 = 20
    tID22 = 21
    tID23 = 22
    tID24 = 23
    tID25 = 24

    menu = wxMenu()

    if self.frame.societyViewer.isEmptyTree():
      item = wxMenuItem(menu, tID24, "Open Society")
      item.SetBitmap(images.getSocietyBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID25, "Create New Society")
      item.SetBitmap(images.getSocietyBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID24, self.OnOpenSociety)
      EVT_MENU(self, tID25, self.OnCreateSociety)
      return menu

    if isinstance(self.entityObj, Society):
      # we either want to add a host or delete the society and all its subs.
      item = wxMenuItem(menu, tID1, "Add Host")
      item.SetBitmap(images.getHostBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID2, "Delete This Society")
      item.SetBitmap(images.getSocietyBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID3, "Rename Society")
      item.SetBitmap(images.getSocietyBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID1, self.OnAddHost)
      EVT_MENU(self, tID2, self.OnDeleteSociety)
      EVT_MENU(self, tID3, self.OnRename)
      return menu

    if isinstance(self.entityObj, Host):
      # we either want to add a node or delete the host and all its subs.
      item = wxMenuItem(menu, tID4, "Add Node")
      item.SetBitmap(images.getNodeBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID5, "Delete This Host")
      item.SetBitmap(images.getHostBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID6, "Rename Host")
      item.SetBitmap(images.getHostBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID23, "View/Edit Info")
      item.SetBitmap(images.getHostBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID4, self.OnAddNode)
      EVT_MENU(self, tID5, self.OnDeleteEntity)
      EVT_MENU(self, tID6, self.OnRename)
      EVT_MENU(self, tID23, self.OnEditNodeInfo)
      return menu

    if isinstance(self.entityObj, Node):
      # we either want to add a agent or delete the node and all its subs.
      item = wxMenuItem(menu, tID7, "Add Agent")
      item.SetBitmap(images.getAgentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID8, "Delete This Node")
      item.SetBitmap(images.getNodeBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID9, "Rename Node")
      item.SetBitmap(images.getNodeBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID10, "View/Edit Info")
      item.SetBitmap(images.getNodeBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID7, self.OnAddAgent)
      EVT_MENU(self, tID8, self.OnDeleteEntity)
      EVT_MENU(self, tID9, self.OnRename)
      EVT_MENU(self, tID10, self.OnEditNodeInfo)
      EVT_MENU(self, tID22, self.OnAddComponent)
      return menu

    if isinstance(self.entityObj, Agent):
      # we either want to add a component or delete the agent and all its subs.
      item = wxMenuItem(menu, tID11, "Add Component")
      item.SetBitmap(images.getComponentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID12, "Delete This Agent")
      item.SetBitmap(images.getAgentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID13, "Rename Agent")
      item.SetBitmap(images.getAgentBitmap())
      menu.AppendItem(item)
      if self.entityObj == self.entityObj.parent.nodeAgent:
        item.Enable(false)
      item = wxMenuItem(menu, tID14, "View/Edit Info")
      item.SetBitmap(images.getAgentBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID11, self.OnAddComponent)
      EVT_MENU(self, tID12, self.OnDeleteEntity)
      EVT_MENU(self, tID13, self.OnRename)
      EVT_MENU(self, tID14, self.OnEditNodeInfo)
      return menu

    if isinstance(self.entityObj, Component):
      # we either want to add a argument or delete the component and all its subs.
      item = wxMenuItem(menu, tID15, "Add Argument")
      item.SetBitmap(images.getArgumentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID16, "Delete This Component")
      item.SetBitmap(images.getComponentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID17, "Rename Component")
      item.SetBitmap(images.getComponentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID18, "View/Edit Info")
      item.SetBitmap(images.getComponentBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID15, self.OnAddArgument)
      EVT_MENU(self, tID16, self.OnDeleteEntity)
      EVT_MENU(self, tID17, self.OnRename)
      EVT_MENU(self, tID18, self.OnEditNodeInfo)
      return menu

    if isinstance(self.entityObj, Argument):
      # we either want to add a argument or delete the component and all its subs.
      item = wxMenuItem(menu, tID19, "Delete This Argument")
      item.SetBitmap(images.getArgumentBitmap())
      menu.AppendItem(item)
      item = wxMenuItem(menu, tID20, "Edit Argument")
      item.SetBitmap(images.getArgumentBitmap())
      menu.AppendItem(item)
      EVT_MENU(self, tID19, self.OnDeleteEntity)
      EVT_MENU(self, tID20, self.OnRename)
      return menu

  #************************************************************************

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

  def OnGetItemText(self, item, col):
    return "Item %d, column %d" % (item, col)

  def GetBitmap(self, text):
    txt = str(text).lower()
    if txt == 'society':   return self.societyImage
    if txt == 'host':      return self.hostImage
    if txt == 'node':      return self.nodeImage
    if txt == 'agent':     return self.agentImage
    if txt == 'component': return self.componentImage
    if txt == 'argument': return self.argumentImage
    return self.questionImage

###

  def OnCreateSociety(self, event):
    newSociety = self.frame.societyViewer.createSociety()
    self.frame.society = newSociety
    self.frame.societyOpen = 1
    self.frame.enableSocietySaveMenuItems()

  def OnAddHost(self, event):
    self.frame.societyViewer.addHost(self.frame.society)

  def OnAddNode(self, event):
    includeParams = True
    showNodeAgent = True
    self.frame.societyViewer.addNode(self.currentItem, includeParams, showNodeAgent)

  def OnAddAgent(self, event):
    includeClass = True
    self.frame.societyViewer.addAgent(self.currentItem, includeClass)

  def OnAddComponent(self, event):
    self.frame.societyViewer.addComponent(self.currentItem)

  def OnAddArgument(self, event):
    self.frame.societyViewer.addArgument(self.currentItem)

  def OnDeleteSociety(self, event):
    dlg = CougaarMessageDialog(self, "delete")
    self.KillIt = dlg.getUserInput()
    if self.KillIt == wxID_YES:
      self.frame.closeSociety("society")
      os.remove(self.frame.societyFile)  # delete the XML file from disk

  def OnDeleteEntity(self, event):
    deletedItems = self.frame.societyViewer.GetSelections()
    self.frame.societyViewer.deleteEntity(deletedItems)

  def OnRename(self, event):
    self.frame.societyViewer.EditLabel(self.currentItem)

  def OnEditNodeInfo(self, event):
    #Bring up a separate Frame to view/edit other info
    if not self.infoFrameOpen:  # only one may be open at a time
      nodeInfoEditor = NodeInfoEditor(self, self.log)
      nodeInfoEditor.Show(true)
      self.infoFrameOpen = 1

#----------------------------------------------------------------------

  def getEntityObj(self):
    return self.frame.societyViewer.GetPyData(self.currentItem)

#----------------------------------------------------------------------

  def enableButton(self, buttonName, enable=true):
    if buttonName == "openSocietyButton":
      self.openSocietyButton.Enable(enable)
    elif buttonName == "saveSocietyButton":
      self.saveSocietyButton.Enable(enable)
    elif buttonName == "closeSocietyButton":
      self.closeSocietyButton.Enable(enable)
    elif buttonName == "getHnaMapButton":
      self.getHnaMapButton.Enable(enable)
    else:
      raise Exception, "Attempting to enable/disable unknown button"

#----------------------------------------------------------------------

  def StartDrag(self, dataList):
    # The 'dataList' argument is a list, the first element of which is a reference to the
    # viewer which is the source of the drag.  The second element is list of lists, with each
    # of the element lists containing a tree item id plus the associated entity of a
    # Cougaar society to be dragged
    # NEW PART:
    # We want to store the entity in a Dictionary using entity.name as the key.  Then we
    # only want to pickle the entity name, not the whole entity obj.
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
    dataObj = wxCustomDataObject(wxCustomDataFormat("CougaarComponent"))
    dataObj.SetData(dataString)

    # Create the drop source and begin the drag and drop operation
    sourceViewer.setDropResult(0)  # reset
    dragSource = wxDropSource(self)
    dragSource.SetData(dataObj)
    self.frame.setDragSource(sourceViewer)
    result = dragSource.DoDragDrop(wxDrag_DefaultMove)
    altResult = sourceViewer.getDropResult()
    if altResult == wxDragNone:
      result = altResult
    sourceViewer.isDragSource = False

    # Tell the drag source what to do with the object that was dragged
    if result == wxDragMove:
      self.log.WriteText("DragDrop completed: %d item(s) moved\n" % len(treeItemList))  # debug
      for itemData in treeItemList:
        item = itemData[0]
        entity = itemData[1]
        #~ entity.delete_entity()  # delete object from the underlying society model
        if entity.has_changed_parent():
          entity.delete_from_prev_parent()  # delete object from the underlying society model
        sourceViewer.Delete(item) # delete item from the tree

    elif result == wxDragCopy:
      self.log.WriteText("Item copied\n")
    elif result == wxDragError:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drag & Drop Error\n")
    elif result == wxDragNone:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drop Rejected\n")
    elif result == wxDragCancel:
      self.frame.objCloset.clear()  # empty the closet
      self.log.WriteText("Drag Cancelled")
    else:
      self.log.WriteText("Drag & Drop totally hosed")

#************************************************************************
def runTest(frame, nb, log ): runApp(frame, nb, log)


def runApp( frame, nb, log ):
    win = SocietyEditorPanel( frame, nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
<H2>The CSMARTer Society Editor ...</H2>
<P>
To use, read in a society file. Then read in rules files and apply them as needed. Finally, write the society back out
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])
