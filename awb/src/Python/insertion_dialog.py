#!/bin/env python
#----------------------------------------------------------------------------
# Name:         insertion_dialog.py
# Purpose:      dialogs for insertion
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: insertion_dialog.py,v 1.6 2004-12-06 22:22:46 damoore Exp $
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
from CSModel.parameter import VMParameter
from CSModel.host import Host
from CSModel.node import Node
from CSModel.agent import Agent
from CSModel.facet import Facet
from CSModel.component import Component
from CSModel.argument import Argument
from CSModel.parameter import *
import wx


#---------------------------------------------------------------------------

class NewEntityDialog (wx.TextEntryDialog):

  def __init__(self, parent, label):
    wx.TextEntryDialog.__init__(self, parent, label, 'Add New Entity')
    self.SetSize((175, -1))
    if self.ShowModal() == wx.ID_OK:
      parent.newEntityName = self.GetValue()
    self.Destroy()

#---------------------------------------------------------------------------

class NewNodeDialog:

  def __init__(self, parent):
    self.win = wx.Dialog(parent, -1, "New Node", size=wx.Size(400, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
    ###---------------------------------------------------
    self.parent = parent
    sizer = wx.BoxSizer(wx.VERTICAL)
    
    label = wx.StaticText(self.win, -1, "New Node")
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    # text boxes
    # Name
    nameBox = wx.BoxSizer(wx.HORIZONTAL)
    nameLabel = wx.StaticText(self.win, -1, "Name:")
    nameBox.Add(nameLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    tID = wx.NewId()
    self.nodeName = wx.TextCtrl(self.win, tID, "", size=(200,-1))
    nameBox.Add(self.nodeName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    sizer.AddSizer(nameBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    
    # Class
    classBox = wx.BoxSizer(wx.HORIZONTAL)
    
    classLabel = wx.StaticText(self.win, -1, "Class:")
    classBox.Add(classLabel, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    nodeClass = wx.TextCtrl(self.win, -1, "org.cougaar.bootstrap.Bootstrapper", size=(200,-1))
    classBox.Add(nodeClass, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    sizer.AddSizer(classBox, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    
    # parameters
    self.progPanel = AddParameterPanel(self.win, 'prog', True)
    sizer.Add(self.progPanel, 1, wx.GROW)
    self.envPanel = AddParameterPanel(self.win, 'env', True)
    sizer.Add(self.envPanel, 1, wx.GROW)
    self.envPanel.Show()
    self.vmPanel = AddParameterPanel(self.win, 'vm', True)
    self.vmPanel.params.SetInsertionPoint(0)  # insert next item at top of the list
    self.vmPanel.params.WriteText("-Dorg.cougaar.node.name=" + \
                                                  "(system will complete)")
    self.vmPanel.params.SetInsertionPointEnd()  # now go back to the end
    self.vmPanel.params.WriteText("\n-Dorg.cougaar.name.server=" + \
                                                  self.parent.parent.frame.society.get_nameserver())
    sizer.Add(self.vmPanel, 1, wx.GROW)
    self.vmPanel.Show()
    
    line = wx.StaticLine(self.win, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
    
    # buttons
    box = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)
    
    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)
    self.win.CenterOnParent()
    
    val = self.win.ShowModal()
    if val == wx.ID_OK:
      parent.newEntityName = self.nodeName.GetValue()
      parent.newNodeClass = nodeClass.GetValue()
      parent.newProgParams = self.progPanel.params.GetValue()
      parent.newEnvParams = self.envPanel.params.GetValue()
      parent.newVmParams = self.vmPanel.params.GetValue()
    self.win.Destroy()
  
  #Adds a default vm_param for the name of the node being created
  def OnNodeNameEntry(self, event):
    newNodeName = self.nodeName.GetValue()
    self.vmPanel.params.WriteText("-Dorg.cougaar.node.name=" + newNodeName + "\n")
    host = self.parent.getEntityObj()

#---------------------------------------------------------------------------

class NewAgentDialog:
  def __init__(self, parent):
    self.win = wx.Dialog(parent, -1, "New Agent", size=wx.Size(350, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

    sizer = wx.BoxSizer(wx.VERTICAL)

    label = wx.StaticText(self.win, -1, "New Agent")
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self.win, -1, "Name:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    # Agent name text box
    agentName = wx.TextCtrl(self.win, -1, "", size=(200,-1))
    box.Add(agentName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self.win, -1, "Class:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    # Agent class text box
    agentClass = wx.TextCtrl(self.win, -1, "org.cougaar.core.agent.SimpleAgent", size=(200,-1))
    box.Add(agentClass, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    line = wx.StaticLine(self.win, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

    # OK and CANCEL buttons
    box = wx.BoxSizer(wx.HORIZONTAL)

    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wx.ID_OK:
        parent.newEntityName = agentName.GetValue()
        parent.newAgentClass = agentClass.GetValue()
    self.win.Destroy()

#---------------------------------------------------------------------------

class NewComponentDialog:
  def __init__(self, parent):
    self.win = wx.Dialog(parent, -1, "New Component", size=wx.Size(350, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
###---------------------------------------------------

    sizer = wx.BoxSizer(wx.VERTICAL)

    label = wx.StaticText(self.win, -1, "New Component")
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)


# text boxes
# Name
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self.win, -1, "Name:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    componentName = wx.TextCtrl(self.win, -1, "", size=(80,-1))
    box.Add(componentName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

# Class
    box = wx.BoxSizer(wx.HORIZONTAL)

    label = wx.StaticText(self.win, -1, "Class:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    componentClass = wx.TextCtrl(self.win, -1, "", size=(150,-1))
    box.Add(componentClass, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    line = wx.StaticLine(self.win, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

# Priority
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self.win, -1, "Priority:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    prioValues = ["HIGH", "INTERNAL", "BINDER", "COMPONENT", "LOW"]
    defaultPrio = "COMPONENT"
    componentPriority = wx.ComboBox(self.win, -1, defaultPrio, wx.DefaultPosition, wx.Size(100, -1),
                    prioValues, wx.CB_DROPDOWN | wx.CB_READONLY)
    box.Add(componentPriority, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
  
# Order
    label = wx.StaticText(self.win, -1, "Order:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    componentOrder = wx.TextCtrl(self.win, -1, "", size=wx.Size(50, -1))
    #~ box.Add(orderSpinner, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    box.Add(componentOrder, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
    
    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
  
# InsertionPoint
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self.win, -1, "Insertion Point:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    componentInsertionPoint = wx.TextCtrl(self.win, -1, "Node.AgentManager.Agent.PluginManager.Plugin", 
                                                        size=(250,-1))
    box.Add(componentInsertionPoint, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
### ------------------------------------
    box = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wx.ID_OK:
      parent.newComponentName = componentName.GetValue()
      parent.newComponentClass = componentClass.GetValue()
      parent.newComponentPriority = componentPriority.GetValue()
      parent.newComponentInsertionPoint = componentInsertionPoint.GetValue()
      parent.newComponentOrder = componentOrder.GetValue()
    self.win.Destroy()

#---------------------------------------------------------------------------

class AddMultipleValuesDialog:

  def __init__(self, parent, node=None, type=None):
    self.node = node
    self.valueType = type  # will be either 'vm', 'prog', 'env', 'facet', or None
    self.parent = parent
    self.displayedPanels = []  # holds a ref to each panel displayed
    title = ""
    labelText = ""
    if self.valueType == 'prog' or self.valueType == 'env' or self.valueType == 'vm':
      title = "Add Parameters"
      labelText = "Enter new node parameters"
    elif self.valueType == 'facet':
      title = "Add Facets"
      labelText = "Enter new facets in 'key=value' format"
    self.win = wx.Dialog(parent, -1, title, size=wx.Size(350, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
    
###---------------------------------------------------

    sizer = wx.BoxSizer(wx.VERTICAL)

    label = wx.StaticText(self.win, -1, labelText)
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

# parameters
    if self.valueType is None:  # allow entry of all three types of parameter
      self.progPanel = AddParameterPanel(self.win, 'prog')
      sizer.Add(self.progPanel, 1, wx.GROW)
      self.displayedPanels.append(self.progPanel)
      self.envPanel = AddParameterPanel(self.win, 'env')
      sizer.Add(self.envPanel, 1, wx.GROW)
      self.displayedPanels.append(self.envPanel)
      self.envPanel.Show()
      self.vmPanel = AddParameterPanel(self.win, 'vm')
      sizer.Add(self.vmPanel, 1, wx.GROW)
      self.displayedPanels.append(self.vmPanel)
      self.vmPanel.Show()
    else:  # only allow entry of one type of parameter
      self.panel = AddParameterPanel(self.win, self.valueType)
      sizer.Add(self.panel, 1, wx.GROW)
      self.displayedPanels.append(self.panel)
    
    line = wx.StaticLine(self.win, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

# buttons
    box = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)
    self.win.CenterOnParent()

    val = self.win.ShowModal()
    if val == wx.ID_OK:
      self.addNewParams()
    self.win.Destroy()

  def addNewParams(self):
    self.paramsList = [] # will hold a list of objects to be added
    for paramPanel in self.displayedPanels:
      paramValues = (str(paramPanel.params.GetValue()))
      dataPresent = False
      if paramValues is not None and paramValues != "":
        dataPresent = True
        newParams = paramValues.split("\n")  # a list of strings
        for param in newParams:
          if len(param) > 0:
            if paramPanel.paramType == 'vm':
              self.paramsList.append(VMParameter(param))
            elif paramPanel.paramType == 'prog':
              self.paramsList.append(ProgParameter(param))
            elif paramPanel.paramType == 'env':
              self.paramsList.append(EnvParameter(param))
            elif paramPanel.paramType == 'facet':
              print "Index of =:", str(param.find("=")) 
              if param.find("=") > 0:
                self.paramsList.append(Facet(param))
              else:
                msg = '''A facet must be in "key=value" format.  Please reenter.'''
                errorDialog = wx.MessageDialog(self.parent, msg, style = wx.CAPTION | wx.OK | 
                     wx.THICK_FRAME | wx.ICON_ERROR)
                errorDialog.ShowModal()
                return
    
    if dataPresent:
      # if we're in the NodeInfoEditor, update the tree
      if isinstance(self.parent, NodeInfoEditor):
        parentItem = self.parent.currentItem # the item user right-clicked
        parentData = self.parent.tree.GetPyData(parentItem)
        if parentData is not None: # if the right click was on a Param or Facet item:
          # set parent to the appropriate Parameter or Facet heading item
          parentItem = self.parent.tree.GetItemParent(parentItem)
        for newParam in self.paramsList:
          paramData = [newParam, "value"]  # the PyData
          if isinstance(newParam, Facet):
            for facetPair in newParam.each_facet_pair():
              newItem = self.parent.tree.AppendItem(parentItem, facetPair)
          else:   # it's a Parameter instance
            newItem = self.parent.tree.AppendItem(parentItem, newParam.value)
          self.parent.tree.SetPyData(newItem, paramData)
        # finally, add new params or facets to the society model
        change = [NodeInfoEditor.ADD, self.node, self.paramsList] # package the change elements in a list
        self.parent.changesToMake.append(change) # store the changes til user clicks "OK"
      else:   # we're on the main society tree, so just make the change
        self.node = self.parent.entityObj # the node to which params are being added
        for each_param in self.paramsList:
          self.node.add_parameter(each_param)
    else:
      print "No new parameters entered"

#---------------------------------------------------------------------------
class AddParameterPanel(wx.Panel):

  def __init__(self, parent, paramType, nodeCreation=False):
    wx.Panel.__init__(self, parent, -1)
    self.parent = parent
    self.paramType = paramType
    self.nodeCreation = nodeCreation
    self.defaultParam = ""
    
    if nodeCreation is True and self.paramType == "prog":
      self.defaultParam = "org.cougaar.core.node.Node"
    elif nodeCreation is True and self.paramType == "vm":
      self.defaultParam = '''
-Dorg.cougaar.core.agent.startTime=08/10/2005
-Dorg.cougaar.core.persistence.clear=True
-Dorg.cougaar.core.persistence.enable=False
-Dorg.cougaar.planning.ldm.lps.ComplainingLP.level=0
-Duser.timezone=GMT'''
    box = wx.BoxSizer(wx.VERTICAL)
    
    labelText = ""
    if self.paramType == "facet":
      labelText = "Facets:"
    else:
      labelText = self.paramType + "_parameters:"
    progLabel = wx.StaticText(self, -1, labelText)
    box.Add(progLabel, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
    self.params = wx.TextCtrl(self, -1, self.defaultParam, size=(300,130),
                                        style=wx.TE_MULTILINE | wx.HSCROLL)
    self.params.SetInsertionPointEnd()
    box.Add(self.params, 1, wx.GROW | wx.ALIGN_CENTRE | wx.ALL, 5)

    self.SetSizer(box)
    self.SetAutoLayout(True)
    box.Fit(self)

#**************************************************************

class CougaarMessageDialog:
  def __init__(self, parent, topic, msg=None):
    self.win = None
    if topic is None or len(topic) == 0:
      dialogFormat = 0
    elif topic == "open society":
      dialogFormat = 0
      if msg is None:
        msg = '''A society is already open.  Please close it before opening another.'''
    elif topic == "confirm":
      if msg is None:
        msg = '''Save society before closing?'''
      dialogFormat = 1
    elif topic == "delete":
      if msg is None:
        msg = '''Are you sure you want to delete the society?\n\n
Doing so will permanently delete the society file from the disk.'''
      dialogFormat = 2
    elif topic == "info":
      dialogFormat = 3
    elif topic == "error":
      dialogFormat = 4
      
    if dialogFormat == 0:
      self.win = wx.MessageDialog(parent, msg, style = wx.CAPTION | wx.OK | 
                     wx.THICK_FRAME | wx.ICON_EXCLAMATION)
    elif dialogFormat == 1:
      self.win = wx.MessageDialog(parent, msg, style = wx.CAPTION | wx.YES_NO | 
                     wx.YES_DEFAULT | wx.CANCEL | wx.THICK_FRAME | wx.ICON_QUESTION)
    elif dialogFormat == 2:
      self.win = wx.MessageDialog(parent, msg, style = wx.CAPTION | wx.YES_NO | 
                     wx.NO_DEFAULT | wx.THICK_FRAME | wx.ICON_QUESTION)
    if dialogFormat == 3:
      self.win = wx.MessageDialog(parent, msg, style = wx.CAPTION | wx.OK | 
                     wx.THICK_FRAME | wx.ICON_INFORMATION)
    if dialogFormat == 4:
      self.win = wx.MessageDialog(parent, msg, style = wx.CAPTION | wx.OK | 
                     wx.THICK_FRAME | wx.ICON_ERROR)
  
  def display(self):
    self.win.ShowModal()
    self.win.Destroy()
  
  def getUserInput(self):
    val = self.win.ShowModal()
    self.win.Destroy()
    return val

#**************************************************************

class FindItemDialog:
  def __init__(self, parent, showViewerRadio=False):
    self.win = wx.Dialog(parent, -1, "Find society entity", size=wx.Size(350, 200),
                   style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
    
    self.parent = parent
    sizer = wx.BoxSizer(wx.VERTICAL)
    
    label = wx.StaticText(self.win, -1, "Enter name of society entity to find:")
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    # Item name text box
    self.itemName = wx.TextCtrl(self.win, -1, self.parent.searchLabel, size=(200,-1))
    self.itemName.SetSelection(-1, -1)
    sizer.Add(self.itemName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
       
    # Case-sensitive search desired checkbox
    self.caseSearchDesired = False
    caseSearchID = wx.NewId()
    self.caseSearchCheckbox = wx.CheckBox(self.win, caseSearchID, "Perform Case-Sensitive Search")
    self.caseSearchCheckbox.SetValue(self.parent.caseSearchDesired)
    self.Bind(wx.EVT_CHECKBOX,   self.OnCaseSearchChecked, self.caseSearchCheckbox)
    sizer.Add(self.caseSearchCheckbox, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, border=7)
    
    # Viewer in which to search radio box
    rbID = wx.NewId()
    rbLabel = "Search for desired item in:"
    buttonTitles = ["Agent List", "HNA Map                      "]
    self.rb = wx.RadioBox(self.win, rbID, rbLabel, wx.DefaultPosition, (-1, 80), buttonTitles, 1, wx.RA_SPECIFY_COLS)
    self.rb.SetSelection(1)  # HNA Map is default selection
    if not showViewerRadio:
      self.rb.Enable(False)
      self.viewerToSearch = self.parent.societyViewer
    else:
      self.viewerToSearch = self.parent.laydownViewer
    self.Bind(wx.EVT_RADIOBOX, self.OnEvtRadioBox, self.rb)  
    sizer.Add(self.rb, 0, wx.ALIGN_CENTER | wx.ALL, 10)
    
    line = wx.StaticLine(self.win, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
    sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER | wx.TOP, 5)

    # OK and CANCEL buttons
    box = wx.BoxSizer(wx.HORIZONTAL)

    btn = wx.Button(self.win, wx.ID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
    box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.AddSizer(box, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(True)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wx.ID_OK:
      self.parent.searchLabel = self.itemName.GetValue()
      self.parent.caseSearchDesired = self.caseSearchDesired
      self.parent.currentTree = self.viewerToSearch
    self.win.Destroy()
  
  def OnCaseSearchChecked(self, event):
    if self.caseSearchCheckbox.IsChecked():
      self.caseSearchDesired = True
    else:
      self.caseSearchDesired = False
  
  def OnEvtRadioBox(self, event):
    if self.rb.GetSelection() == 0:  # Agent List
      self.viewerToSearch = self.parent.agentViewer
    else:  # HNA Map
      self.viewerToSearch = self.parent.laydownViewer

#**************************************************************

class NodeInfoEditor(wx.Frame):

  EDIT = 0
  DELETE = 1
  ADD = 2

  def __init__(self, parent, log, ID = -1, title = 'Edit Node Info', 
                    pos=wx.DefaultPosition, size=(450,450), 
                    style=wx.DEFAULT_FRAME_STYLE):
    wx.Frame.__init__(self, parent, ID, title, pos, size, style)
    self.parent = parent
    self.log = log
    self.changesToMake = []
    tID = wx.NewId()
    self.log.WriteText("new NodeInfoEditor\n")
    self.tree = wx.TreeCtrl(self, tID, wx.DefaultPosition, (450,450),
                           wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS)
    
    #------------------------------------------------------------------------------------------------
    #   Build the tree
    
    self.entityObj = self.parent.getEntityObj()
    
    if isinstance(self.entityObj, Host):
      self.root = self.tree.AddRoot("HOST: " + self.entityObj.name)
      facetTitleNode = self.tree.AppendItem(self.root, "Facets")
      for facet in self.entityObj.each_facet():
        for facetString in facet.each_facet_pair():
          hostFacetNode = self.tree.AppendItem(facetTitleNode, facetString)
          data = [facet, "value"]
          self.tree.SetPyData(hostFacetNode, data)
          
    elif isinstance(self.entityObj, Node):
      self.root = self.tree.AddRoot("NODE: " + self.entityObj.name)
      classTitleNode = self.tree.AppendItem(self.root, "Class")
      classNode = self.tree.AppendItem(classTitleNode, str(self.entityObj.klass))
      data = [self.entityObj, "klass"]
      self.tree.SetPyData(classNode, data)
      facetTitleNode = self.tree.AppendItem(self.root, "Facets")
      for facet in self.entityObj.each_facet():
        for facetString in facet.each_facet_pair():
          nodeFacetNode = self.tree.AppendItem(facetTitleNode, facetString)
          data = [facet, "value"]
          self.tree.SetPyData(nodeFacetNode, data)
      envParamTitleNode = self.tree.AppendItem(self.root, "Env_Parameters")
      for each_param in self.entityObj.env_parameters:
        envParamNode = self.tree.AppendItem(envParamTitleNode, each_param.value)
        data = [each_param, "value"]
        self.tree.SetPyData(envParamNode, data)
      progParamTitleNode = self.tree.AppendItem(self.root, "Prog_Parameters")
      for each_param in self.entityObj.prog_parameters:
        progParamNode = self.tree.AppendItem(progParamTitleNode, each_param.value)
        data = [each_param, "value"]
        self.tree.SetPyData(progParamNode, data)
      vmParamTitleNode = self.tree.AppendItem(self.root, "VM_Parameters")
      for each_param in self.entityObj.vm_parameters:
        vmParamNode = self.tree.AppendItem(vmParamTitleNode, each_param.value)
        data = [each_param, "value"]
        self.tree.SetPyData(vmParamNode, data)
      
    elif isinstance(self.entityObj, Agent):
      self.root = self.tree.AddRoot("AGENT: " + self.entityObj.name)
      classTitleNode = self.tree.AppendItem(self.root, "Class")
      classNode = self.tree.AppendItem(classTitleNode, str(self.entityObj.klass))
      data = [self.entityObj, "klass"]
      self.tree.SetPyData(classNode, data)
      facetTitleNode = self.tree.AppendItem(self.root, "Facets")
      for facet in self.entityObj.each_facet():
        for facetString in facet.each_facet_pair():
          agentFacetNode = self.tree.AppendItem(facetTitleNode, facetString)
          data = [facet, "value"]
          self.tree.SetPyData(agentFacetNode, data)
      
    elif isinstance(self.entityObj, Component):
      self.root = self.tree.AddRoot("COMPONENT: " + self.entityObj.name)
      compKlassTitleNode = self.tree.AppendItem(self.root, "Class")
      compKlassNode = self.tree.AppendItem(compKlassTitleNode, str(self.entityObj.klass))
      data = [self.entityObj, "klass"]
      self.tree.SetPyData(compKlassNode, data)
      compPriTitleNode = self.tree.AppendItem(self.root, "Priority")
      compPriNode = self.tree.AppendItem(compPriTitleNode, str(self.entityObj.priority))
      data = [self.entityObj, "priority"]
      self.tree.SetPyData(compPriNode, data)
      insertPtTitleNode = self.tree.AppendItem(self.root, "Insertion Point")
      insertPtNode = self.tree.AppendItem(insertPtTitleNode, str(self.entityObj.insertionpoint))
      data = [self.entityObj, "insertionpoint"]
      self.tree.SetPyData(insertPtNode, data)
      compOrderTitleNode = self.tree.AppendItem(self.root, "Order")
      compOrderNode = self.tree.AppendItem(compOrderTitleNode, str(self.entityObj.order))
      data = [self.entityObj, "order"]
      self.tree.SetPyData(compOrderNode, data)
      
    cookie = 1     # required by wx.TreeCtrl for getting children.  See docs.
    self.ExpandTree(self.root, cookie)
    self.log.WriteText("new NodeInfoEditor here\n")
    self.tree.SelectItem(self.root)
    
    self.Bind(wx.EVT_TREE_SEL_CHANGED,   self.OnSelChanged, self.tree)
    self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,   self.OnBeginEdit, self.tree)
    self.Bind(wx.EVT_TREE_END_LABEL_EDIT,   self.OnEndEdit, self.tree)
    self.Bind(wx.EVT_TREE_DELETE_ITEM,   self.OnDelete, self.tree)
    self.tree.Bind(wx.EVT_RIGHT_DOWN,   self.OnRightClick)
    self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
    
###---------------------------------------------------

    sizer = wx.BoxSizer(wx.VERTICAL)
    
    btnBox = wx.BoxSizer(wx.HORIZONTAL)
    btn = wx.Button(self, wx.ID_OK, "  OK  ")
    self.Bind(wx.EVT_BUTTON, self.OnOK, btn)
    btn.SetDefault()
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    btn = wx.Button(self, wx.ID_CANCEL, " Cancel ")
    self.Bind(wx.EVT_BUTTON, self.OnCancel, btn)
    self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
    btnBox.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

    sizer.Add(self.tree, 1, wx.EXPAND | wx.ALIGN_CENTER)
    sizer.Add(btnBox, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    self.SetSizer(sizer)
    self.SetAutoLayout(True)
    self.CenterOnParent()
    self.log.WriteText("new NodeInfoEditor: init done\n")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Event Handlers

  def OnSelChanged(self, event):
    self.currentItem = event.GetItem()
    self.itemDataList = self.tree.GetPyData(self.currentItem)
    self.log.WriteText("%s\n" % self.tree.GetItemText(self.currentItem))
    event.Skip()
    
  def OnBeginEdit(self, event):
    self.itemDataList = self.tree.GetPyData(event.GetItem())
    if self.itemDataList is None:
      self.log.WriteText("You can't edit this one...\n")
      event.Veto()
    
  def OnEndEdit(self, event):
    oldLabel = self.tree.GetItemText(self.currentItem) # still has the old label
    newLabel = event.GetLabel()
    if newLabel:  # if the label was actually changed:
      self.log.WriteText("Old label: " + oldLabel + "  New label: " + newLabel)
      self.changeLabel(newLabel)
  
  def changeLabel(self, newLabel):
    entityObj = self.itemDataList[0]
    attribute = self.itemDataList[1]
    change = [NodeInfoEditor.EDIT, entityObj, attribute, newLabel] # package the change elements in a list
    self.changesToMake.append(change) # store the changes til user clicks "OK"
    
  def OnRightClick(self, event):
    self.x = event.GetX()
    self.y = event.GetY()
  
  def OnRightUp(self, event):
    pt = event.GetPosition();
    item, flags = self.tree.HitTest(pt)
    self.currentItem = item
    self.itemDataList = self.tree.GetPyData(item)
    menu = self.SetMenu(self.itemDataList)  # arg is a ref to the obj underlying the tree item
    if menu is not None:
      self.PopupMenu(menu, wx.Point(self.x, self.y))
      menu.Destroy()
    event.Skip()

  def OnOK(self, event):
    # Make all the changes to the underlying society obj
    #format of 'change' list is:
    #change[0]: EDIT, DELETE, or ADD
    #change[1]: the underlying obj associated w/ the current item, or,
    #                  if ADD, the parent of the obj to be added
    #change[2]: name of the attribute involved (for EDIT), or,
    #                   for ADD, the obj to be added, or, for DELETE on a Facet,
    #                   the key for the key/value pair to be deleted
    #change[3]: new value for the attribute (for EDIT only)
    for change in self.changesToMake:
      if change[0] == NodeInfoEditor.EDIT:
        change[1].set_attribute(change[2], change[3])
      elif change[0] == NodeInfoEditor.DELETE:
        if isinstance(change[1], Facet):
          change[1].delete_entity(change[2])
        else:
          change[1].delete_entity()
      else:
        change[1].add_entity(change[2])
    self.changesToMake = []  # empty it out
    self.Close(True)
    self.parent.infoFrameOpen = 0
    
  def OnCancel(self, event):
    self.changesToMake = []  # empty it out
    self.Close(True)
    self.parent.infoFrameOpen = 0
    
  def OnCloseWindow(self, event):
    self.Destroy()
 
  def OnRename(self, event):
    if isinstance(self.itemDataList[0], Component) and self.itemDataList[1] == "priority":
      dlg = wx.Dialog(self.tree, -1, "Edit Component Priority", 
                     style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)
      sizer = wx.BoxSizer(wx.VERTICAL)
      label = wx.StaticText(dlg, -1, "Select new Priority")
      sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
      prioValues = ["HIGH", "INTERNAL", "BINDER", "COMPONENT", "LOW"]
      defaultPrio = self.itemDataList[0].priority
      componentPriority = wx.ComboBox(dlg, -1, defaultPrio, wx.DefaultPosition, wx.Size(100, -1),
                      prioValues, wx.CB_DROPDOWN | wx.CB_READONLY)
      sizer.Add(componentPriority, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
      box = wx.BoxSizer(wx.HORIZONTAL)
      btn = wx.Button(dlg, wx.ID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
      
      btn = wx.Button(dlg, wx.ID_CANCEL, " Cancel ")
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
      
      sizer.AddSizer(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
      
      dlg.SetSizer(sizer)
      dlg.SetAutoLayout(True)
      sizer.Fit(dlg)
      val = dlg.ShowModal()
      if val == wx.ID_OK:
        newLabel = componentPriority.GetStringSelection()
        print "New Prio value:", newLabel  # prg debug
        self.tree.SetItemText(self.currentItem, newLabel)
        self.changeLabel(newLabel)
    else:
      self.tree.EditLabel(self.currentItem)
  
  def OnDeleteItem(self, event):
    entityObj = self.itemDataList[0]
    # package the change elements in a list:
    if isinstance(entityObj, Facet):
      facet = self.tree.GetItemText(self.currentItem)
      facetList = facet.split("=")
      change = [NodeInfoEditor.DELETE, entityObj, facetList[0]] 
    else:
      change = [NodeInfoEditor.DELETE, entityObj] 
    self.changesToMake.append(change) # store the changes til user clicks "OK"
    self.tree.Delete(self.currentItem)

  def OnDelete(self, event):
    self.log.WriteText("Deleted %s\n" % self.tree.GetItemText(self.currentItem))
  
  def OnAddComponent(self, event):
    self.newComponentName = None
    self.newComponentClass = None
    self.newComponentPriority = None
    self.newComponentInsertionPoint = None
    self.newComponentOrder = None
    NewComponentDialog(self)
    if self.newComponentName is not None:
      self.addComponent()
  
  def OnAddArgument(self, event):
    self.newArgumentName = None
    NewArgumentDialog(self)
    if self.newArgumentName is not None:
      self.addArgument()

  def OnAddVmParameter(self, event):
    #Bring up a dialog box to collect/add vm_parameters
    AddMultipleValuesDialog(self, node=self.entityObj, type='vm')
  
  def OnAddProgParameter(self, event):
    #Bring up a dialog box to collect/add prog_parameters
    AddMultipleValuesDialog(self, node=self.entityObj, type='prog')
  
  def OnAddEnvParameter(self, event):
    #Bring up a dialog box to collect/add env_parameters
    AddMultipleValuesDialog(self, node=self.entityObj, type='env')
  
  def OnAddFacet(self, event):
    #Bring up a dialog box to collect/add facets
    AddMultipleValuesDialog(self, node=self.entityObj, type='facet')
  
  def addComponent(self):
    name =str(self.newComponentName)
    klass = str(self.newComponentClass)
    priority = str(self.newComponentPriority)
    insertPt = str(self.newComponentInsertionPoint)
    order = str(self.newComponentOrder)
    newComp = Component(name, klass, priority, insertPt, order, "Hand edit")
    parent = self.currentItem
    itemData = self.tree.GetPyData(parent)
    if itemData is not None:
      parent = self.tree.GetItemParent(parent)
    newItem = self.tree.AppendItem(parent, newComp.name)
    data = [newComp, "name"]
    self.tree.SetPyData(newItem, data)
    compClassTitle = self.tree.AppendItem(newItem, "Class")
    compClass = self.tree.AppendItem(compClassTitle, newComp.klass)
    data = [newComp, "klass"]
    self.tree.SetPyData(compClass, data)
    compPriTitle = self.tree.AppendItem(newItem, "Priority")
    compPri = self.tree.AppendItem(compPriTitle, newComp.priority)
    data = [newComp, "priority"]
    self.tree.SetPyData(compPri, data)
    compInsertTitle = self.tree.AppendItem(newItem, "Insertion Point")
    compInsert = self.tree.AppendItem(compInsertTitle, newComp.insertionpoint)
    data = [newComp, "insertionpoint"]
    self.tree.SetPyData(compInsert, data)
    #~ self.tree.EnsureVisible(compInsert)
    compOrderTitle = self.tree.AppendItem(newItem, "Order")
    compOrder = self.tree.AppendItem(compOrderTitle, newComp.order)
    data = [newComp, "order"]
    self.tree.SetPyData(compOrder, data)
    self.tree.EnsureVisible(compOrder)
    change = [NodeInfoEditor.ADD, parent, newComp] 
    self.changesToMake.append(change) # store the changes til user clicks "OK"

  def addArgument(self):
    if len(str(self.newArgumentName)) > 0:
      parent = None
      newArg = Argument(str(self.newArgumentName), "Hand edit")
      # Update the tree
      selectedItemText = self.tree.GetItemText(self.currentItem)
      if selectedItemText == "Arguments":
        parent = self.tree.GetPyData(self.tree.GetItemParent(self.currentItem))[0]
        newArgItem = self.tree.AppendItem(self.currentItem, newArg.name)
      else:  # selected item is a component name
        parent = self.tree.GetPyData(self.currentItem)[0]
        # see if there's already an "Arguments" header; if not, add one
        child, cookie = self.tree.GetFirstChild(self.currentItem, 1)
        if self.tree.GetItemText(child) == "Arguments":
          newArgItem = self.tree.AppendItem(child, newArg.name)
        else:
          while child.IsOk():
            child, cookie = self.tree.GetNextChild(child, cookie)
            if self.tree.GetItemText(child) == "Arguments":
              newArgItem = self.tree.AppendItem(child, newArg.name)
              break
          else:  # "Arguments" heading not found, so add it
            argTitleNode = self.tree.AppendItem(self.currentItem, "Arguments")
            newArgItem = self.tree.AppendItem(argTitleNode, newArg.name)
      data = [newArg, "value"]
      self.tree.SetPyData(newArgItem, data)
      self.tree.EnsureVisible(newArgItem)
      change = [NodeInfoEditor.ADD, parent, newArg] 
      self.changesToMake.append(change) # store the changes til user clicks "OK"

  
#**************************************************************************
#  Helper Methods
#**************************************************************************

  # Recursively iterates over all the tree nodes and expands them.
  def ExpandTree(self, treeNode, cookie):
    self.log.WriteText("ExpandTree\n")
    if treeNode.IsOk(): 
      self.tree.Expand(treeNode) 
      (child, cookie) = self.tree.GetFirstChild(treeNode)
#      print 'child:', child
#      while child[0].IsOk():
      while child.IsOk():
#        self.ExpandTree(child[0], child[1])
        self.ExpandTree(child, cookie)
        self.log.WriteText("ExpandTree here\n")
#        child = self.tree.GetNextChild(child[0], child[1])
        (child, cookie) = self.tree.GetNextChild(child, cookie)
    self.log.WriteText("ExpandTree done\n")
  def SetMenu(self, itemDataList):
  
    tID1 = 0
    tID2 = 1
    tID3 = 2
    tID4 = 3
    tID5 = 4
    tID6 = 5
    tID7 = 6
    tID8 = 7
    
    menu = wx.Menu()
    editMenuItem = wx.MenuItem(menu, tID1, "Edit")
    deleteMenuItem = wx.MenuItem(menu, tID2, "Delete")
    addVmParamMenuItem = wx.MenuItem(menu, tID3, "Add vm_parameter")
    addProgParamMenuItem = wx.MenuItem(menu, tID6, "Add prog_parameter")
    addEnvParamMenuItem = wx.MenuItem(menu, tID7, "Add env_parameter")
    addCompMenuItem = wx.MenuItem(menu, tID4, "Add Component")
    addArgMenuItem = wx.MenuItem(menu, tID5, "Add Argument")
    addFacetMenuItem = wx.MenuItem(menu, tID8, "Add Facet")
    
    if self.tree.GetItemText(self.currentItem) == "VM_Parameters":
      menu.AppendItem(addVmParamMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddVmParameter, addVmParamMenuItem)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Prog_Parameters":
      menu.AppendItem(addProgParamMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddProgParameter, addProgParamMenuItem)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Env_Parameters":
      menu.AppendItem(addEnvParamMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddEnvParameter, addEnvParamMenuItem)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Components":
      menu.AppendItem(addCompMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddComponentr, addCompMenuItem)
      return menu

    if self.tree.GetItemText(self.currentItem) == "Arguments":
      menu.AppendItem(addArgMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddArgument, addArgMenuItem)
      return menu

    if self.tree.GetItemText(self.currentItem) == "Facets":
      menu.AppendItem(addFacetMenuItem)
      self.Bind(wx.EVT_MENU, self.OnAddFacet, addFacetMenuItem)
      return menu

    if itemDataList is not None:
      if isinstance(itemDataList[0], VMParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addVmParamMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDeleteItem, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddVmParameter, addVmParamMenuItem)
        return menu
      
      if isinstance(itemDataList[0], ProgParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addProgParamMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDeleteItem, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddProgParameter, addProgParamMenuItem)
        return menu
      
      if isinstance(itemDataList[0], EnvParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addEnvParamMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDeleteItem, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddEnvParameter, addEnvParamMenuItem)
        return menu
      
      if isinstance(itemDataList[0], Component):
        menu.AppendItem(editMenuItem)
        if itemDataList[1] == 'name':
          menu.AppendItem(deleteMenuItem)
          menu.AppendItem(addCompMenuItem)
          menu.AppendItem(addArgMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDeleteItem, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddComponent, addCompMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddArgument, addArgMenuItem)
        return menu
      
      if isinstance(itemDataList[0], Facet):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addFacetMenuItem)
        self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
        self.Bind(wx.EVT_MENU, self.OnDeleteItem, deleteMenuItem)
        self.Bind(wx.EVT_MENU, self.OnAddFacet, addFacetMenuItem)

        return menu
      
      # For all other items (except headings):
      menu.AppendItem(editMenuItem)
      self.Bind(wx.EVT_MENU, self.OnRename, editMenuItem)
      return menu
      
    else:
      return None
  
  #Gets the object associated with the parent of the currently selected item;
  #if the parent is just a heading item, go up one more level and get that obj;
  #if no other parent is found, just return None
  def getParentObj(self):
    parentItem = self.tree.GetItemParent(self.currentItem)
    parentData = self.tree.GetPyData(parentItem)
    if parentData is None: # it's a heading item, so get the parent's parent
      parentItem = self.tree.GetItemParent(parentItem)
      if parentItem is not None:
        parentData = self.tree.GetPyData(parentItem)
      else:
        return None
    return parentData[0]
  
    