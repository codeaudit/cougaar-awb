#!/bin/env python
#----------------------------------------------------------------------------
# Name:         
# Purpose:      
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: societyViewer.py,v 1.4 2004-11-02 19:22:36 damoore Exp $
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

from __future__ import generators

import wx
import images
from societyFactoryServer import *
import string
from types import *
from insertion_dialog import *

SOCIETY = 'society'
HOST = 'host'
NODE = 'node'
AGENT = 'agent'
COMPONENT = 'component'
ARGUMENT = 'argument'
CONVERTED2DOT5 = True

class SocietyViewer(wx.TreeCtrl):
  def __init__(self, parent, id, name, pos = wx.DefaultPosition, size = wx.DefaultSize, 
                     style = wx.TR_HAS_BUTTONS, log = None, inclComponents=True):
    wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
    self.parent = parent
    self.id = id
    self.name = name
    self.pos = pos
    self.size = size
    self.style = style
    self.log = log
    self.addImages()
    self.inclComponents = inclComponents
    self.emptyTree = True
    self.firstNode = True
    self.society = None
    self.isDragSource = False
    self.dropResult = None
    self.itemTextDict = {}
    self.masterFacetList = []
    self.colourisedItemsList = []
    self.colourisedItemIndex = 0
    
    self.displayedFacetDict = {}
    self.displayedFacetDict['society'] = []
    self.displayedFacetDict['host'] = []
    self.displayedFacetDict['node'] = []
    self.displayedFacetDict['agent'] = []    
###
  
  def addImages(self):
    self.il = wx.ImageList(16,16)
    self.societyImage   = self.il.Add(images.getSocietyBitmap())
    self.hostImage      = self.il.Add(images.getHostBitmap())
    self.nodeImage      = self.il.Add(images.getNodeBitmap())
    self.agentImage     = self.il.Add(images.getAgentBitmap())
    self.componentImage = self.il.Add(images.getComponentBitmap())
    self.argumentImage  = self.il.Add(images.getArgumentBitmap())
    self.questionImage  = self.il.Add(images.getQuestionBitmap())
    self.SetImageList(self.il)
###

  def GetBitmap(self, text):
    txt = str(text).lower()
    if txt == SOCIETY:   return self.societyImage
    if txt == HOST:      return self.hostImage 
    if txt == NODE:      return self.nodeImage
    if txt == AGENT:     return self.agentImage 
    if txt == COMPONENT: return self.componentImage
    if txt == ARGUMENT:  return self.argumentImage
    return self.questionImage
###

  def UpdateControl(self, society, inclNodeAgent=False):   
    # Pull the objects that make up the society out of memory and build a tree. 
    # The PyData associated with each tree item is the object from the 
    # underlying society model that represents the tree item.
       
    self.society = society
    self.inclNodeAgent = inclNodeAgent
    
    #First destroy any existing tree
    if self.GetRootItem() is not None:
      #print 'existing tree... de-Struct'
      self.DeleteAllItems()
      self.emptyTree = True

    # Now build a new one
    numItems = 0  # keep a count
    self.societyNode = self.AddRoot(self.society.name, 0)
    if self.societyNode.IsOk():
      self.emptyTree = False
    self.hostItem = None  # a ref to the current host tree node...needed for Expand() method call
    self.nodeItem = None  # a ref to the current node tree node...needed for Expand() method call
    self.SetPyData(self.societyNode, self.society)
    numItems += 1
    for host in self.society.each_host():
      hostLabel = host.name
      self.hostItem = self.AppendItem(self.societyNode, hostLabel, 1)
      if not self.inclNodeAgent and host.isExcluded:
        self.SetItemBackgroundColour(self.hostItem, wx.RED)
        self.SetItemTextColour(self.hostItem, wx.WHITE)
      self.SetPyData(self.hostItem, host)
      self.Colourise(self.hostItem)
      numItems += 1
      for node in host.each_node():
        nodeLabel = node.name
        self.nodeItem = self.AppendItem(self.hostItem, nodeLabel, 2)
        if not self.inclNodeAgent and node.isExcluded:
          self.SetItemBackgroundColour(self.nodeItem, wx.RED)
          self.SetItemTextColour(self.nodeItem, wx.WHITE)
        self.SetPyData(self.nodeItem, node)
        self.Colourise(self.nodeItem)
        numItems += 1
        for agent in node.each_agent(inclNodeAgent):
          agentItem = None
          agentDisplayName = agent.name
          if inclNodeAgent and agent.isNodeAgent():
            # This ensures that, when the agents in a node are sorted, the node agent 
            # remains at the top of the list regardless of where it should fit alphabetically.
            agentItem = self.InsertItemBefore(self.nodeItem, 0, agentDisplayName, 3)
          else:
            agentItem = self.AppendItem(self.nodeItem, agentDisplayName, 3)
            if not self.inclNodeAgent and agent.isExcluded:
              self.SetItemBackgroundColour(agentItem, wx.RED)
              self.SetItemTextColour(agentItem, wx.WHITE)
          self.SetPyData(agentItem, agent)
          self.Colourise(agentItem)
          numItems += 1
          if self.inclComponents:
            for component in agent.each_component():
              compItem = self.AppendItem(agentItem, component.name, 4)
              self.SetPyData(compItem, component)
              self.Colourise(compItem)
              numItems += 1
              for argument in component.arguments:
                argItem = self.AppendItem(compItem, argument.name, 5)
                self.SetPyData(argItem, argument)
                self.Colourise(argItem)
                numItems += 1
        #~ self.sortAgents(self.nodeItem)
      #~ self.SortChildren(self.hostItem)
    #~ self.SortChildren(self.societyNode)
    #~ self.log.WriteText("Populated tree with %d items\n" % numItems )
    
    self.Expand(self.societyNode)
    #~ wx.LogMessage('Number of society entities modified: ' + str(len(self.colourisedItemsList)))

  #---------------------------------------------
  
  def Colourise(self, item):
    entityObj = self.GetPyData(item)
    ruleDescription = entityObj.rule
    boringRules = ['BASE', 'HAND EDIT', 'AUTO-BUILT', 'AUTO-CREATE']
    
    if ruleDescription.upper() in boringRules:
      return
    self.SetItemBackgroundColour(item, wx.CYAN)
    self.SetItemTextColour(item, wx.RED)
    self.colourisedItemsList.append(item) # keep a list of colourised items
  
  #---------------------------------------------
  
  def getNumEntitiesChanged(self):
    return str(len(self.colourisedItemsList))
  
  #---------------------------------------------
  
  def DeleteAllItems(self):
    wx.TreeCtrl.DeleteAllItems(self)
    self.emptyTree = True
  
  #---------------------------------------------
  
  def isEmptyTree(self):
    return self.emptyTree
  
  #---------------------------------------------
  
  def getSociety(self):
    return self.society
  
# ******************************************************
#       Expansion  methods
# ******************************************************

  # Expands the entire society down to the lowest level (Arguments)
  def expandEntireSociety(self):
    self.expandTree(self.GetRootItem())
    
  # Expands society element to show all hosts
  def expandSociety(self):
    self.expandTree(self.GetRootItem(), 0)
    
  # Expands host element to show all nodes
  def expandHosts(self):
    self.expandTree(self.GetRootItem(), 1)
  
  # Expands node element to show all agents
  def expandNodes(self):
    self.expandTree(self.GetRootItem(), 2)
  
  # Expands agent element to show all components
  def expandAgents(self):
    self.expandTree(self.GetRootItem(), 3)

  # Expands component element to show all arguments
  # (basically the same as expandEntireSociety(), but 
  # expandEntireSociety() will expand the entire tree
  # even if a new level is added, whereas this will still
  # only go down to the fourth level).
  def expandComponents(self):
    self.expandTree(self.GetRootItem(), 4)

  # Recursively iterates over a specified number of levels of the tree nodes and expands them.
  # A numLevels value of -1 means all levels of the tree are to be expanded
  def expandTree(self, treeNode, numLevels = -1, startingLevel = 0):
    #~ if treeNode.IsOk():
    self.Expand(treeNode)
    if self.GetChildrenCount(treeNode, False):
      startingLevel += 1
      if numLevels < 0 or startingLevel <= numLevels:
        cookie = -1
        child, cookie = self.GetFirstChild(treeNode, cookie)
        while child: 
          self.expandTree(child, numLevels, startingLevel)
          child, cookie = self.GetNextChild(treeNode, cookie)
      self.ScrollTo(self.GetRootItem())


# ******************************************************
#       Collapsing methods
# ******************************************************

  # Collapses society down so tree is displayed only as far as hosts
  def collapseHosts(self):
    self.collapseTree(self.GetRootItem(), 1)
    self.expandSociety()
  
  # Collapses society down so tree is displayed only as far as nodes
  def collapseNodes(self):
    self.collapseTree(self.GetRootItem(), 2)
    self.expandHosts()
  
  # Collapses society down so tree is displayed only as far as agents
  def collapseAgents(self):
    self.collapseTree(self.GetRootItem(), 3)
    self.expandNodes()

  # Collapses society down so tree is displayed only as far as components
  def collapseComponents(self):
    self.collapseTree(self.GetRootItem(), 4)
    self.expandAgents()

  # Recursively iterates over a specified number of levels of the tree nodes and expands them.
  # A numLevels value of -1 means all levels of the tree are to be expanded
  def collapseTree(self, treeNode, numLevels = -1, startingLevel = 0):
    if treeNode.IsOk():
      self.Collapse(treeNode)
      startingLevel += 1
      if numLevels < 0 or startingLevel <= numLevels:
        cookie = -1
        child, cookie = self.GetFirstChild(treeNode, cookie)
        while child.IsOk(): 
          self.collapseTree(child, numLevels, startingLevel)
          child, cookie = self.GetNextChild(treeNode, cookie)
          #~ child, cookie = self.GetNextChild(child, cookie)
  
  ##
  # Returns a list of the tree item id's for all the items of the same type 
  # and with the same parent as the argument.
  #
  # itemType::[String] 'society', 'host', 'node', 'agent', 'component', or 'argument'
  #
  def getItemList(self, itemType):
    hostList = self.getChildren(self.GetRootItem())
    nodeList = []
    agentList = []
    if itemType == "society":
      return [self.GetRootItem()]
    if itemType == "host":
      return hostList
    else:
      for hostItem in hostList:
        nodeList.extend(self.getChildren(hostItem))
    if itemType == "node":
      return nodeList
    else:
      for nodeItem in nodeList:
        agentList.extend(self.getChildren(nodeItem))
    if itemType == "agent":
      return agentList
    else:
      raise Exception, "Invalid item type specified"
  
  ##
  # Returns a list of tree item id's for all the children of the argument item.
  #
  # item::[wx.TreeItemId] The tree item for which a list of children is desired
  #
  def getChildren(self, item):
    children = []
    item, cookie = self.GetFirstChild(item, 1)
    if item.IsOk():
      children = self.addSiblings(item)
    return children
  
  ##
  # Returns a list of tree item id's for all the siblings of the argument item.
  # The list includes the tree item id for the argument item.
  #
  # item::[wx.TreeItemId] The tree item for which a list of siblings is desired
  #
  def getSiblings(self, item):
    parentItem = self.GetItemParent(item)
    return self.getChildren(parentItem)
  
  ##
  # Similar to getSiblings() except that this assumes the argument item is the
  # first child of the parent, so it doesn't need to find its parent or its first
  # sibling.  Return value is identical to what you would get with getSiblings(),
  # but this skips the steps of first finding the parent and then the first child.
  #
  # item::[wx.TreeItemId] The tree item for which a list of siblings is desired
  #  
  def addSiblings(self, item):
    itemList = []
    while item.IsOk():
      itemList.append(item)
      item = self.GetNextSibling(item)
    return itemList
  
  ##
  # Replaces one item in the tree with another.
  #
  # itemToBeReplaced::[wx.TreeItemId] The tree item to be replaced
  # newItemLabel::[TreeItemLabel] The text label for the new item to be inserted
  # iconType::[integer] The int representing the image icon associated with
  #                                    the entity object type
  #
  def replaceItem(self, itemToBeReplaced, newItemLabel, iconType, keepChildren=False):
    insertAfterItem = self.GetPrevSibling(itemToBeReplaced)
    parentItem = self.GetItemParent(itemToBeReplaced)
    itemText = newItemLabel.getAllText()  # turn TreeItemLabel obj into a String
    if insertAfterItem.IsOk():
      newItem = self.InsertItem(parentItem, insertAfterItem, itemText, iconType)
    else:  # receiverItem was the first child of the parent, so add at top
      newItem = self.InsertItemBefore(parentItem, 0, itemText, iconType)
    if keepChildren:
      self.transferChildren(itemToBeReplaced, newItem, iconType)
    return newItem
  
  ##
  # Transfers children from one parent item to another.  Operation is performed 
  # recursively, so the children's children get transferred, too.  PyData gets
  # transferred, too.
  #
  # fromParentItem::[wx.TreeItemId] The tree item from which children are transferred
  # toParentItem:: [wx.TreeItemId] The tree item to which children are transferred.
  # iconType:: [integer] The int representing the image icon associated with the parent item
  #
  def transferChildren(self, fromParentItem, toParentItem, iconType):
    children = self.getChildren(fromParentItem)
    for child in children:
      childObj = self.GetPyData(child)
      newChildItem = self.AppendItem(toParentItem, childObj.name, iconType+1)
      self.SetPyData(newChildItem, childObj)
      if self.ItemHasChildren(child):
        self.transferChildren(child, newChildItem, iconType+1)

  
  def findSpecificString(self, baseString, stringToFind, occurrenceNum):
    # Finds a specific occurrence of 'stringToFind' in a baseString that
    # may contain several occurrences.  The occurrence to find is
    # specified by 'occurrenceNum'.  An occurrenceNum of 1 would mean 
    # "find the first occurrence"; 2 would mean "find the second", etc.
    # Returns the index of the specified occurrence, or -1 if the stringToFind 
    # doesn't occur at least occurrenceNum times in baseString.
    index = 0
    beg = 0
    for j in range(occurrenceNum):
      if beg < len(baseString):
        index = baseString.find(stringToFind, beg)
        if index == -1:
          return index
        beg = index + 1
      else:
        return -1
    return index
  
  #*******************************************************************
  
  def deleteEntity(self, deletedItems):
    type = None
    okToDelete = True
    
    # Verify that selected items are all of the same type
    deletedObjects = []
    for item in deletedItems:
      deletedObjects.append(self.GetPyData(item))
    selectedTypesOk = self.verifyMultiSelectTypes(deletedObjects)
    
    if selectedTypesOk:
      if self.name == 'laydownViewer':
        msg = 'If you delete this agent, it will not be unassigned, ' + \
                    'it will be destroyed.\n\nAre you sure you want to delete this agent?'
        dlg = CougaarMessageDialog(self, 'delete', msg)
        choice = dlg.getUserInput()
        if choice == wx.ID_NO:
          okToDelete = False
        
      if okToDelete:
        for deletedItem in deletedItems:
          deletedObj = self.GetPyData(deletedItem)
          if isinstance(deletedObj, Agent) and deletedObj.isNodeAgent():
            self.log.WriteText("Can't delete the Node Agent.\n")
          else:
            deletedObj.delete_entity()  # deletes itself
            if isinstance(deletedObj, Agent):
              deletedObj.society.adjustAgentCount(False)
            self.Delete(deletedItem)
  
  #*******************************************************************

  def createSociety(self):
    self.newEntityName = None
    NewEntityDialog(self, "New Society:")  # assigns a value to the above variable
    if self.newEntityName is not None:
      newSociety = Society(str(self.newEntityName), "Hand edit")
      newSociety.isDirty = True
      self.UpdateControl(newSociety)
      return newSociety
  
  #*******************************************************************
  
  def addHost(self, society):
    self.newEntityName = None
    NewEntityDialog(self, "New Host:")  # assigns a value to the above variable
    if self.newEntityName is not None:
      newHost = Host(str(self.newEntityName), "Hand edit")
      verifyHost = society.add_host(newHost)
      if verifyHost is not None:
        newItem = self.AppendItem(self.GetRootItem(), newHost.name, 1)
        self.SetPyData(newItem, newHost)
        self.SortChildren(self.GetRootItem())
        self.EnsureVisible(newItem)
  
  #----------------------------------------------------------------------
  
  def addNode(self, hostItem, includeParams=False, showNodeAgent=False):
    self.newEntityName = None
    self.newNodeClass = None
    self.newProgParams = None
    self.newEnvParams = None
    self.newVmParams = None
    if includeParams:
      NewNodeDialog(self)  # assigns values to all the above variables
    else:
      NewEntityDialog(self, "New Node:")  # assigns value to newEntityName
    if self.newEntityName is not None:
      newNode = Node(str(self.newEntityName), "Hand edit")
      if includeParams:
        # Add node parameters
        newNode.klass = str(self.newNodeClass)
        progParams = str(self.newProgParams).split("\n")
        envParams = str(self.newEnvParams).split("\n")
        vmParams = str(self.newVmParams).split("\n")
        progParamList = []
        envParamList = []
        vmParamList = []
        for param in progParams:
          if len(param) > 0:
            progParamList.append(ProgParameter(param))
        newNode.add_prog_parameters(progParamList)
        for param in envParams:
          if len(param) > 0:
            envParamList.append(EnvParameter(param))
        newNode.add_env_parameters(envParamList)
        for param in vmParams:
          if len(param) > 0:
            if param.startswith("-Dorg.cougaar.node.name"):
              vmParamList.insert(0, VMParameter("-Dorg.cougaar.node.name=" + newNode.name))
            else:
              vmParamList.append(VMParameter(param))
        newNode.add_vm_parameters(vmParamList)
      verifyNode = self.GetPyData(hostItem).add_node(newNode)
      # If verifyNode is None, it means the new node couldn't be added because a
      # node by that name already exists.
      if not verifyNode:
        self.log.WriteText("Unable to add duplicate Node: %s\n" % newNode.name)
      else:
        newItem = self.AppendItem(hostItem, newNode.name, 2)
        self.SetPyData(newItem, newNode)
        #~ self.SortChildren(hostItem)
        self.EnsureVisible(newItem)
        if showNodeAgent:
          newAgentItem = self.AppendItem(newItem, newNode.nodeAgent.name, 3)
          self.SetPyData(newAgentItem, newNode.nodeAgent)
  
  #----------------------------------------------------------------------
  
  def addAgent(self, nodeItem, includeClass=False):
    self.newEntityName = None
    self.newAgentClass = None
    if includeClass:
      NewAgentDialog(self)  # assigns values to all the above variables
    else:
      NewEntityDialog(self, "New Agent:")  # assigns value to newEntityName
    if self.newEntityName is not None:   
      if includeClass:
        newAgent = Agent(str(self.newEntityName), str(self.newAgentClass), "Hand edit")
      else:
        newAgent = Agent(str(self.newEntityName), rule="Hand edit")
      node = self.GetPyData(nodeItem)
      verifyAgent = node.add_agent(newAgent)
      node.society.adjustAgentCount(True)
      if verifyAgent is not None:
        newItem = self.AppendItem(nodeItem, newAgent.name, 3)
        self.SetPyData(newItem, newAgent)
        #~ self.sortAgents(nodeItem)
        self.EnsureVisible(newItem)
  
  #----------------------------------------------------------------------

  def addComponent(self, parentItem):
    self.newComponentName = None
    self.newComponentClass = None
    self.newComponentPriority = None
    self.newComponentInsertionPoint = None
    self.newComponentOrder = None
    NewComponentDialog(self)  # assigns values to all the above variables
    if self.newComponentName is not None:
      name =str(self.newComponentName)
      klass = str(self.newComponentClass)
      priority = str(self.newComponentPriority)
      insertPt = str(self.newComponentInsertionPoint)
      order = str(self.newComponentOrder)
      newComp = Component(name, klass, priority, insertPt, order, "Hand edit")
      parentObj = self.GetPyData(parentItem)
      verifyComponent = parentObj.add_component(newComp)
      # Only add it to the tree if it's a child of an Agent.  If it's a child of a Node,
      # it belongs on the Info tree.
      if isinstance(parentObj, Agent):
        newItem = self.AppendItem(parentItem, newComp.name, 4)
        self.SetPyData(newItem, newComp)
        self.EnsureVisible(newItem)
  
  #----------------------------------------------------------------------

  def addArgument(self, componentItem):
    self.newEntityName = None
    NewEntityDialog(self, "New Argument:")  # assigns a value to the above variable
    if self.newEntityName is not None:
      newArg = Argument(str(self.newEntityName), "Hand edit")
      self.GetPyData(componentItem).add_argument(newArg)
      newItem = self.AppendItem(componentItem, newArg.name, 5)
      self.SetPyData(newItem, newArg)
      self.EnsureVisible(newItem)
  
  #----------------------------------------------------------------------
  
  def sortAgents(self, nodeItem, agentItemList=None):
    if self.inclNodeAgent:
      if agentItemList is None:
        agentItemList = self.getChildren(nodeItem)
      for agentItem in agentItemList:
        agentItemLabel = self.GetItemText(agentItem)
        agentName = agentItemLabel.getItemName()
        if agentName.startswith("!"):
          self.SortChildren(nodeItem)
          agentItemLabel.setItemName(agentName[1:])
          self.SetItemText(agentItem, agentItemLabel)
          break
        #~ elif agentItemLabel == self.GetItemText(nodeItem):
        elif agentName == self.GetItemText(nodeItem).getItemName():
          agentItemLabel.setItemName("!" + agentName)
          #~ self.SetItemText(agentItem, "!" + agentItemLabel)
          self.SetItemText(agentItem, agentItemLabel)
          self.sortAgents(nodeItem, agentItemList)
    else:
      self.SortChildren(nodeItem)
  
  #----------------------------------------------------------------------
  
  def verifyMultiSelectTypes(self, itemsList):
    # Verifies that each item selected as part of a multi-select is of the same type
    baseClass = None
    for item in itemsList:
      if baseClass is None:
        baseClass = item.__class__
      elif item.__class__ != baseClass:
        msg = '''When selecting multiple items, all the items must be of the same type.'''
        dlg = wx.MessageDialog(self, msg, style = wx.CAPTION | wx.OK | 
             wx.THICK_FRAME | wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        return False
    return True
  
  #----------------------------------------------------------------------
  
  # Change the part of the item label that represents the entity name.
  # Note that this does not allow changes to any facets that may be displayed.
  #
  # oldLabel:: [TreeItemLabel]  Label prior to user edit
  # newLabel:: [TreeItemLabel]  Label after user edit
  #
  def editLabelText(self, oldLabel, newLabel):
    # Change the underlying Society:
    renamedObj = self.GetPyData(self.parent.currentItem)
    name = renamedObj.rename(newLabel.getItemName())
    msg = oldLabel.itemName + " renamed to " + newLabel.itemName
    
    # If the new name duplicates a name already used, the society will not allow the change.
    # In that case, replaceItem() will return the original name of the entity.
    if name == oldLabel.getItemName():  # New name was a dupe. Return the tree item label to its orig value.
      self.parent.log.WriteText("Unable to rename: name already taken\n")
      msg = msg +  ", but new name is a dupe; rename cancelled."  
      print msg
      return False
    
    elif oldLabel.hasTextElements():  # It is a valid new name, but don't allow changes to displayed facets, if any
      newLabel.textElements = oldLabel.textElements
      itemImage = self.GetItemImage(self.parent.currentItem)
      keepChildren = True
      newItem = self.replaceItem(self.parent.currentItem, newLabel, itemImage, keepChildren)
      self.SetPyData(newItem, self.parent.entityObj)
      self.Delete(self.parent.currentItem)
      self.UnselectAll()
      self.SelectItem(newItem)
    
    # If the item renamed was a node, rename its node agent, too
    if isinstance(self.parent.entityObj, Node):
      agents = self.getChildren(self.parent.currentItem)
      for agent in agents:
        if self.GetItemText(agent).getItemName() == oldLabel.getItemName():
          try:
            self.SetItemText(agent, self.toTreeItemLabel(newLabel.getItemName()))
          except AssertionError:
            # wx.TreeCtrl.SetItemText(item, label) is only supposed to work with single 
            # selection controls, but this is a valid use of that method and it seems to
            # work even though this is a multiple selection control, so just swallow the 
            # exception.
            #~ print "AssertionError raised in SocietyEditor::OnEndLabelEdit()"
            pass
          agentObj = self.GetPyData(agent)
          agentObj.rename(newLabel.getItemName())
          # Now do the same for Components of the agent
          self.renameComponents(agent, oldLabel.getItemName(), newLabel.getItemName())
          break
      if not self.inclNodeAgent:
        # The node agent will not have been included in the operation above, so do it now
        nodeAgent = self.parent.entityObj.nodeAgent
        for comp in nodeAgent.each_component():
          compName = self.getNewComponentName(comp.name, oldLabel.getItemName(), newLabel.getItemName())
          comp.rename(compName)
    
    # If the item renamed was an agent, rename its components, too
    elif isinstance(self.parent.entityObj, Agent):
      self.renameComponents(self.parent.currentItem, oldLabel.getItemName(), newLabel.getItemName())
      
    return True
  
  #------------------------------------------------------------------------------------
  
  def renameComponents(self, agentItem, oldAgentName, newAgentName):
    components = self.getChildren(agentItem)
    if len(components) > 0:
      # The agent has some children in the tree
      for compItem in components:
        compName = self.GetItemText(compItem).getItemName()
        compName = self.getNewComponentName(compName, oldAgentName, newAgentName)
        try:
          #~ self.SetItemText(compItem, compName)
          self.SetItemText(compItem, self.toTreeItemLabel(compName))
        except AssertionError:
          #~ print "AssertionError raised in SocietyViewer::renameComponents()"
          pass
        compObj = self.GetPyData(compItem)
        compObj.rename(compName)
    else:
      # Agent has no children in the tree...but could still have components that are not 
      # in the tree if the current panel is AgentLaydown.  In this case, no need to 
      # update the tree, just the society model.
      agentObj = self.GetPyData(agentItem)
      for component in agentObj.each_component():
        name = self.getNewComponentName(component.name, oldAgentName, newAgentName)
        component.rename(name)
      
  #------------------------------------------------------------------------------------
  
  def getNewComponentName(self, oldCompName, oldAgentName, newAgentName):
    if oldCompName.startswith(oldAgentName):
      compNameParts = oldCompName.split('|')
      return newAgentName + '|' + compNameParts[1]
    return oldCompName
  
  #------------------------------------------------------------------------------------
  
  def setDropResult(self, result):
    self.dropResult = result
  
  #------------------------------------------------------------------------------------
  
  def getDropResult(self):
    return self.dropResult
  
  #------------------------------------------------------------------------------------
  
  ##
  # Finds the tree item with the specified label and highlights it in the tree viewer
  #
  # itemLabel::[String] The text label associated with the tree item sought
  # caseSearchDesired:: [boolean] Flag to indicate if search should be case-sensitive
  #
  def findItem(self, itemLabel, caseSearchDesired=False, newSearch=True):
    if newSearch:
      self.searchResultSet = []
      self.currentResult = 0
      self.showNextItem = True
      if not caseSearchDesired:
        itemLabel = itemLabel.upper()
      # Start looking at the root item (i.e., the society)
      self.searchTree(itemLabel, self.GetRootItem(), 1, caseSearchDesired)
      moreToFind = True
      if len(self.searchResultSet) == 0:
        self.showNotFoundDialog()
        moreToFind = False
      self.parent.frame.enableFindNextMenuItem(moreToFind)
    else:
      self.currentResult += 1
      moreToFind = True
      if len(self.searchResultSet) > self.currentResult:
        # there is another result to show, so show it
        self.removeHighlighting(self.searchResultSet[self.currentResult-1])
        self.highlightItem(self.searchResultSet[self.currentResult])
      else:
        self.showNotFoundDialog()
        moreToFind = False
        self.parent.frame.enableFindNextMenuItem(False)
  
  def searchTree(self, labelToFind, treeNode, cookie, caseSearchDesired):
    if treeNode.IsOk():
      self.currentLabel = self.GetItemText(treeNode).getItemName()
      if not caseSearchDesired:
        self.currentLabel = self.currentLabel.upper()
      if self.currentLabel.find(labelToFind) >= 0:
        # found an occurrence; add it to the result set
        self.searchResultSet.append(treeNode)
        if self.showNextItem:
          # show user the item, and while user is pondering it, continue search for more occurrences
          self.highlightItem(treeNode) # will only be called the first time (see next line)
          self.showNextItem = False
      child, cookie = self.GetFirstChild(treeNode, cookie)
      while child.IsOk(): 
        self.searchTree(labelToFind, child, cookie, caseSearchDesired)
        child, cookie = self.GetNextChild(treeNode, cookie)
  
  def highlightItem(self, item, color='blue'):
    self.EnsureVisible(item)
    print 'highlightItem:Item', item
    if color == 'blue':
      bgcolor = wx.NamedColour('BLUE')
    elif color == 'gray':
      bgcolor = wx.NamedColour('LIGHT GREY')
    else:
      bgcolor = wx.Colour(24, 28, 123)  # dark navy blue
    self.SetItemBackgroundColour(item, bgcolor)
    self.SetItemTextColour(item, wx.WHITE)
  
  def removeHighlighting(self, item):
    print 'removeHighlighting: old Item', item 
    self.SetItemBackgroundColour(item, wx.WHITE)
    self.SetItemTextColour(item, wx.BLACK)
  
  def itemIsHighlighted(self, item):
    return self.GetItemBackgroundColour(item) != wx.WHITE
  
  def showNotFoundDialog(self):
    dlg = CougaarMessageDialog(self, "info", "Item not found")
    dlg.display()
  
  ##
  # Returns a two-tuple containing the wx.TreeItemId of the item and its PyData object
  # or None if the item was not found
  #
  def getItemByLabel(self, label, parentNode):
    self.searchResultSet = []
    item = None
    entity = None
    self.showNextItem = False
    self.searchTree(label, parentNode, 1, True)
    if len(self.searchResultSet) > 0:  # we'll just take the first one
      item = self.searchResultSet[0]
    if item is not None:
      entity = self.GetPyData(item)
    return item, entity
  
  # ---------------------------------------------------------------------------------------------
  
  # Converts the society in the wx.TreeCtrl into a string in XML format.
  #
  # lowestLevel::[String] A type of Cougaar entity that is the lowest level in 
  # the hierarchy that will be included in the resulting XML string.  Valid
  # values are "all", "host" or "hosts", "node" or "nodes", "agent" or "agents", 
  # "component" or "components", and "argument" or "arguments".  For 
  # example, "to_xml('agents')" will show the society, hosts, nodes, and
  # agents in the XML, but no components or arguments.  The default value
  # of "all" will result in an XML string that contains all the Cougaar entities
  # that exist in the society.
  #
  # Note: the XML string produced is a stripped-down version designed for use
  # with the HNA Laydown function, so no XML attributes other than the name
  # are included for any entity.  It is envisioned that this method will only be 
  # used for saving the HNA Mapped society.
  #
  def to_xml(self, lowestLevel='all'):
    self.xml = "<?xml version='1.0'?>\n"
    self.currHost = None
    self.currNode = None
    if lowestLevel.lower() == 'all':
      numLevels = -1
    elif lowestLevel.lower() == 'host' or lowestLevel.lower() == 'hosts':
      numLevels = 1
    elif lowestLevel.lower() == 'node' or lowestLevel.lower() == 'nodes':
      numLevels = 2
    elif lowestLevel.lower() == 'agent' or lowestLevel.lower() == 'agents':
      numLevels = 3
    elif lowestLevel.lower() == 'component' or lowestLevel.lower() == 'components':
      numLevels = 4
    elif lowestLevel.lower() == 'argument' or lowestLevel.lower() == 'arguments':
      numLevels = 5
    self.build_xml(self.GetRootItem(), 1, numLevels)
    self.firstNode = True  # reset
    return self.xml
  
  # Recursively iterates over a specified number of levels of the tree nodes and uses
  # the tree item label to construct a String in XML format.
  # A numLevels value of -1 means all levels of the tree are to be included.
  def build_xml(self, treeNode, cookie, numLevels=-1, treeLevel = 0):
    self.alreadyClosed = False
    hasFacets = False
    tab = 4 * ' '  # 4 spaces
    if treeNode.IsOk():
      if treeLevel == 0:
        self.xml = self.xml + "<society name='"+ self.getLabel(treeNode) +"'"
      elif treeLevel == 1:
        hostName = self.getLabel(treeNode)
        indent = tab * treeLevel
        self.xml = self.xml + indent + "<host name='" + hostName +"'"
        #~ self.xml = self.xml + "  <host name='" + hostName +"'"
        self.currHost = self.society.get_host_by_name(hostName)
        if self.currHost is None:
          msg = 'Error building XML due to invalid host name: ' + hostName
          dlg = CougaarMessageDialog(self, "error", msg)
          dlg.display()
          self.xml = "xxx"
          return
        if len(self.currHost.facets) > 0:
          hasFacets = True
          self.xml = self.xml + ">\n"
          for facet in self.currHost.facets:
            self.xml = self.xml + facet.to_xml(2)
          self.alreadyClosed = True
      elif treeLevel == 2:
        nodeName = self.getLabel(treeNode)
        indent = tab * treeLevel
        self.xml = self.xml + indent + "<node name='" + nodeName +"'"
        #~ self.xml = self.xml + "    <node name='" + nodeName +"'"
        self.currNode = self.currHost.get_node_by_name(nodeName)
        if self.currNode is None:
          msg = 'Error building XML due to invalid node name: ' + nodeName
          dlg = CougaarMessageDialog(self, "error", msg)
          dlg.display()
          self.xml = "xxx"
          return
        if len(self.currNode.facets) > 0:
          hasFacets = True
          self.xml = self.xml + ">\n"
          for facet in self.currNode.facets:
            self.xml = self.xml + facet.to_xml(3)
          self.alreadyClosed = True
      elif treeLevel == 3:
        #~ self.firstNode = False
        indent = tab * treeLevel
        self.xml = self.xml + indent + "<agent name='" + self.getLabel(treeNode) +"'"
        #~ self.xml = self.xml + "      <agent name='" + self.getLabel(treeNode) +"'"
      elif treeLevel == 4:
        indent = tab * treeLevel
        self.xml = self.xml + indent + "<component name='" + self.getLabel(treeNode) +"'"
        #~ self.xml = self.xml + "        <component name='" + self.getLabel(treeNode) +"'"
      elif treeLevel == 5:
        indent = tab * treeLevel
        self.xml = self.xml + indent + "<argument>" + self.getLabel(treeNode)
        #~ self.xml = self.xml + "          <argument>" + self.getLabel(treeNode)
      treeLevel += 1
      keepGoing = False
      if numLevels < 0 or treeLevel <= numLevels:
        keepGoing = True
      child, cookie = self.GetFirstChild(treeNode, cookie)
      childCount = 0
      while child.IsOk() and keepGoing: 
        if not self.alreadyClosed:
          self.xml = self.xml + ">\n"
        else:
          self.alreadyClosed = False
        childCount += 1
        self.build_xml(child, cookie, numLevels, treeLevel)
        child, cookie = self.GetNextChild(treeNode, cookie)
      #~ if childCount == 0 and not self.firstNode:
      if childCount == 0 and not hasFacets:
        self.xml = self.xml + "/>\n"
        self.alreadyClosed = True
      elif treeLevel == 1:
        self.xml = self.xml + "</society>\n"
      elif treeLevel == 2:
        indent = tab * (treeLevel-1)
        self.xml = self.xml + indent + "</host>\n"
      elif treeLevel == 3:
        indent = tab * (treeLevel-1)
        self.xml = self.xml + indent + "</node>\n"
      elif treeLevel == 4:
        indent = tab * (treeLevel-1)
        self.xml = self.xml + indent + "</agent>\n"
      elif treeLevel == 5:
        indent = tab * (treeLevel-1)
        self.xml = self.xml + indent + "</component>\n"
      elif treeLevel == 6:
        self.xml = self.xml + "</argument>\n"
      #~ if self.firstNode:
        #~ self.firstNode = False
  
  #----------------------------------------------------------------------
  
  # Strips off any facets that may be displayed in the tree label.  Also
  # strips off any spaces that may be at either end of the entity name.
  #
  # treeNode::[wx.TreeItemId] The ID of the current tree item
  #
  def getLabel(self, treeNode):
    return self.GetItemText(treeNode).getItemName()
  
  #----------------------------------------------------------------------
  
  # Returns a list of the facet types currently displayed in the tree 
  # view for items of the specified type.
  #
  # entityType:: [String]  One of ['society' |'host' | 'node' | 'agent']
  # 
  def getDisplayedFacets(self, entityType):
    if self.displayedFacetDict.has_key(entityType):
      return self.displayedFacetDict[entityType]
    raise Exception, "Bad entity type provided as argument"
  
  #----------------------------------------------------------------------
  
  # Adds a new facet type to the list of facets currently displayed.
  #
  # entityType:: [String]  One of ['society' |'host' | 'node' | 'agent']
  # facetType:: [String] The new facet type that is now displayed
  #
  def addDisplayedFacet(self, entityType, facetType):
    facetList = []
    if self.displayedFacetDict.has_key(entityType):
      facetList = self.displayedFacetDict[entityType]
    else:
      raise Exception, "Bad entity type provided as argument"
    facetList.append(facetType)
  
  #----------------------------------------------------------------------
  
  # Removes a facet type from the list of facets currently displayed.
  #
  # entityType:: [String]  One of ['society' |'host' | 'node' | 'agent']
  # facetType:: [String] The facet type to be removed
  #
  def removeDisplayedFacet(self, entityType, facetType):
    facetList = []
    if self.displayedFacetDict.has_key(entityType):
      facetList = self.displayedFacetDict[entityType]
      if facetType == 'all':
        for i in range(len(facetList)):
          facetList.pop()  # empty out the List
        return
    
    facetsToRemove = []
    for facet in facetList:
      if facet == facetType:
        facetsToRemove.append(facet)
    for facet in facetsToRemove:
      facetList.remove(facet)
  
  #----------------------------------------------------------------------
  
  # Returns a list of the society model objects corresponding to each of the
  # selected tree items.
  #
  def getSelectedObjects(self):
    selectedObjList = []
    selectedItems = self.GetSelections()
    for item in selectedItems:
      selectedObjList.append(self.GetPyData(item))
    return selectedObjList
  
  #----------------------------------------------------------------------
  
  # Returns True if the specified facetType is currently displayed
  # for the specified entityType; else, returns False
  #
  # facetType::[String]  One of [society-all | host-all | node-all | agent-all | enclave | service | role]
  # entityType:: [String] One of [society | host | node | agent]
  #
  def isFacetDisplayed(self, facetType, entityType):
    facetsDisplayed = self.getDisplayedFacets(entityType)
    if facetType in facetsDisplayed:
      return True
    return False
  
  #----------------------------------------------------------------------
  
  # Overrides wx.TreeCtrl::GetItemText(wx.TreeItemId) to allow use of 
  # a TreeItemLabel obj rather than a wx.String as the item text.
  # Returns the TreeItemLabel obj associated with the specified item.
  #
  # itemId:: [wx.TreeItemId]  The item whose text is sought
  #
  def GetItemText(self, itemId):
    entity = self.GetPyData(itemId)
    if self.itemTextDict.has_key(entity.name):
      return self.itemTextDict[entity.name]
    return self.toTreeItemLabel(wx.TreeCtrl.GetItemText(self, itemId))
  
  #----------------------------------------------------------------------
  
  # Overrides wx.TreeCtrl::SetItemText(wx.TreeItemId, wx.String) to allow use of a TreeItemLabel 
  # obj rather than a wx.String as the item text.
  # 
  # itemId:: [wx.TreeItemId]  The tree item whose text is to be set
  # treeItemLabel:: [TreeItemLabel]  The new text to be associated with the given tree item.
  #
  def SetItemText(self, itemId, treeItemLabel):
    try:
      wx.TreeCtrl.SetItemText(self, itemId, treeItemLabel.getAllText())
    except AssertionError:
      #~ pass  # swallow this annoying exception, which shouldn't be raised in the first place
      print "AssertionError raised by wx.Python on wx.TreeCtrl::SetItemText()"
    self.itemTextDict[treeItemLabel.getItemName()] = treeItemLabel  # hang onto a ref to this TreeItemLabel
  
  #----------------------------------------------------------------------
  
  # Overrides wx.TreeCtrl::Delete(wx.TreeItemId) to allow a TreeItemLabel that may have
  # been associated with the specified item to be removed before the item is deleted.
  #
  # itemId:: [wx.TreeItemId]  The tree item to be deleted.
  def Delete(self, itemId):
    label = self.GetItemText(itemId)
    itemName = label.getItemName()
    if self.itemTextDict.has_key(itemName):
      del self.itemTextDict[itemName]
    wx.TreeCtrl.Delete(self, itemId)
  
  #----------------------------------------------------------------------
  
  def toTreeItemLabel(self, itemText):
    itemName = None
    tempTextElements = []
    textElements = {}
    textList = []
    index = itemText.find(' (')
    if index == -1:
      itemName = itemText
    else:
      itemName = itemText[:index]
      tempTextElements = str(itemText[index+2:]).split(')  (')
    for text in tempTextElements:
      if text.endswith(') '):
        text = text[:-2]  # strip off the closing paren
        textList.append(text)
      # There's no way to know from looking what facet type is represented by the facet
      # value that's displayed, so we'll just default it to 'all'.  It's not really important 
      # because this method should never be called when there are ANY text elements
      # present.  Whenever a text element is added, the SetItemText() method saves
      # the TreeItemLabel into a Dictionary, so we shouldn't be converting a string to
      # a TreeItemLabel for any item that already has facets displayed.
    if len(textList) > 0:
      textElements['all'] = textList
    treeItemLabel = TreeItemLabel(itemName, textElements)
    return treeItemLabel
  
  #----------------------------------------------------------------------

  # THIS IS NOT WORKING FOR SOME REASON
  #~ def each_item(self, startNode):
    #~ '''Recursively traverses a tree and yields 
      #~ each wx.TreeItemId at and below startNode.'''
    #~ if startNode:
      #~ yield startNode
      #~ print "yielding an item"  #  debug
      #if self.GetChildrenCount(startNode, False):
      #~ numItems = self.GetChildrenCount(startNode, False)
      #~ print "\nNumber of kids:", numItems # debug
      #~ if numItems:
        #~ cookie = -1
        #~ child, cookie = self.GetFirstChild(startNode, cookie)
        #~ while child:
          #~ self.each_item(child)
          #~ child, cookie = self.GetNextChild(startNode, cookie)
    #~ else:
      #~ print "Encountered bad tree item"  # debug
  
  #----------------------------------------------------------------------

  #~ def clearAllLabels_notworking(self):
    #~ counter = 1
    #~ for item in self.each_item(self.societyNode):
      #~ print "clearing label from item number", counter
      #~ label = self.GetItemText(item)
      #~ label.removeAllTextElements()
      #~ counter += 1
      
  def clearAllLabels(self, startNode):
    '''Recursively traverses a tree and remove text elements  
      from each TreeItemLabel at and below startNode.'''
    counter = 1
    if startNode:
      self.GetItemText(startNode).removeAllTextElements()
      counter += 1
      if self.GetChildrenCount(startNode, False):
        cookie = -1
        child, cookie = self.GetFirstChild(startNode, cookie)
        while child:
          self.clearAllLabels(child)
          child, cookie = self.GetNextChild(startNode, cookie)

# ***************************************************************************
# ***************************************************************************

class TreeItemLabel:

  # This class represents the text label associated with a wx.TreeCtrl item.  It consists of a
  # String item name and zero or more text elements.  These text elements are extra info 
  # about the item.  In the CSMARTer context, the elements represent facets.  When
  # displayed, each element (other than the item name) is surrounded by parentheses.
  # Elements can be one or more facets and may be in 'attrib=value' format or may be
  # just a value.
  # textElements is a Dictionary: key = facet type, value = a List of values for that facet type
  
  def __init__(self, itemName, textElementDict={}):
    self.itemName = itemName
    self.textElements = textElementDict
  
  def __str__(self):
    return self.getAllText()
  
  def getItemName(self):
    return self.itemName
  
  def setItemName(self, aName):
    self.itemName = aName
  
  def getTextElement(self, facetType):
    return self.textElements[facetType]
  
  def addTextElement(self, facetType, facetValue):
    existingLabelFacets = []
    if self.textElements.has_key(facetType):
      existingLabelFacets = self.textElements[facetType]
      existingLabelFacets.extend(facetValue)
    else:
      self.textElements[facetType] = facetValue
  
  def removeTextElement(self, facetType):
    if self.textElements.has_key(facetType):
      del self.textElements[facetType]
  
  def removeAllTextElements(self):
    self.textElements.clear()
  
  def getAllText(self):
    return self.itemName + self.getTextElements()

  def getTextElements(self):
    elementString = ''
    elementLists = self.textElements.values()  # elementLists is a List of Lists
    for elements in elementLists:
      elementString = elementString + ' ('
      separator = ''
      counter = 0
      for element in elements:
        if counter > 0:
          separator = ' / '
        elementString = elementString + separator + element
        counter += 1
      elementString = elementString + ') '
    return elementString
  
  def numTextElements(self):
    return len(self.textElements)
  
  def hasTextElements(self):
    return len(self.textElements) > 0
  
  def find(self, stringToFind):
    return self.getAllText().find(stringToFind)


def runTest(frame, nb, log ): runApp(frame, nb, log)


def runApp( frame, nb, log ):
    win = SocietyEditorPanel( frame, nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
<H2>The CSMARTer Society Viewer ...</H2>
<P>
To use, read in a society file. Then read in rules files and apply them as needed. Finally, write the society back out 
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])

