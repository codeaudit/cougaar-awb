#!/bin/env python
#----------------------------------------------------------------------------
# Name:         insertion_dialog.py
# Purpose:      dialogs for insertion
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: insertion_dialog.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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
from ACMEPy.parameter import VMParameter
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from ACMEPy.facet import Facet
from ACMEPy.component import Component
from ACMEPy.argument import Argument
from ACMEPy.parameter import *

#---------------------------------------------------------------------------

class NewEntityDialog (wxTextEntryDialog):

  def __init__(self, parent, label):
    wxTextEntryDialog.__init__(self, parent, label, 'Add New Entity')
    self.SetSize((175, -1))
    if self.ShowModal() == wxID_OK:
      parent.newEntityName = self.GetValue()
    self.Destroy()

#---------------------------------------------------------------------------

class NewNodeDialog:

  def __init__(self, parent):
    self.win = wxDialog(parent, -1, "New Node", size=wxSize(400, 200),
                   style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)
    ###---------------------------------------------------
    self.parent = parent
    sizer = wxBoxSizer(wxVERTICAL)
    
    label = wxStaticText(self.win, -1, "New Node")
    sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
    
    # text boxes
    # Name
    nameBox = wxBoxSizer(wxHORIZONTAL)
    nameLabel = wxStaticText(self.win, -1, "Name:")
    nameBox.Add(nameLabel, 0, wxALIGN_CENTRE|wxALL, 5)
    
    tID = wxNewId()
    self.nodeName = wxTextCtrl(self.win, tID, "", size=(200,-1))
    nameBox.Add(self.nodeName, 1, wxALIGN_CENTRE|wxALL, 5)
    
    sizer.AddSizer(nameBox, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)
    
    # Class
    classBox = wxBoxSizer(wxHORIZONTAL)
    
    classLabel = wxStaticText(self.win, -1, "Class:")
    classBox.Add(classLabel, 0, wxALIGN_CENTRE|wxALL, 5)
    
    nodeClass = wxTextCtrl(self.win, -1, "org.cougaar.bootstrap.Bootstrapper", size=(200,-1))
    classBox.Add(nodeClass, 1, wxALIGN_CENTRE|wxALL, 5)
    
    sizer.AddSizer(classBox, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)
    
    # parameters
    self.progPanel = AddParameterPanel(self.win, 'prog', True)
    sizer.Add(self.progPanel, 1, wxGROW)
    self.envPanel = AddParameterPanel(self.win, 'env', True)
    sizer.Add(self.envPanel, 1, wxGROW)
    self.envPanel.Show()
    self.vmPanel = AddParameterPanel(self.win, 'vm', True)
    self.vmPanel.params.SetInsertionPoint(0)  # insert next item at top of the list
    self.vmPanel.params.WriteText("-Dorg.cougaar.node.name=" + \
                                                  "(system will complete)")
    self.vmPanel.params.SetInsertionPointEnd()  # now go back to the end
    self.vmPanel.params.WriteText("\n-Dorg.cougaar.name.server=" + \
                                                  self.parent.parent.frame.society.get_nameserver())
    sizer.Add(self.vmPanel, 1, wxGROW)
    self.vmPanel.Show()
    
    line = wxStaticLine(self.win, -1, size=(20,-1), style=wxLI_HORIZONTAL)
    sizer.Add(line, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxRIGHT|wxTOP, 5)
    
    # buttons
    box = wxBoxSizer(wxHORIZONTAL)
    btn = wxButton(self.win, wxID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
    
    btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
    
    sizer.AddSizer(box, 0, wxALIGN_CENTER|wxALL, 5)
    
    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(true)
    sizer.Fit(self.win)
    self.win.CenterOnParent()
    
    val = self.win.ShowModal()
    if val == wxID_OK:
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
    self.win = wxDialog(parent, -1, "New Agent", size=wxSize(350, 200),
                   style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)

    sizer = wxBoxSizer(wxVERTICAL)

    label = wxStaticText(self.win, -1, "New Agent")
    sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    box = wxBoxSizer(wxHORIZONTAL)

    label = wxStaticText(self.win, -1, "Name:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    # Agent name text box
    agentName = wxTextCtrl(self.win, -1, "", size=(200,-1))
    box.Add(agentName, 1, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)

    box = wxBoxSizer(wxHORIZONTAL)

    label = wxStaticText(self.win, -1, "Class:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    # Agent class text box
    agentClass = wxTextCtrl(self.win, -1, "org.cougaar.core.agent.SimpleAgent", size=(200,-1))
    box.Add(agentClass, 1, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)

    line = wxStaticLine(self.win, -1, size=(20,-1), style=wxLI_HORIZONTAL)
    sizer.Add(line, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxRIGHT|wxTOP, 5)

    # OK and CANCEL buttons
    box = wxBoxSizer(wxHORIZONTAL)

    btn = wxButton(self.win, wxID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxALIGN_CENTER|wxALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(true)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wxID_OK:
        parent.newEntityName = agentName.GetValue()
        parent.newAgentClass = agentClass.GetValue()
    self.win.Destroy()

#---------------------------------------------------------------------------

class NewComponentDialog:
  def __init__(self, parent):
    self.win = wxDialog(parent, -1, "New Component", size=wxSize(350, 200),
                   style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)
###---------------------------------------------------

    sizer = wxBoxSizer(wxVERTICAL)

    label = wxStaticText(self.win, -1, "New Component")
    sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)


# text boxes
# Name
    box = wxBoxSizer(wxHORIZONTAL)
    label = wxStaticText(self.win, -1, "Name:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    componentName = wxTextCtrl(self.win, -1, "", size=(80,-1))
    box.Add(componentName, 1, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)

# Class
    box = wxBoxSizer(wxHORIZONTAL)

    label = wxStaticText(self.win, -1, "Class:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    componentClass = wxTextCtrl(self.win, -1, "", size=(150,-1))
    box.Add(componentClass, 1, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)

    line = wxStaticLine(self.win, -1, size=(20,-1), style=wxLI_HORIZONTAL)
    sizer.Add(line, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxRIGHT|wxTOP, 5)

# Priority
    box = wxBoxSizer(wxHORIZONTAL)
    label = wxStaticText(self.win, -1, "Priority:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
    
    prioValues = ["HIGH", "INTERNAL", "BINDER", "COMPONENT", "LOW"]
    defaultPrio = "COMPONENT"
    componentPriority = wxComboBox(self.win, -1, defaultPrio, wxDefaultPosition, wxSize(100, -1),
                    prioValues, wxCB_DROPDOWN | wxCB_READONLY)
    box.Add(componentPriority, 0, wxALIGN_CENTRE|wxALL, 5)
  
# Order
    label = wxStaticText(self.win, -1, "Order:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
    componentOrder = wxTextCtrl(self.win, -1, "", size=wxSize(50, -1))
    #~ box.Add(orderSpinner, 0, wxALIGN_CENTRE|wxALL, 5)
    box.Add(componentOrder, 0, wxALIGN_RIGHT|wxALL, 5)
    
    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)
  
# InsertionPoint
    box = wxBoxSizer(wxHORIZONTAL)
    label = wxStaticText(self.win, -1, "Insertion Point:")
    box.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

    componentInsertionPoint = wxTextCtrl(self.win, -1, "Node.AgentManager.Agent.PluginManager.Plugin", 
                                                        size=(250,-1))
    box.Add(componentInsertionPoint, 1, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)
### ------------------------------------
    box = wxBoxSizer(wxHORIZONTAL)
    btn = wxButton(self.win, wxID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxALIGN_CENTER|wxALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(true)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wxID_OK:
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
    self.win = wxDialog(parent, -1, title, size=wxSize(350, 200),
                   style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)
    
###---------------------------------------------------

    sizer = wxBoxSizer(wxVERTICAL)

    label = wxStaticText(self.win, -1, labelText)
    sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

# parameters
    if self.valueType is None:  # allow entry of all three types of parameter
      self.progPanel = AddParameterPanel(self.win, 'prog')
      sizer.Add(self.progPanel, 1, wxGROW)
      self.displayedPanels.append(self.progPanel)
      self.envPanel = AddParameterPanel(self.win, 'env')
      sizer.Add(self.envPanel, 1, wxGROW)
      self.displayedPanels.append(self.envPanel)
      self.envPanel.Show()
      self.vmPanel = AddParameterPanel(self.win, 'vm')
      sizer.Add(self.vmPanel, 1, wxGROW)
      self.displayedPanels.append(self.vmPanel)
      self.vmPanel.Show()
    else:  # only allow entry of one type of parameter
      self.panel = AddParameterPanel(self.win, self.valueType)
      sizer.Add(self.panel, 1, wxGROW)
      self.displayedPanels.append(self.panel)
    
    line = wxStaticLine(self.win, -1, size=(20,-1), style=wxLI_HORIZONTAL)
    sizer.Add(line, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5)

# buttons
    box = wxBoxSizer(wxHORIZONTAL)
    btn = wxButton(self.win, wxID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxALIGN_CENTER|wxALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(true)
    sizer.Fit(self.win)
    self.win.CenterOnParent()

    val = self.win.ShowModal()
    if val == wxID_OK:
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
                errorDialog = wxMessageDialog(self.parent, msg, style = wxCAPTION | wxOK | 
                     wxTHICK_FRAME | wxICON_ERROR)
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
class AddParameterPanel(wxPanel):

  def __init__(self, parent, paramType, nodeCreation=False):
    wxPanel.__init__(self, parent, -1)
    self.parent = parent
    self.paramType = paramType
    self.nodeCreation = nodeCreation
    self.defaultParam = ""
    
    if nodeCreation is True and self.paramType == "prog":
      self.defaultParam = "org.cougaar.core.node.Node"
    elif nodeCreation is True and self.paramType == "vm":
      self.defaultParam = '''
-Dorg.cougaar.core.agent.startTime=08/10/2005
-Dorg.cougaar.core.persistence.clear=true
-Dorg.cougaar.core.persistence.enable=false
-Dorg.cougaar.planning.ldm.lps.ComplainingLP.level=0
-Duser.timezone=GMT'''
    box = wxBoxSizer(wxVERTICAL)
    
    labelText = ""
    if self.paramType == "facet":
      labelText = "Facets:"
    else:
      labelText = self.paramType + "_parameters:"
    progLabel = wxStaticText(self, -1, labelText)
    box.Add(progLabel, 0, wxALIGN_CENTRE | wxALL, 5)
    self.params = wxTextCtrl(self, -1, self.defaultParam, size=(300,130),
                                        style=wxTE_MULTILINE | wxHSCROLL)
    self.params.SetInsertionPointEnd()
    box.Add(self.params, 1, wxGROW | wxALIGN_CENTRE | wxALL, 5)

    self.SetSizer(box)
    self.SetAutoLayout(true)
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
      self.win = wxMessageDialog(parent, msg, style = wxCAPTION | wxOK | 
                     wxTHICK_FRAME | wxICON_EXCLAMATION)
    elif dialogFormat == 1:
      self.win = wxMessageDialog(parent, msg, style = wxCAPTION | wxYES_NO | 
                     wxYES_DEFAULT | wxCANCEL | wxTHICK_FRAME | wxICON_QUESTION)
    elif dialogFormat == 2:
      self.win = wxMessageDialog(parent, msg, style = wxCAPTION | wxYES_NO | 
                     wxNO_DEFAULT | wxTHICK_FRAME | wxICON_QUESTION)
    if dialogFormat == 3:
      self.win = wxMessageDialog(parent, msg, style = wxCAPTION | wxOK | 
                     wxTHICK_FRAME | wxICON_INFORMATION)
    if dialogFormat == 4:
      self.win = wxMessageDialog(parent, msg, style = wxCAPTION | wxOK | 
                     wxTHICK_FRAME | wxICON_ERROR)
  
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
    self.win = wxDialog(parent, -1, "Find society entity", size=wxSize(350, 200),
                   style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)
    
    self.parent = parent
    sizer = wxBoxSizer(wxVERTICAL)
    
    label = wxStaticText(self.win, -1, "Enter name of society entity to find:")
    sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)
    
    # Item name text box
    self.itemName = wxTextCtrl(self.win, -1, self.parent.searchLabel, size=(200,-1))
    self.itemName.SetSelection(-1, -1)
    sizer.Add(self.itemName, 1, wxALIGN_CENTRE|wxALL, 5)
       
    # Case-sensitive search desired checkbox
    self.caseSearchDesired = False
    caseSearchID = wxNewId()
    self.caseSearchCheckbox = wxCheckBox(self.win, caseSearchID, "Perform Case-Sensitive Search")
    self.caseSearchCheckbox.SetValue(self.parent.caseSearchDesired)
    EVT_CHECKBOX(self.win, caseSearchID, self.OnCaseSearchChecked)
    sizer.Add(self.caseSearchCheckbox, flag=wxALIGN_CENTER_HORIZONTAL | wxBOTTOM, border=7)
    
    # Viewer in which to search radio box
    rbID = wxNewId()
    rbLabel = "Search for desired item in:"
    buttonTitles = ["Agent List", "HNA Map                      "]
    self.rb = wxRadioBox(self.win, rbID, rbLabel, wxDefaultPosition, (-1, 80), buttonTitles, 1, wxRA_SPECIFY_COLS)
    self.rb.SetSelection(1)  # HNA Map is default selection
    if not showViewerRadio:
      self.rb.Enable(false)
      self.viewerToSearch = self.parent.societyViewer
    else:
      self.viewerToSearch = self.parent.laydownViewer
    EVT_RADIOBOX(self.win, rbID, self.OnEvtRadioBox)
    sizer.Add(self.rb, 0, wxALIGN_CENTER | wxALL, 10)
    
    line = wxStaticLine(self.win, -1, size=(20,-1), style=wxLI_HORIZONTAL)
    sizer.Add(line, 0, wxGROW | wxALIGN_CENTER | wxTOP, 5)

    # OK and CANCEL buttons
    box = wxBoxSizer(wxHORIZONTAL)

    btn = wxButton(self.win, wxID_OK, " OK ")
    btn.SetDefault()
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
    box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    sizer.AddSizer(box, 0, wxALIGN_CENTER|wxALL, 5)

    self.win.SetSizer(sizer)
    self.win.SetAutoLayout(true)
    sizer.Fit(self.win)

    val = self.win.ShowModal()
    if val == wxID_OK:
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

class NodeInfoEditor(wxFrame):

  EDIT = 0
  DELETE = 1
  ADD = 2

  def __init__(self, parent, log, ID = -1, title = 'Edit Node Info', 
                    pos=wxDefaultPosition, size=(450,450), 
                    style=wxDEFAULT_FRAME_STYLE):
    wxFrame.__init__(self, parent, ID, title, pos, size, style)
    self.parent = parent
    self.log = log
    self.changesToMake = []
    tID = wxNewId()
    
    self.tree = wxTreeCtrl(self, tID, wxDefaultPosition, (450,450),
                           wxTR_HAS_BUTTONS | wxTR_EDIT_LABELS)
    
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
    
    cookie = 1     # required by wxTreeCtrl for getting children.  See docs.
    self.ExpandTree(self.root, cookie)
    self.tree.SelectItem(self.root)
    
    EVT_TREE_SEL_CHANGED    (self, tID, self.OnSelChanged)
    EVT_TREE_BEGIN_LABEL_EDIT(self, tID, self.OnBeginEdit)
    EVT_TREE_END_LABEL_EDIT (self, tID, self.OnEndEdit)
    EVT_TREE_DELETE_ITEM(self, tID, self.OnDelete)
    EVT_RIGHT_DOWN(self.tree, self.OnRightClick)
    EVT_RIGHT_UP(self.tree, self.OnRightUp)

###---------------------------------------------------

    sizer = wxBoxSizer(wxVERTICAL)
    
    btnBox = wxBoxSizer(wxHORIZONTAL)
    btn = wxButton(self, wxID_OK, "  OK  ")
    EVT_BUTTON(self, wxID_OK, self.OnOK)  
    btn.SetDefault()
    btnBox.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    btn = wxButton(self, wxID_CANCEL, " Cancel ")
    EVT_BUTTON(self, wxID_CANCEL, self.OnCancel)  
    EVT_CLOSE(self, self.OnCloseWindow)
    btnBox.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

    sizer.Add(self.tree, 1, wxEXPAND | wxALIGN_CENTER)
    sizer.Add(btnBox, 0, wxALIGN_CENTER|wxALL, 5)

    self.SetSizer(sizer)
    self.SetAutoLayout(true)
    self.CenterOnParent()

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
      self.PopupMenu(menu, wxPoint(self.x, self.y))
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
    self.Close(true)
    self.parent.infoFrameOpen = 0
    
  def OnCancel(self, event):
    self.changesToMake = []  # empty it out
    self.Close(true)
    self.parent.infoFrameOpen = 0
    
  def OnCloseWindow(self, event):
    self.Destroy()
 
  def OnRename(self, event):
    if isinstance(self.itemDataList[0], Component) and self.itemDataList[1] == "priority":
      dlg = wxDialog(self.tree, -1, "Edit Component Priority", 
                     style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)
      sizer = wxBoxSizer(wxVERTICAL)
      label = wxStaticText(dlg, -1, "Select new Priority")
      sizer.Add(label, 0, wxALIGN_CENTRE | wxALL, 5)
      prioValues = ["HIGH", "INTERNAL", "BINDER", "COMPONENT", "LOW"]
      defaultPrio = self.itemDataList[0].priority
      componentPriority = wxComboBox(dlg, -1, defaultPrio, wxDefaultPosition, wxSize(100, -1),
                      prioValues, wxCB_DROPDOWN | wxCB_READONLY)
      sizer.Add(componentPriority, 0, wxALIGN_CENTRE | wxALL, 5)
      box = wxBoxSizer(wxHORIZONTAL)
      btn = wxButton(dlg, wxID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
      
      btn = wxButton(dlg, wxID_CANCEL, " Cancel ")
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
      
      sizer.AddSizer(box, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5)
      
      dlg.SetSizer(sizer)
      dlg.SetAutoLayout(true)
      sizer.Fit(dlg)
      val = dlg.ShowModal()
      if val == wxID_OK:
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
    if treeNode.IsOk():
      self.tree.Expand(treeNode)
      child = self.tree.GetFirstChild(treeNode, cookie)
      while child[0].IsOk():
        self.ExpandTree(child[0], child[1])
        child = self.tree.GetNextChild(child[0], child[1])

  def SetMenu(self, itemDataList):
  
    tID1 = 0
    tID2 = 1
    tID3 = 2
    tID4 = 3
    tID5 = 4
    tID6 = 5
    tID7 = 6
    tID8 = 7
    
    menu = wxMenu()
    editMenuItem = wxMenuItem(menu, tID1, "Edit")
    deleteMenuItem = wxMenuItem(menu, tID2, "Delete")
    addVmParamMenuItem = wxMenuItem(menu, tID3, "Add vm_parameter")
    addProgParamMenuItem = wxMenuItem(menu, tID6, "Add prog_parameter")
    addEnvParamMenuItem = wxMenuItem(menu, tID7, "Add env_parameter")
    addCompMenuItem = wxMenuItem(menu, tID4, "Add Component")
    addArgMenuItem = wxMenuItem(menu, tID5, "Add Argument")
    addFacetMenuItem = wxMenuItem(menu, tID8, "Add Facet")
    
    if self.tree.GetItemText(self.currentItem) == "VM_Parameters":
      menu.AppendItem(addVmParamMenuItem)
      EVT_MENU(self, tID3, self.OnAddVmParameter)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Prog_Parameters":
      menu.AppendItem(addProgParamMenuItem)
      EVT_MENU(self, tID6, self.OnAddProgParameter)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Env_Parameters":
      menu.AppendItem(addEnvParamMenuItem)
      EVT_MENU(self, tID7, self.OnAddEnvParameter)
      return menu
    
    if self.tree.GetItemText(self.currentItem) == "Components":
      menu.AppendItem(addCompMenuItem)
      EVT_MENU(self, tID4, self.OnAddComponent)
      return menu

    if self.tree.GetItemText(self.currentItem) == "Arguments":
      menu.AppendItem(addArgMenuItem)
      EVT_MENU(self, tID5, self.OnAddArgument)
      return menu

    if self.tree.GetItemText(self.currentItem) == "Facets":
      menu.AppendItem(addFacetMenuItem)
      EVT_MENU(self, tID8, self.OnAddFacet)
      return menu

    if itemDataList is not None:
      if isinstance(itemDataList[0], VMParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addVmParamMenuItem)
        EVT_MENU(self, tID1, self.OnRename)
        EVT_MENU(self, tID2, self.OnDeleteItem)
        EVT_MENU(self, tID3, self.OnAddVmParameter)
        return menu
      
      if isinstance(itemDataList[0], ProgParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addProgParamMenuItem)
        EVT_MENU(self, tID1, self.OnRename)
        EVT_MENU(self, tID2, self.OnDeleteItem)
        EVT_MENU(self, tID6, self.OnAddProgParameter)
        return menu
      
      if isinstance(itemDataList[0], EnvParameter):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addEnvParamMenuItem)
        EVT_MENU(self, tID1, self.OnRename)
        EVT_MENU(self, tID2, self.OnDeleteItem)
        EVT_MENU(self, tID7, self.OnAddEnvParameter)
        return menu
      
      if isinstance(itemDataList[0], Component):
        menu.AppendItem(editMenuItem)
        if itemDataList[1] == 'name':
          menu.AppendItem(deleteMenuItem)
          menu.AppendItem(addCompMenuItem)
          menu.AppendItem(addArgMenuItem)
        EVT_MENU(self, tID1, self.OnRename)
        EVT_MENU(self, tID2, self.OnDeleteItem)
        EVT_MENU(self, tID4, self.OnAddComponent)
        EVT_MENU(self, tID5, self.OnAddArgument)
        return menu
      
      if isinstance(itemDataList[0], Facet):
        menu.AppendItem(editMenuItem)
        menu.AppendItem(deleteMenuItem)
        menu.AppendItem(addFacetMenuItem)
        EVT_MENU(self, tID1, self.OnRename)
        EVT_MENU(self, tID2, self.OnDeleteItem)
        EVT_MENU(self, tID8, self.OnAddFacet)
        return menu
      
      # For all other items (except headings):
      menu.AppendItem(editMenuItem)
      EVT_MENU(self, tID1, self.OnRename)
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
  
    