# Name:         cougaar_drag-n-drop.py
# Purpose:     Specify classes for implementing Drag and Drop functionality
#                     in CSMARTer
#
# Author:       ISAT (P. Gardella)
#
# RCS-ID:       $Id: cougaar_DragAndDrop.py,v 1.2 2004-11-01 21:18:50 jblau Exp $
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
import cPickle
from ACMEPy.society import Society
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from ACMEPy.component import Component
from ACMEPy.argument import Argument

#************************************************************************
#  DnD classes
#************************************************************************

class CougaarDropTarget(wx.PyDropTarget):

  def __init__(self, window, log, frame, inclComponents=False):
    wx.PyDropTarget.__init__(self)
    self.log = log
    self.viewer = window
    self.frame = frame    # ref to the top-level CSmarter object
    self.inclComponents = inclComponents  # do we include components, too?
    self.mouseOverItem = self.viewer.GetRootItem()  # arbitrarily initialized to the root item
    self.isCopyOperation = False
    
    # Specify the type of data we will accept:
    self.format = wx.CustomDataFormat("CougaarComponent")
    self.dataObj = wx.CustomDataObject(self.format)
    self.SetDataObject(self.dataObj)
    
  # some virtual methods that track the progress of the drag
  def OnEnter(self, x, y, d):
    #~ self.log.WriteText("OnEnter: %d, %d, %d\n" % (x, y, d))
    #~ print "OnEnter: %d, %d, %d" % (x, y, d)
    if not self.viewer.isDragSource:
      self.viewer.UnselectAll()
    if d != wx.DragCopy:
      self.isCopyOperation = False
    else:
      self.isCopyOperation = True      
    return d
  
  def OnLeave(self):
    #~ self.log.WriteText("OnLeave\n")
    pass
  
  def OnDragOver(self, x, y, d):
    # The value returned here tells the source what kind of visual
    # feedback to give (i.e., what sort of cursor icon).  For example, 
    # if wxDragCopy is returned then only the copy cursor will be shown, 
    # even if the source allows moves.  You can use the passed in (x,y) to 
    # determine what kind of feedback to give.  In this case we return the 
    # suggested value which is based on whether the Ctrl key is pressed.
    #~ self.log.WriteText("OnDragOver: %d, %d, %d\n" % (x, y, d))
    
    if wx.Platform == '__WXMSW__':  # this method crashes in Linux, so only use w/ Windows
      #~ print "OnDragOver: %d" % d
      # This controls the icon associated with the mouse cursor when an item is being dragged.  
      # If the mouse cursor is over a valid drop target, we'll get the copy (if CTRL is held) or 
      # the move icon (if CTRL is not held).  If the mouse cursor is over an invalid drop target,
      # we'll get the "No drop" icon (circle with a slash through it).  Could not get the "No drop" 
      # icon to work in Linux.  In fact, the whole app crashes in Linux (Red Hat 8) with a 
      # "Segmentation fault".
      # 
      if d != wx.DragCopy:
        self.isCopyOperation = False
      else:
        self.isCopyOperation = True      
      if not self.mouseOverItem:  # properly initialize this in case it wasn't already
        self.mouseOverItem = self.viewer.GetRootItem()
      
      draggedEntity = self.frame.objCloset.values()[0]  # just get the first item; using it to determine its type
      treeItem, flag = self.viewer.HitTest(wx.Point(x,y))
      
      if treeItem.IsOk():
        if treeItem != self.mouseOverItem or not self.viewer.itemIsHighlighted(self.mouseOverItem):  # Only do this if the mouse position has changed
          self.viewer.removeHighlighting(self.mouseOverItem)  # un-hilite the previously moused-over item
          self.mouseOverItem = treeItem
          validItemFlags = [8, 16, 64, 128, 2056, 2112, 4104, 4112, 4160, 4224]
          if flag not in validItemFlags:
            self.dragOverRetVal = wx.DragNone  
            return self.dragOverRetVal  
          mouseOverObj = self.viewer.GetPyData(self.mouseOverItem)  
          
          # Following blocks describe invalid drop targets for various types of draggedEntity:
          if isinstance(draggedEntity, Host):  
            if isinstance(mouseOverObj, Node) or isinstance(mouseOverObj, Agent):  
              self.dragOverRetVal = wx.DragNone  
              return self.dragOverRetVal  
          
          elif isinstance(draggedEntity, Node):  
            if isinstance(mouseOverObj, Society) or isinstance(mouseOverObj, Agent):  
              self.dragOverRetVal = wx.DragNone  
              return self.dragOverRetVal  
          elif isinstance(draggedEntity, Agent) and isinstance(mouseOverObj, Society):  
            self.dragOverRetVal = wx.DragNone  
            return self.dragOverRetVal
          
          # Must be a valid drop target
          self.viewer.highlightItem(self.mouseOverItem, 'selectionBlue')
          self.dragOverRetVal = d  
          return self.dragOverRetVal  
        
        # The drop target the mouse is over is the same drop target as for the previous call of this method.  
        # So, return the same value.
        if not self.dragOverRetVal:
          self.dragOverRetVal = d  # if it's never been initialized, initialize it to the value of var 'd'
        return self.dragOverRetVal  # return same as was returned last time (mainly for when mouse position hasn't changed)
      
      # Mouse is over an invalid tree item, but previous tree item is still highlighted
      elif self.viewer.itemIsHighlighted(self.mouseOverItem):
        self.viewer.removeHighlighting(self.mouseOverItem)
        self.dragOverRetVal = wx.DragNone  
        return self.dragOverRetVal  
      
      # Mouse is over an invalid tree item
      else:
        self.dragOverRetVal = wx.DragNone  
        return self.dragOverRetVal
    
    else:  # if we're running on Unix, skip all the above stuff
      return d
  
  def OnDrop(self, x, y):
    #~ self.log.WriteText("OnDrop: %d %d\n" % (x, y))
    if wx.Platform == '__WXMSW__':
      #~ print "OnDrop: %d %d\n" % (x, y)
      self.viewer.removeHighlighting(self.mouseOverItem)
      self.viewer.SelectItem(self.mouseOverItem)
    return true
  
  def OnData(self, x, y, d):  # multi drag & drop
    # Called when OnDrop returns true.  Gets the data and does something with it.
    #~ self.log.WriteText("OnData: %d, %d, %d\n" % (x, y, d))
    #~ print "OnData: %d" % d
    entity = None
    sourceViewer = None  # the viewer that was the drag source
    successful = False
    isHomoDrop = False  # short for a homotypical drop; i.e., dropping one object onto another of the same type/class
    reorder = True  # where appearing, indicates we want to reorder, vice add, the entity
    orderAfterObj = None  # the obj after which a new entity is to be added in the society model
    itemList = []
    
    # If the viewer that's the drop target is one of the viewers on the agentLaydown panel, 
    # then change currentViewer to that viewer
    if self.viewer.parent == self.frame.agentLaydown:
      self.frame.agentLaydown.currentViewer = self.viewer
    
    # copy the data from the drag source to our data object
    if self.GetData():
      entityString = self.dataObj.GetData()
      # convert it back to a list obj 
      itemNameList = cPickle.loads(entityString) # a list of names of objects being dropped
      if len(itemNameList) > 0:
        entityName = itemNameList[0]  # just look at the first dropped name for now
        entity = self.frame.objCloset[entityName]  # get the obj out of the closet
        # Next few lines are nec because wxPyDropTarget can't be forced (in Linux, at 
        # least) to return anything other than what it's internally programmed to return
        # (despite use of a 'return' statement). So if we want to force it to return something
        # of our choosing, we must store the desired return value in the source viewer 
        # from where it can be retrieved by the drag source.
        sourceViewer = self.frame.getDragSource()  
      else:
        sourceViewer.setDropResult(wx.DragNone)
        return wx.DragNone
      
      # Populate variables we will need to update the destination tree
      receiverItem, flags = self.viewer.HitTest(wx.Point(x, y))
      iconType = None
      parentItem = None
      
      if receiverItem.IsOk():  # need this to prevent sys crash when tree has no items
        receiverData = self.viewer.GetPyData(receiverItem)
        
        if isinstance(entity, Host): 
          iconType = self.viewer.hostImage
          if isinstance(receiverData, Host):
            isHomoDrop = True
          elif not isinstance(receiverData, Society):
            sourceViewer.setDropResult(wx.DragNone)
            return wx.DragNone  # can only drop Hosts on a Society or another host
          
        elif isinstance(entity, Node): # if dragging a Node, ok to drop it on a Host or another Node
          iconType = self.viewer.nodeImage
          if isinstance(receiverData, Node):
            isHomoDrop = True
          elif not isinstance(receiverData, Host):
            sourceViewer.setDropResult(wx.DragNone)
            return wx.DragNone  # reject the drop operation
            
        elif isinstance(entity, Agent):  # if dragging an Agent, ok to drop it on a Host, Node, or another Agent
          iconType = self.viewer.agentImage
          if isinstance(receiverData, Host):  # if we drop it on a host:
            if receiverData.countNodes() == 0:  # if there are no nodes on this host, create one
              newNode = Node(receiverData.name + "_NODE_0")
              newNode.parent = receiverData
              receiverData.add_node(newNode)  # add it to the society object...
              # ...add it to the tree and make the node the new receiverItem/receiverData
              receiverItem = self.viewer.AppendItem(receiverItem, newNode.name, self.viewer.nodeImage)
              self.viewer.SetPyData(receiverItem, newNode)
              receiverData = newNode
            else:  # there is at least one node on the host already
              # make this node the new receiverItem to receive the dragged agent
              receiverItem, cookie = self.viewer.GetFirstChild(receiverItem, 1)  # ignore cookie
              receiverData = self.viewer.GetPyData(receiverItem)
          elif isinstance(receiverData, Agent):
            isHomoDrop = True
          elif not isinstance(receiverData, Node):
            sourceViewer.setDropResult(wx.DragNone)
            return wx.DragNone  # can't drop an agent on a component or argument
            
        elif isinstance(entity, Component): # ok to drop a component on an agent or another component
          iconType = self.viewer.componentImage
          # Strip off the source agent's name and prepend the destination agent's name
          entityStrippedName = entity.getStrippedName() # strip off the agent name prefix
          agentName = ''
          if isinstance(receiverData, Component):  # if we dropped it on another component
            isHomoDrop = True
            agentName = receiverData.parent.name
          elif isinstance(receiverData, Agent):
            agentName = receiverData.name
          #~ elif not isinstance(receiverData, Agent):
          else:
            sourceViewer.setDropResult(wx.DragNone)
            return wx.DragNone  # can't drop a component on a host, node, or argument
          entity.name = agentName + "|" + entityStrippedName
            
        elif isinstance(entity, Argument): # ok to drop an argument on a component or another argument
          iconType = self.viewer.argumentImage
          if isinstance(receiverData, Argument):
            isHomoDrop = True
          elif not isinstance(receiverData, Component):
            sourceViewer.setDropResult(wx.DragNone)
            return wx.DragNone  # can't drop an argument on a host, node, or agent
            
        else:  # what else could it be?
          sourceViewer.setDropResult(wx.DragNone)
          return wx.DragNone  # reject the drop operation
        
        if isHomoDrop:
          parentItem = self.viewer.GetItemParent(receiverItem)
          receiverData = self.viewer.GetPyData(parentItem)
        
        # Now make updates to the tree and the society model
        for entityName in itemNameList:
          entity = self.frame.objCloset[entityName]  # get the entity obj from the closet
          del self.frame.objCloset[entityName] # then remove it from the closet
          # We don't need agents marked for exclusion in the mappedSociety, so remove the mark
          if isinstance(entity, Agent) and self.viewer == self.frame.laydownViewer:
            entity.isExcluded = False
          entityLabel = entity.name
          # Update the tree first
          newItem = None
          insertAfterItem = None
          # If we're dropping one entity on another of the same type, we want to add
          # the new item in front of the one on which it was dropped.
          if isHomoDrop:
            insertAfterItem = self.viewer.GetPrevSibling(receiverItem)
            objDroppedOn = self.viewer.GetPyData(receiverItem)
            droppedOnNodeAgent = False
            if insertAfterItem.IsOk():
              orderAfterObj = self.viewer.GetPyData(insertAfterItem)
            elif isinstance(objDroppedOn, Agent) and objDroppedOn.isNodeAgent():
              orderAfterObj = objDroppedOn  # add it AFTER the node agent
              droppedOnNodeAgent = True
            else:  # receiverItem was the first child of the parent, so add at top
              orderAfterObj = receiverData
            
            # Now add the dropped item to the society model and tree (if it's not already there)
            entityAdded = receiverData.add_entity(entity, orderAfterObj, self.isCopyOperation)
            if entityAdded is not None:  # if it wasn't a dupe
              if insertAfterItem.IsOk():
                newItem = self.viewer.InsertItem(parentItem, insertAfterItem, entityLabel, iconType)
              elif droppedOnNodeAgent:  # insert it immediately AFTER the node agent
                newItem = self.viewer.InsertItemBefore(parentItem, 1, entityLabel, iconType)
              else:  # receiverItem was the first child of the parent, so add at top
                newItem = self.viewer.InsertItemBefore(parentItem, 0, entityLabel, iconType)
          else:
            entityAdded = receiverData.add_entity(entity, None, self.isCopyOperation)  # add it to its new location
            if entityAdded is not None:  # if it wasn't a dupe
              newItem = self.viewer.AppendItem(receiverItem, entityLabel, iconType)
          if newItem is not None:  # it was successfully added to the tree
            self.viewer.SetPyData(newItem, entity)
            # update the label
            if self.viewer.itemTextDict.has_key(entityLabel):
              label = self.viewer.itemTextDict[entityLabel]
              self.viewer.SetItemText(newItem, label)
            else:
              itemList.append(newItem)  # used later for updating facet display
            # If we moved around an entity marked for exclusion, preserve the highlighted label
            if (isinstance(entity, Agent) or isinstance(entity, Node) or isinstance(entity, Host)) \
                and entity.isExcluded:
              self.viewer.SetItemBackgroundColour(newItem, wx.RED)
              self.viewer.SetItemTextColour(newItem, wx.WHITE)
            
            # Do some things unique to agents
            if isinstance(entity, Agent):
              if self.inclComponents:
                self.bringComponents(newItem, entity)
              #~ self.viewer.sortAgents(receiverItem)
            elif isinstance(entity, Host):
              self.bringNodes(newItem, entity)
            elif isinstance(entity, Node):
              self.bringAgents(newItem, entity)
            elif isinstance(entity, Component):
              self.bringArguments(newItem, entity)
            #~ self.viewer.SortChildren(receiverItem)
            self.viewer.EnsureVisible(newItem)
            successful = True
          
          # The following ops on Host, Nodes, and Agents are necessary to keep the Pickler from
          # running amok and gobbling up massive quantities of memory after several drag/drops
          # Additional note: This is probably no longer necessary, but it's not hurting anything  
          # and may reduce memory usage somewhat.
          if isinstance(entity, Host):
            inclNodeAgent = True
            for node in entity.each_node():
              node.society = self.viewer.society
              for agent in node.each_agent(inclNodeAgent):
                agent.society = self.viewer.society
          elif isinstance(entity, Node) or isinstance(entity, Agent):
            entity.society = self.viewer.society
          
    if successful:
      # Update agent counter
      if self.viewer == self.frame.agentViewer:
        self.viewer.parent.agentViewerTotalLabel.SetLabel('Total Agents: ' + str(self.viewer.society.countAgents()))
      elif self.viewer == self.frame.laydownViewer:
        self.viewer.parent.laydownViewerTotalLabel.SetLabel('Total Agents: ' + str(self.viewer.society.countAgents()))
        
        # Update facet display
        if len(itemList) > 0 and hasattr(entity, 'facets'):
          # hasattr will only return False if the entity dropped is a Component or an Argument,
          # which means the DnD is being done in the SocietyEditor tab
          entityType = entity.__class__.__name__.lower()
          self.updateFacetDisplay(entityType, itemList)
      
      return d  # 'd' signals the source what to do with the original data (move, copy,
                # etc.)  In this case we just return the suggested value given to us.
                # NOTE: In Linux, at least, this method does not necessarily
                # return the value of 'd'.  It does in Windows 2000.  In Linux,
                # it returns "either wxDragCopy or wxDragMove [or wxDragCancel]
                # depending on the state of the keys (<Ctrl>, <Shift>, and <Alt>) at
                # the moment of drop."  (See "Drag and drop overview" in wxPython docs)
    else:
      sourceViewer.setDropResult(wx.DragNone)
      return wx.DragNone  # rejected drop

  def bringNodes(self, hostItem, host):
    for node in host.each_node():
      newNodeItem = self.viewer.AppendItem(hostItem, node.name, self.viewer.nodeImage)
      self.viewer.SetPyData(newNodeItem, node)
      self.updateFacetDisplay('node', self.viewer.getChildren(hostItem))
      self.bringAgents(newNodeItem, node)
    #~ self.viewer.SortChildren(hostItem)
  
  def bringAgents(self, nodeItem, node):
    inclNodeAgent = True
    if self.viewer == self.frame.laydownViewer or self.viewer == self.frame.agentViewer:
      inclNodeAgent = False
    for agent in node.each_agent(inclNodeAgent):  
      newAgentItem = self.viewer.AppendItem(nodeItem, agent.name, self.viewer.agentImage)
      self.viewer.SetPyData(newAgentItem, agent)
      self.updateFacetDisplay('agent', self.viewer.getChildren(nodeItem))
      if self.inclComponents:  # will use this in Society Editor, but not Agent Laydown
        self.bringComponents(newAgentItem, agent)
    #~ self.viewer.sortAgents(nodeItem)
  
  def bringComponents(self, agentItem, agent):
    for component in agent.each_component():
      newCompItem = self.viewer.AppendItem(agentItem, component.name, self.viewer.componentImage)
      self.viewer.SetPyData(newCompItem, component)
      self.bringArguments(newCompItem, component)
  
  def bringArguments(self, compItem, component):
      for argument in component.each_argument():
        newArgItem = self.viewer.AppendItem(compItem, argument.name, self.viewer.argumentImage)
        self.viewer.SetPyData(newArgItem, argument)
  
  #
  # Reshows facets that were showing before the drag/drop
  #
  # entityType:: [String]  One of [society | host | node | agent]  
  # droppedItemsList:: [List]  A list of wxTreeItemIds of the tree items that were dropped on the drop target
  #
  def updateFacetDisplay(self, entityType, droppedItemsList):
    updateFacetDisplay = True
    # reshow facets for the specified entity type
    self.frame.agentLaydown.showFacet('', entityType, update=updateFacetDisplay, itemList=droppedItemsList)  
