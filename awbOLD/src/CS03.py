#!/bin/env python
#----------------------------------------------------------------------------
# Name:         CS03.py
# Purpose:      CSmarter umbrella
#
# Author:       ISAT (D. Moore
#
# RCS-ID:       $Id: CS03.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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
import sys, os, time
from   wxPython.wx import *
from   wxPython.html import wxHtmlWindow
from societyBuilder import SocietyBuilderPanel
from agentLaydown import AgentLaydownPanel
from societyEditor import SocietyEditorPanel
from insertion_dialog import CougaarMessageDialog
from insertion_dialog import FindItemDialog
from societyFactoryServer import SocietyFactoryServer
from societyController import *
from ACMEPy.node import Node
import images

#---------------------------------------------------------------------------

class MyLog(wxPyLog):
    def __init__(self, textCtrl, logTime=0):
        wxPyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime
        self.logFile = open('CSMARTer.log', 'w')

    def DoLogString(self, message, timeStamp):
        timeStr = time.strftime("%a, %d %b %Y %H:%M:%S",
            time.localtime(timeStamp)) + ": "
        if self.logTime:
            #~ message = time.strftime("%X", time.localtime(timeStamp)) + \
            message =  timeStr + message
        if self.tc:
            self.tc.AppendText(message + '\n')
        self.logFile.write(timeStr + message + '\n')

    def Close(self):
        self.logFile.close()
        del self.logFile

#---------------------------------------------------------------------------

class MyTP(wxPyTipProvider):
    def GetTip(self):
        return "This is my tip"

#---------------------------------------------------------------------------

def opj(path):
    """Convert paths to the platform-specific separator"""
    return apply(os.path.join, tuple(path.split('/')))


#---------------------------------------------------------------------------

class CSmarter(wxFrame):
    overviewText = "Overview"

    # constants to refer to the wxNotebook pages
    OVERVIEW = 0
    RULE_EDITOR = 1
    SOCIETY_EDITOR = 2
    AGENT_LAYDOWN = 3

    # establish some menu item id constants
    SAVE_RULE = 0
    SAVE_AS_RULE = 1
    SAVE_SOCIETY = 2
    SAVE_AS_SOCIETY = 3
    SAVE_AS_HNA_SOCIETY = 4
    UNDO = 5
    CHANGE_NAMESERVER = 6
    SHOW_SOCIETY = 7
    SHOW_HOSTS = 8
    SHOW_NODES = 9
    SHOW_AGENTS = 10
    SHOW_COMPONENTS = 11
    COLLAPSE_HOSTS = 12
    COLLAPSE_NODES = 13
    COLLAPSE_AGENTS = 14
    COLLAPSE_COMPONENTS = 15
    SORT = 16
    FIND = 17
    CLOSE_RULEBOOK = 18
    DELETE_RULE = 19
    FIND_NEXT = 20
    RENAME_RULE = 21

    def __init__(self, parent, id, title, initHeight = 710, initPane=1):
      wxFrame.__init__(self, parent, -1, title, size = (800, initHeight),
                       style=wxDEFAULT_FRAME_STYLE|wxNO_FULL_REPAINT_ON_RESIZE)

      self.cwd = os.getcwd()
      self.curOverview = ""
      self.window = None
      self.initialPane = initPane
      self.nb = None
      self.log = None
      self.society = None  # for holding a society in Society Editor and Rule tabs
      self.agentSociety = None # for holding a society that's just an agent list
      self.mappedSociety = None # for holding a newly HNA-mapped society
      self.societyViewer = None # wxTreeCtrl for displaying the society in Society Editor
      self.agentViewer = None  # wxTreeCtrl for displaying initial agent list in Agent Laydown tab
      self.laydownViewer = None  # wxTreeCtrl for displaying host-node-agent laydown
      self.societyOpen = false  # for the Society Editor
      self.agentSocietyOpen = false  # for the Agent List in Agent Laydown tab
      self.mappedSocietyOpen = false  # for the HNA Map in Agent Laydown tab
      self.societyFile = None  # string name of xml file for self.society
      self.agentSocietyFile = None  # string name of xml file for self.agentSociety
      self.societyHnaFile = None  # string name of xml file for self.mappedSociety
      self.controlFile = None # string name of xml file for self.controlFile
      self.ruleOpen = false
      self.ruleApplied = false
      self.currentPage = CSmarter.RULE_EDITOR
      self.currentTree = None
      self.undoBuffer = []
      self.rulebookId = CSmarter.CLOSE_RULEBOOK * 10

      self.openRulebookCount = 0
      self.searchLabel = ""
      self.caseSearchDesired = False
      self.objCloset = {} # for storing entity obj's during DnD ops
      self.dragSource = None  # for storing viewer that was source of a drag
      self.windowHeight = initHeight
      self.mappedSocietySaveCounter = 0
      icon = images.getCSMARTerIcon()
      self.SetIcon(icon)

      try:
        if wxPlatform == '__WXMSW__':
            # setup a taskbar icon, and catch some events from it
            self.tbicon = wxTaskBarIcon()
            self.tbicon.SetIcon(icon, "CS03")
            EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.OnTaskBarActivate)
            EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarMenu)
            EVT_MENU(self.tbicon, self.TBMENU_RESTORE, self.OnTaskBarActivate)
            EVT_MENU(self.tbicon, self.TBMENU_CLOSE, self.OnTaskBarClose)

        wxCallAfter(self.ShowTip)

        self.otherWin = None
        EVT_IDLE(self, self.OnIdle)
        EVT_CLOSE(self, self.OnCloseWindow)
        EVT_ICONIZE(self, self.OnIconfiy)
        EVT_MAXIMIZE(self, self.OnMaximize)

        self.Centre(wxBOTH)
        self.CreateStatusBar(1, wxST_SIZEGRIP)

        splitterId = wxNewId()
        self.splitter2 = wxSplitterWindow(self, splitterId, style=wxNO_3D|wxSP_3D)
        EVT_SIZE(self, self.OnSplitterResize)

        def EmptyHandler(evt):
          pass

        EVT_ERASE_BACKGROUND(self.splitter2, EmptyHandler)

        #---------------------------------------------------------------------------

        # Make a File menu
        self.mainmenu = wxMenuBar()
        fileMenu = wxMenu()

        fileMenu.Append(CSmarter.SAVE_RULE, 'Save &Rule\tCtrl+R', 'Save an existing rule')
        EVT_MENU(self, CSmarter.SAVE_RULE, self.OnRuleSave)

        fileMenu.Append(CSmarter.SAVE_AS_RULE, 'Save R&ule As...\tAlt+R', 'Save as a new rule')
        EVT_MENU(self, CSmarter.SAVE_AS_RULE, self.OnRuleSaveAs)

        fileMenu.Append(CSmarter.SAVE_SOCIETY, '&Save Society\tCtrl+S', 'Save an existing society')
        EVT_MENU(self, CSmarter.SAVE_SOCIETY, self.OnSocietySave)

        fileMenu.Append(CSmarter.SAVE_AS_SOCIETY, 'Save Society &As...\tAlt+S', 'Save as a new society')
        EVT_MENU(self, CSmarter.SAVE_AS_SOCIETY, self.OnSocietySaveAs)

        fileMenu.Append(CSmarter.SAVE_AS_HNA_SOCIETY, 'Save HNA &Map As...\tAlt+M', 'Save as a new society')
        EVT_MENU(self, CSmarter.SAVE_AS_HNA_SOCIETY, self.OnHnaMapSaveAs)

        exitID = wxNewId()
        fileMenu.Append(exitID, 'E&xit\tAlt+X', 'Get the heck outta here!')
        EVT_MENU(self, exitID, self.OnFileExit)

        if not self.ruleOpen:
          fileMenu.Enable(CSmarter.SAVE_RULE, false)
          fileMenu.Enable(CSmarter.SAVE_AS_RULE, false)
        if not self.societyOpen:
          fileMenu.Enable(CSmarter.SAVE_SOCIETY, false)
          fileMenu.Enable(CSmarter.SAVE_AS_SOCIETY, false)
        if not self.mappedSocietyOpen:
          fileMenu.Enable(CSmarter.SAVE_AS_HNA_SOCIETY, false)

        self.mainmenu.Append(fileMenu, '&File')

        #---------------------------------------------------------------------------

        # Make an Edit menu
        self.editMenu = wxMenu()

        self.editMenu.Append(CSmarter.UNDO, '&Undo\tCtrl+Z', 'Undo last edit')
        EVT_MENU(self, CSmarter.UNDO, self.OnUndo)
        self.editMenu.Enable(CSmarter.UNDO, false)

        self.editMenu.Append(CSmarter.SORT, '&Sort selected item', 'Sort entities in selected item')
        EVT_MENU(self, CSmarter.SORT, self.OnSort)
        self.editMenu.Enable(CSmarter.SORT, false)

        self.editMenu.Append(CSmarter.CHANGE_NAMESERVER, 'Change &name server', 'Specify a new name server')
        EVT_MENU(self, CSmarter.CHANGE_NAMESERVER, self.OnChangeNameServer)
        self.editMenu.Enable(CSmarter.CHANGE_NAMESERVER, false)

        self.editMenu.Append(CSmarter.FIND, '&Find\tCtrl+F', 'Find a specific society entity by name')
        EVT_MENU(self, CSmarter.FIND, self.OnFind)
        self.editMenu.Enable(CSmarter.FIND, false)

        self.editMenu.Append(CSmarter.FIND_NEXT, 'Find &Next\tF3', 'Find the next occurrence of a specific society entity by name')
        EVT_MENU(self, CSmarter.FIND_NEXT, self.OnFindNext)
        self.editMenu.Enable(CSmarter.FIND_NEXT, false)

        self.editMenu.Append(CSmarter.RENAME_RULE, '&Rename Rule\tCtrl+R', 'Rename a society transformation rule')
        EVT_MENU(self, CSmarter.RENAME_RULE, self.OnRenameRule)
        self.editMenu.Enable(CSmarter.RENAME_RULE, false)

        self.editMenu.Append(CSmarter.DELETE_RULE, '&Delete Rule\tAlt+D', 'Delete a society transformation rule')
        EVT_MENU(self, CSmarter.DELETE_RULE, self.OnDeleteRule)
        self.editMenu.Enable(CSmarter.DELETE_RULE, false)

        self.mainmenu.Append(self.editMenu, '&Edit')

        #---------------------------------------------------------------------------

        # Make an View menu
        self.viewMenu = wxMenu()

        self.viewMenu.Append(CSmarter.SHOW_SOCIETY, 'Show &Entire Society\tCtrl+E', 'Expand entire Society tree')
        EVT_MENU(self, CSmarter.SHOW_SOCIETY, self.OnShowSociety)

        self.viewMenu.Append(CSmarter.SHOW_NODES, 'Show All &Nodes\tCtrl+N', 'Show All Nodes')
        EVT_MENU(self, CSmarter.SHOW_NODES, self.OnShowNodes)

        self.viewMenu.Append(CSmarter.SHOW_AGENTS, 'Show All &Agents\tCtrl+A', 'Show All Agents')
        EVT_MENU(self, CSmarter.SHOW_AGENTS, self.OnShowAgents)

        self.viewMenu.Append(CSmarter.SHOW_COMPONENTS, 'Show All &Components\tCtrl+C', 'Show All Components')
        EVT_MENU(self, CSmarter.SHOW_COMPONENTS, self.OnShowComponents)

        self.viewMenu.Append(CSmarter.COLLAPSE_HOSTS, 'Collapse To &Hosts\tAlt+O', 'Collapse To Hosts')
        EVT_MENU(self, CSmarter.COLLAPSE_HOSTS, self.OnCollapseHosts)

        self.viewMenu.Append(CSmarter.COLLAPSE_NODES, 'Collapse To &Nodes\tAlt+N', 'Collapse To Nodes')
        EVT_MENU(self, CSmarter.COLLAPSE_NODES, self.OnCollapseNodes)

        self.viewMenu.Append(CSmarter.COLLAPSE_AGENTS, 'Collapse To &Agents\tAlt+A', 'Collapse To Agents')
        EVT_MENU(self, CSmarter.COLLAPSE_AGENTS, self.OnCollapseAgents)

        self.viewMenu.Append(CSmarter.COLLAPSE_COMPONENTS, 'Collapse To &Components\tAlt+C', 'Collapse To Components')
        EVT_MENU(self, CSmarter.COLLAPSE_COMPONENTS, self.OnCollapseComponents)

        self.viewMenu.AppendSeparator()

        helpText = "Removes rules belonging to the chosen rulebook from the Rulebook window"
        self.viewMenu.Append(CSmarter.CLOSE_RULEBOOK, "Close RuleBook\tCtrl+B", helpText)
        EVT_MENU(self, CSmarter.CLOSE_RULEBOOK, self.OnCloseRulebook)

        self.viewMenu.Enable(CSmarter.SHOW_SOCIETY, false)
        self.viewMenu.Enable(CSmarter.SHOW_NODES, false)
        self.viewMenu.Enable(CSmarter.SHOW_AGENTS, false)
        self.viewMenu.Enable(CSmarter.SHOW_COMPONENTS, false)
        self.viewMenu.Enable(CSmarter.COLLAPSE_HOSTS, false)
        self.viewMenu.Enable(CSmarter.COLLAPSE_NODES, false)
        self.viewMenu.Enable(CSmarter.COLLAPSE_AGENTS, false)
        self.viewMenu.Enable(CSmarter.COLLAPSE_COMPONENTS, false)
        self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, false)

        self.mainmenu.Append(self.viewMenu, '&View')

        #---------------------------------------------------------------------------

        # Make a Help menu
        helpMenu = wxMenu()

        debugMenu = wxMenu()

        printSocModelId = wxNewId()
        debugMenu.Append(printSocModelId, 'Print society model (plain text)\tF11', 'Print plain text to console window.')
        EVT_MENU(self, printSocModelId, self.OnPrintSocietyModelPlain)

        printSocModelXmlId = wxNewId()
        debugMenu.Append(printSocModelXmlId, 'Print society model (XML)\tF12', 'Print XML text to console window.')
        EVT_MENU(self, printSocModelXmlId, self.OnPrintSocietyModelXML)

        debugId = wxNewId()
        helpMenu.AppendMenu(debugId, "Debug", debugMenu)

        helpId = wxNewId()
        helpMenu.Append(helpId, '&About\tF1', 'wxPython RULES!!!')
        EVT_MENU(self, helpId, self.OnHelpAbout)

        self.mainmenu.Append(helpMenu, '&Help')

        #---------------------------------------------------------------------------

        self.SetMenuBar(self.mainmenu)

        # set the menu accellerator table...
        aTable = wxAcceleratorTable([(wxACCEL_ALT,  ord('X'), exitID),
                                     (wxACCEL_CTRL, ord('H'), helpId)])
        self.SetAcceleratorTable(aTable)

        #---------------------------------------------------------------------------


        # Create a Notebook to go in top of wxSplitterWindow
        self.nb = wxNotebook(self.splitter2, -1, style=wxCLIP_CHILDREN)
        EVT_NOTEBOOK_PAGE_CHANGED(self, -1, self.OnPageChange)

        # Set up a log on the View Log Notebook page to go in bottom of wxSplitter Window
        self.log = wxTextCtrl(self.splitter2, -1,
                              style = wxTE_MULTILINE|wxTE_READONLY|wxHSCROLL)

        # Set the wxWindows log target to be this textctrl
        #wxLog_SetActiveTarget(wxLogTextCtrl(self.log))

        # But instead of the above we want to show how to use our own wxLog class
        self.logger = MyLog(self.log)
        wxLog_SetActiveTarget(self.logger)

        #~ wxLogChain(wxLogStderr())
        #~ wxLogChain(self.logger)

        #~ wxLog_SetLogLevel(wxLOG_Warning)
        wxLog_SetLogLevel(wxLOG_Message)

        # for serious debugging
        #wxLog_SetActiveTarget(wxLogStderr())
        #wxLog_SetTraceMask(wxTraceMessages)

        # Notebook page 0:  CSMARTer Overview
        if 0:  # the old way
            self.ovr = wxHtmlWindow(self.nb, -1, size=(400, 400))
            self.nb.AddPage(self.ovr, self.overviewText)

        else:  # hopefully I can remove this hacky code soon, see bug #216861
            panel = wxPanel(self.nb, -1, style=wxCLIP_CHILDREN)
            self.ovr = wxHtmlWindow(panel, -1, size=(400, 400))
            self.nb.AddPage(panel, self.overviewText)

            def OnOvrSize(evt, ovr=self.ovr):
                ovr.SetSize(evt.GetSize())

            EVT_SIZE(panel, OnOvrSize)
            EVT_ERASE_BACKGROUND(panel, EmptyHandler)

        self.SetOverview(self.overviewText, overview)

        # Notebook page 1:  Rule Editor
        self.ruleEditor = SocietyBuilderPanel(self.nb, self, self.log)
        self.nb.AddPage(self.ruleEditor, 'Rules')

        # Notebook page 2:  Society Editor
        self.societyEditor = SocietyEditorPanel(self.nb, self, self.log)
        self.nb.AddPage(self.societyEditor, 'Society Editor')

        # Notebook page 3:  Agent Laydown
        self.agentLaydown = AgentLaydownPanel(self.nb, self, self.log)
        self.nb.AddPage(self.agentLaydown, 'Agent Laydown')

        # Notebook page 4:  Society Controller
        self.societyController = SocietyController(self.nb, self, self.log)
        self.nb.AddPage(self.societyController, 'Society Controller')

        self.Show(true)

        # add the windows to the splitter and split it.
        self.splitter2.SplitHorizontally(self.nb, self.log, 560)
        self.splitter2.SetMinimumPaneSize(20)

        # select initial items
        self.nb.SetSelection(self.initialPane)

        #wxLogMessage('window handle: %s' % self.GetHandle())
        wxLogMessage('CS03 initialized.')

      except Exception:
        import traceback
        traceback.print_exc()

    #---------------------------------------------
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        wxLogMessage(text)

    def write(self, txt):
        self.WriteText(txt)

    #---------------------------------------------
    def SetOverview(self, name, text):
        self.curOverview = text
        lead = text[:6]
        if lead != '<html>' and lead != '<HTML>':
            text = '<br>'.join(text.split('\n'))
        self.ovr.SetPage(text)
        self.nb.SetPageText(0, name)

    #---------------------------------------------

    def OnSplitterResize(self, event):
      # When window height is resized, we want the notebook (i.e., top panel) resized,
      # while the log panel remains constant.  Calculate how much the window height
      # changed, then move the splitter sash that much.
      # Note: this causes a LOT of flicker while the window is being resized.  I tried
      # to delay the redraw until the resizing was complete, but couldn't figure out
      # how to turn the auto redraw off.
      size = self.GetSize()
      heightChange = size.height - self.windowHeight
      sashPos = self.splitter2.GetSashPosition()
      self.splitter2.SetSashPosition(sashPos + heightChange)
      self.windowHeight = size.height
      event.Skip()

    #***************************************
    # Menu methods
    #***************************************

    # File menu methods

    def OnRuleSave(self, event):
      self.ruleEditor.SaveRule()

    def OnRuleSaveAs(self, event):
      self.ruleEditor.filename = None
      self.ruleEditor.SaveRule()

    def OnSocietySave(self, event):
      self.saveSociety("society")

    def OnSocietySaveAs(self, event):
      self.societyFile = None
      self.saveSociety("society")

    def OnHnaMapSaveAs(self, event):
      if self.agentLaydown.tempMappedSociety is not None:
        self.mappedSociety.close()
        self.mappedSociety = self.agentLaydown.tempMappedSociety
      self.mappedSocietySaveCounter = 0  # forces a 'Save As' rather than a 'Save'
      self.saveSociety("mappedSociety")

    def OnFileExit(self, event):
        self.Close()

    #---------------------------------------------

    # Edit menu methods

    def OnUndo(self, event):
      # The undoBuffer contains one object: a List named 'lastState' that contains
      # a reference to the panel in which the last edit was done and some number
      # of other Lists, each containing two elements: [0]: a reference to the control
      # last updated;  [1]: a reference to the state of that control before the last change.
      lastState = self.undoBuffer.pop()
      # Now dispatch the undo to the panel in which it was invoked
      if lastState[0] == self.agentLaydown:
        self.agentLaydown.undo(lastState)
      elif lastState[0] == self.ruleEditor:
        pass
      elif lastState[0] == self.societyEditor:
        pass
      self.mainmenu.Enable(CSmarter.UNDO, false)

    def OnSort(self, event):
      if self.currentPage == CSmarter.AGENT_LAYDOWN:
        self.currentTree = self.agentLaydown.currentViewer
      if self.currentTree is not None:
        selectedItems = self.currentTree.GetSelections()
        for selectedItem in selectedItems:
          selectedObj = self.currentTree.GetPyData(selectedItem)
          if isinstance(selectedObj, Node):
            self.currentTree.sortAgents(selectedItem)
          else:
            self.currentTree.SortChildren(selectedItem)

    def OnChangeNameServer(self, event):
      self.win = wxDialog(self, -1, "Change name server", size=wxSize(350, 200),
                     style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)

      sizer = wxBoxSizer(wxVERTICAL)

      label = wxStaticText(self.win, -1, "Select a new name server")
      sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

      ### ------------------------------------

      textBox = wxBoxSizer(wxHORIZONTAL)

      hostLabel = wxStaticText(self.win, -1, "Host:")
      textBox.Add(hostLabel, 0, wxALIGN_CENTRE)

      hostList = []
      for host in self.society.each_host():
        hostList.append(host.name)
      value = self.society.nameserver_host
      if len(hostList) == 0:
        hostList.append(value)

      self.cb = wxComboBox(self.win, 500, value, wxDefaultPosition, wxSize(65, -1),
                      hostList, wxCB_DROPDOWN | wxCB_READONLY)
      EVT_COMBOBOX(self, 500, self.EvtComboBox)
      EVT_TEXT_ENTER(self, 500, self.EvtTextEnter)
      textBox.Add(self.cb, 0, wxALIGN_CENTRE | wxALL, 5)

      portLabel = wxStaticText(self.win, -1, "Ports:")
      textBox.Add(portLabel, 0, wxALIGN_CENTRE | wxLEFT, 5)

      portValue = self.society.nameserver_suffix
      self.portText = wxTextCtrl(self.win, 505, portValue, wxDefaultPosition, wxSize(75, -1))
      textBox.Add(self.portText, 0, wxALIGN_CENTRE | wxALL, 5)

      sizer.AddSizer(textBox, 1, wxALIGN_CENTRE|wxALL, 5)

      ### ------------------------------------

      box = wxBoxSizer(wxHORIZONTAL)
      btn = wxButton(self.win, wxID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

      btn = wxButton(self.win, wxID_CANCEL, " Cancel ")
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

      sizer.AddSizer(box, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5)

      self.win.SetSizer(sizer)
      self.win.SetAutoLayout(true)
      sizer.Fit(self.win)

      val = self.win.ShowModal()
      if val == wxID_OK:
        self.society.set_nameserver(self.cb.GetValue() + self.portText.GetValue())
        #Now change the nameserver parameter in each node in the society:
        for node in self.society.each_node():
          node.updateNameServerParam(self.society.get_nameserver())

    def OnFind(self, event):
      showViewerRadio = (self.currentPage == CSmarter.AGENT_LAYDOWN)
      FindItemDialog(self, showViewerRadio)
      if len(self.searchLabel) > 0:
        self.currentTree.findItem(self.searchLabel, self.caseSearchDesired)
        #~ self.mainmenu.Enable(CSmarter.FIND_NEXT, true)

    def OnFindNext(self, event):
      if len(self.searchLabel) > 0:
        self.currentTree.findItem(self.searchLabel, self.caseSearchDesired, False)

    def OnRenameRule(self, event):
      self.ruleEditor.OnRenameRule(event)

    def OnDeleteRule(self, event):
      self.ruleEditor.OnDeleteRule(event)

    #---------------------------------------------

    def EvtComboBox(self, evt):
      pass

    def EvtTextEnter(self, evt):
      self.log.WriteText('EvtTextEnter: %s\n' % evt.GetString())

    #---------------------------------------------

    # View menu methods

    def OnShowSociety(self, event):
      self.currentTree.expandEntireSociety()

    def OnShowNodes(self, event):
      self.currentTree.expandHosts()

    def OnShowAgents(self, event):
      self.currentTree.expandNodes()

    def OnShowComponents(self, event):
      self.currentTree.expandAgents()

    def OnCollapseHosts(self, event):
      self.currentTree.collapseHosts()

    def OnCollapseNodes(self, event):
      self.currentTree.collapseNodes()

    def OnCollapseAgents(self, event):
      self.currentTree.collapseAgents()

    def OnCollapseComponents(self, event):
      self.currentTree.collapseComponents()

    def OnCloseRulebook(self, event):
      closeRulesDialog = wxDialog(self, -1, "Close Rulebook", size=wxSize(350, 200),
                     style = wxCAPTION | wxSYSTEM_MENU | wxTHICK_FRAME)

      sizer = wxBoxSizer(wxVERTICAL)

      label = wxStaticText(closeRulesDialog, -1, "Select one or more Rulebooks to close")
      sizer.Add(label, 0, wxALIGN_CENTRE|wxALL, 5)

      # wxListBox to allow user to select rulebook to close
      rulebooks = self.ruleEditor.getRulebookNames()
      listBox = wxListBox(closeRulesDialog, 550, wxDefaultPosition, wxSize(85, -1),
                      rulebooks, wxLB_EXTENDED | wxLB_NEEDED_SB | wxLB_HSCROLL | wxLB_SORT )

      sizer.Add(listBox, 0, wxALIGN_CENTRE|wxALL, 5)

      box = wxBoxSizer(wxHORIZONTAL)
      btn = wxButton(closeRulesDialog, wxID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

      btn = wxButton(closeRulesDialog, wxID_CANCEL, " Cancel ")
      box.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)

      sizer.AddSizer(box, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5)

      closeRulesDialog.SetSizer(sizer)
      closeRulesDialog.SetAutoLayout(true)
      sizer.Fit(closeRulesDialog)

      val = closeRulesDialog.ShowModal()
      if val == wxID_OK:
        rulebookIdsToKill = listBox.GetSelections()  # returns a tuple of ints
        for rulebookId in rulebookIdsToKill:
          self.ruleEditor.removeRulebook(listBox.GetString(rulebookId))

    #---------------------------------------------

    # Help menu methods

    def OnPrintSocietyModelPlain(self, event):
      print self.currentTree.society.prettyPrintNamesOnly()

    def OnPrintSocietyModelXML(self, event):
      print self.currentTree.society.to_xml()

    def OnHelpAbout(self, event):
        from About import MyAboutBox
        about = MyAboutBox(self)
        about.ShowModal()
        about.Destroy()

    #---------------------------------------------
    def OnPageChange(self, event):
      self.currentPage = event.GetSelection()

      if self.currentPage == CSmarter.OVERVIEW:
        self.currentTree = None
        self.editMenu.Enable(CSmarter.SORT, false)
        self.mainmenu.Enable(CSmarter.FIND, false)
        self.mainmenu.Enable(CSmarter.FIND_NEXT, false)
        self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, False)
        self.enableRuleMenuItems(False)

      if self.currentPage == CSmarter.RULE_EDITOR:
        self.currentTree = None
        self.enableTreeViews(false)
        if self.societyOpen and self.ruleEditor.aRuleIsChecked:
          self.ruleEditor.applyRulesButton.Enable(true)
        else:
          self.ruleEditor.applyRulesButton.Enable(false)
        self.editMenu.Enable(CSmarter.SORT, false)
        self.mainmenu.Enable(CSmarter.FIND, false)
        self.mainmenu.Enable(CSmarter.FIND_NEXT, false)
        if self.openRulebookCount > 0:
          self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, True)
        else:
          self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, False)
        if self.ruleEditor.lb.GetSelection() >= 0:
          self.enableRuleMenuItems(True)

      elif self.currentPage == CSmarter.SOCIETY_EDITOR:
        self.currentTree = self.societyViewer
        if self.societyOpen:
          self.enableTreeViews(true)
          self.editMenu.Enable(CSmarter.CHANGE_NAMESERVER, true)
          if len(self.currentTree.GetSelections()) > 0:
            self.editMenu.Enable(CSmarter.SORT, True)
          else:
            self.editMenu.Enable(CSmarter.SORT, False)
          self.mainmenu.Enable(CSmarter.FIND, true)
          if len(self.searchLabel) > 0:
            self.mainmenu.Enable(CSmarter.FIND_NEXT, true)
        else:
          self.editMenu.Enable(CSmarter.SORT, False)
          self.mainmenu.Enable(CSmarter.FIND, False)
          self.mainmenu.Enable(CSmarter.FIND_NEXT, False)
        self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, False)
        self.enableRuleMenuItems(False)

      elif self.currentPage == CSmarter.AGENT_LAYDOWN:
        if self.agentLaydown.currentViewer is None:
          self.currentTree = self.laydownViewer
        else:
          self.currentTree = self.agentLaydown.currentViewer
        if self.currentTree is not None and len(self.currentTree.GetSelections()) > 0:
          self.editMenu.Enable(CSmarter.SORT, True)
        else:
          self.editMenu.Enable(CSmarter.SORT, False)
        if self.mappedSocietyOpen or self.agentSocietyOpen:
          self.mainmenu.Enable(CSmarter.FIND, true)
          if len(self.searchLabel) > 0:
            self.mainmenu.Enable(CSmarter.FIND_NEXT, true)
        else:
          self.mainmenu.Enable(CSmarter.FIND, false)
          self.mainmenu.Enable(CSmarter.FIND_NEXT, false)
        if self.mappedSocietyOpen:
          self.enableTreeViews(true)
          self.mainmenu.Enable(CSmarter.SHOW_COMPONENTS, false)
          self.mainmenu.Enable(CSmarter.COLLAPSE_COMPONENTS, false)
          self.mainmenu.Enable(CSmarter.COLLAPSE_AGENTS, false)
          if self.agentSocietyOpen:
            self.agentLaydown.setSpinnerValue()
            self.agentLaydown.distroAgentsButton.Enable(true)
        else:
          self.enableTreeViews(false)
        if self.editMenu.IsEnabled(CSmarter.CHANGE_NAMESERVER):
          self.editMenu.Enable(CSmarter.CHANGE_NAMESERVER, false)
        self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, False)
        self.enableRuleMenuItems(False)

    #---------------------------------------------

    def OnCloseWindow(self, event):
        self.window = None
        self.mainmenu = None
        if hasattr(self, "tbicon"):
            del self.tbicon
        self.logger.Close()
        self.Destroy()

    #---------------------------------------------

    def OnIdle(self, event):
        if self.otherWin:
            self.otherWin.Raise()
            self.window = self.otherWin
            self.otherWin = None

    #----------------------------------------------------------------------

    def openSocietyFile(self, parent, societyId):
      wildcard = "Society XML files (*.xml;*.XML)|*.xml;*.XML|All Files (*.*)|*.*"
      dlg = wxFileDialog(self, "Choose a society", "", "", wildcard, wxOPEN|wxMULTIPLE)
      try:
        if dlg.ShowModal() == wxID_OK:
          fileToOpen = dlg.GetPath()
          self.server = SocietyFactoryServer(fileToOpen, parent, self.log)
          self.server.Start()
          parent.StartAnimation()
          # store a reference to the filename to use when saving the file later
          if societyId == "mappedSociety":
            self.societyHnaFile = fileToOpen
            self.mappedSocietySaveCounter = 0
          elif societyId == "agentSociety":
            self.agentSocietyFile = fileToOpen
          elif societyId == "society":
            self.societyFile = fileToOpen
          elif societyId == "controller":
            self.controlFile = fileToOpen
      finally:
        dlg.Destroy()

    #----------------------------------------------------------------------

    def saveSociety(self, societyId):
      societyToSave = None
      destinationFile = None
      hnaSaveFlag = False
      if societyId == "mappedSociety":
        if self.agentLaydown.tempMappedSociety is not None:
          # There's a temp society in the undo buffer, so make it the new
          # mappedSociety and empty out the undo buffer.
          self.mappedSociety.close()
          self.mappedSociety = self.agentLaydown.tempMappedSociety
          self.agentLaydown.tempMappedSociety = None
          if len(self.undoBuffer) > 0:
            self.undoBuffer.pop()  # empty it out
          self.mainmenu.Enable(CSmarter.UNDO, false)
        societyToSave = self.mappedSociety
        # If this is the first time this society is being saved, prompt user for a file name;
        # i.e., this is a "save as".  For all subsequent saves, just save to same file.
        if self.mappedSocietySaveCounter > 0:
          destinationFile = self.societyHnaFile
        self.mappedSocietySaveCounter += 1
        hnaSaveFlag = True
      elif societyId == "agentSociety":
        # This society should never be saved
        societyToSave = self.agentSociety
      elif societyId == "society":
        societyToSave = self.society
        destinationFile = self.societyFile
      elif societyId == "controller":
        societyToSave = self.controlFile

      if societyToSave is not None:
        # Check for duplicate hosts, nodes, and agents
        dupeFound = self.checkForDuplicates(societyToSave)
        if dupeFound:
          return

        xml = ""
        if societyToSave == self.mappedSociety:
          #~ xml = self.laydownViewer.to_xml("agents")
          xml = self.laydownViewer.to_xml("argument")
          print"laydownViewer.to_xml", xml
        elif societyToSave == self.society:
          xml = societyToSave.to_xml(hnaSaveFlag)
        if xml.startswith('xxx'):  # indicates an error building the xml text
          return
        if destinationFile is None:
          wildcard = "Society XML files (*.xml;*.XML)|*.xml;*.XML|All Files (*.*)|*.*"
          dlg = wxFileDialog(self, "Choose a file to save", "", "", wildcard, wxOPEN|wxMULTIPLE)
          try:
            if dlg.ShowModal() == wxID_OK:
              destinationFile = dlg.GetPath()
          finally:
            dlg.Destroy()
            if societyToSave == self.mappedSociety:
              self.societyHnaFile = destinationFile
            elif societyToSave == self.society:
              self.societyFile = destinationFile

        societyToSave.isDirty = False
        if destinationFile is not None:
          self.save_society(xml, destinationFile)
      else:
        self.log.WriteText("Unable to save empty or unknown society.")

    #----------------------------------------------------------------------

    def save_society(self, xml, destinationFile):
      saveFile = open(destinationFile, 'w')
      saveFile.write(xml)
      saveFile.close()
      self.log.WriteText("Society saved in file %s\n" % destinationFile)

    #------------------------------------------------------------------

    def checkForDuplicates(self, society):
      entityTypes = ["host", "node", "agent"]
      for type in entityTypes:
        dupeCheckDict = {}
        for entity in society.each_entity(type):
          if dupeCheckDict.has_key(entity.name):
            self.displayDupeMessage(type, entity.name)
            return True
          dupeCheckDict[entity.name] = 1
      return False

    #------------------------------------------------------------------

    def displayDupeMessage(self, entityType, dupeName):
      msg = "Duplicate " + entityType + " found: " + dupeName
      dlg = CougaarMessageDialog(self, "error", msg)
      dlg.display()

    #------------------------------------------------------------------

    def closeSociety(self, societyId):
      societyToClose = None
      currentViewer = None
      saveAgents = True
      if societyId != "agentSociety":
        if societyId == "mappedSociety":
          societyToClose = self.mappedSociety
          currentViewer = self.laydownViewer
        elif societyId == "society":
          societyToClose = self.society
          currentViewer = self.societyViewer
          saveAgents = False
        if societyToClose.isDirty:
          # First give user a chance to save the society
          dlg = CougaarMessageDialog(self, "confirm")
          disposition = dlg.getUserInput()
          if disposition == wxID_CANCEL:
            return
          if disposition == wxID_YES:
            self.saveSociety(societyId)

        # Now delete the tree display
        currentViewer.DeleteAllItems()
        # Finally, delete the society object in memory
        if societyToClose is not None:  # shouldn't ever be None...but it sometimes is!
          societyToClose.close(saveAgents)
          societyToClose = None
        if societyId == "mappedSociety":
          self.mappedSociety = None
          self.mappedSocietyOpen = 0
          self.societyHnaFile = None
          self.enableHnaSaveMenuItems(false)
          if not self.agentSocietyOpen:
            self.editMenu.Enable(CSmarter.SORT, false)
        elif societyId == "society":
          self.society = None
          self.societyOpen = 0
          self.societyFile = None
          self.ruleEditor.societyName.SetValue("")
          self.nameServer = None
          self.enableSocietySaveMenuItems(false)
          if not self.mappedSocietyOpen:
            self.editMenu.Enable(CSmarter.SORT, false)
        elif societyId == "controller":
          print "Controller File"

      else:  # societyId == "agentSociety"
        if self.agentViewer is not None:
          self.agentViewer.DeleteAllItems()  # delete the tree
        if self.agentSociety is not None:  # shouldn't ever be None...but it sometimes is!
          # Delete the society object in memory
          self.agentSociety.close()
          self.agentSociety = None
        self.agentSocietyOpen = 0
        self.agentSocietyFile = None
        if len(self.undoBuffer) > 0:
          self.undoBuffer.pop()  # empty it out
        self.mainmenu.Enable(CSmarter.UNDO, false)
        self.enableAgentSocietySaveMenuItems(false)
        if not self.mappedSocietyOpen:
          self.editMenu.Enable(CSmarter.SORT, false)

    #------------------------------------------------------------------

    def enableRuleSaveMenuItems(self, enable=true):
      self.mainmenu.Enable(CSmarter.SAVE_RULE, enable)
      self.mainmenu.Enable(CSmarter.SAVE_AS_RULE, enable)
      self.ruleEditor.saveRuleButton.Enable(enable)

    #---------------------------------------------

    def enableRuleSaveAs(self, enable=true):
      self.mainmenu.Enable(CSmarter.SAVE_AS_RULE, enable)

    #---------------------------------------------

    def enableSocietySaveMenuItems(self, enable=true):
      self.mainmenu.Enable(CSmarter.SAVE_SOCIETY, enable)
      self.mainmenu.Enable(CSmarter.SAVE_AS_SOCIETY, enable)
      self.mainmenu.Enable(CSmarter.CHANGE_NAMESERVER, enable)
      self.mainmenu.Enable(CSmarter.FIND, enable)
      #~ if enable and len(self.searchLabel) > 0:
      self.mainmenu.Enable(CSmarter.FIND_NEXT, False)
      self.ruleEditor.saveSocietyButton.Enable(enable)
      self.ruleEditor.openSocietyButton.Enable(not enable)
      self.societyEditor.saveSocietyButton.Enable(enable)
      self.societyEditor.openSocietyButton.Enable(not enable)
      self.societyEditor.closeSocietyButton.Enable(enable)
      if self.currentPage == CSmarter.SOCIETY_EDITOR:
        self.enableTreeViews(enable)

    #---------------------------------------------

    def enableAgentSocietySaveMenuItems(self, enable=true):
      self.agentLaydown.openAgentListButton.Enable(not enable)
      self.agentLaydown.closeAgentSocietyButton.Enable(enable)
      self.mainmenu.Enable(CSmarter.FIND, enable)
      self.mainmenu.Enable(CSmarter.FIND_NEXT, False)

    #---------------------------------------------

    def enableHnaSaveMenuItems(self, enable=true):
      self.mainmenu.Enable(CSmarter.SAVE_AS_HNA_SOCIETY, enable)
      self.agentLaydown.saveHnaButton.Enable(enable)
      self.agentLaydown.openHnaButton.Enable(not enable)
      self.agentLaydown.closeHnaButton.Enable(enable)
      self.societyEditor.getHnaMapButton.Enable(enable)
      self.enableTreeViews(enable)
      self.mainmenu.Enable(CSmarter.SHOW_COMPONENTS, false)
      self.mainmenu.Enable(CSmarter.COLLAPSE_COMPONENTS, false)
      self.mainmenu.Enable(CSmarter.COLLAPSE_AGENTS, false)
      self.mainmenu.Enable(CSmarter.FIND, enable)
      self.mainmenu.Enable(CSmarter.FIND_NEXT, False)

    #---------------------------------------------

    def enableTreeViews(self, enable=true):
      self.mainmenu.Enable(CSmarter.SHOW_SOCIETY, enable)
      self.mainmenu.Enable(CSmarter.SHOW_NODES, enable)
      self.mainmenu.Enable(CSmarter.SHOW_AGENTS, enable)
      self.mainmenu.Enable(CSmarter.SHOW_COMPONENTS, enable)
      self.mainmenu.Enable(CSmarter.COLLAPSE_HOSTS, enable)
      self.mainmenu.Enable(CSmarter.COLLAPSE_NODES, enable)
      self.mainmenu.Enable(CSmarter.COLLAPSE_AGENTS, enable)
      self.mainmenu.Enable(CSmarter.COLLAPSE_COMPONENTS, enable)

    #---------------------------------------------

    ##
    # Enables or disables the 'Close Rulebook' View menu item depending on
    # whether or not there are any open rulebooks.
    # isRulebookAdded:: [boolean] If True, a rulebook has been added;
    #                                                 If False, a rulebook has been removed
    #
    def updateCloseRulebookMenuItem(self, isRulebookAdded):
      if isRulebookAdded:
        self.openRulebookCount += 1
      else:
        self.openRulebookCount -= 1
      actionFlag = False
      if self.openRulebookCount > 0:
        actionFlag = True
      self.viewMenu.Enable(CSmarter.CLOSE_RULEBOOK, actionFlag)

    #---------------------------------------------

    def enableRuleMenuItems(self, enable=True):
      self.editMenu.Enable(CSmarter.DELETE_RULE, enable)
      self.editMenu.Enable(CSmarter.RENAME_RULE, enable)

    #---------------------------------------------

    def enableFindNextMenuItem(self, enable=True):
      self.mainmenu.Enable(CSmarter.FIND_NEXT, enable)

    #---------------------------------------------

    def setDragSource(self, viewer):
      self.dragSource = viewer

    #---------------------------------------------

    def getDragSource(self):
      return self.dragSource

    #---------------------------------------------

    def ShowTip(self):
        try:
            showTipText = open(opj("data/showTips")).read()
            showTip, index = eval(showTipText)
        except IOError:
            showTip, index = (1, 0)
        if showTip:
            tp = wxCreateFileTipProvider(opj("data/tips.txt"), index)
            ##tp = MyTP(0)
            showTip = wxShowTip(self, tp)
            index = tp.GetCurrentTip()
            open(opj("data/showTips"), "w").write(str( (showTip, index) ))

    #---------------------------------------------
    def OnTaskBarActivate(self, evt):
        if self.IsIconized():
            self.Iconize(false)
        if not self.IsShown():
            self.Show(true)
        self.Raise()

    #---------------------------------------------

    TBMENU_RESTORE = 1000
    TBMENU_CLOSE   = 1001

    def OnTaskBarMenu(self, evt):
        menu = wxMenu()
        menu.Append(self.TBMENU_RESTORE, "Restore CS03")
        menu.Append(self.TBMENU_CLOSE,   "Close")
        self.tbicon.PopupMenu(menu)
        menu.Destroy()

    #---------------------------------------------
    def OnTaskBarClose(self, evt):
        self.Close()

        # because of the way wxTaskBarIcon.PopupMenu is implemented we have to
        # prod the main idle handler a bit to get the window to actually close
        wxGetApp().ProcessIdle()


    #---------------------------------------------
    def OnIconfiy(self, evt):
        wxLogMessage("OnIconfiy")
        evt.Skip()

    #---------------------------------------------
    def OnMaximize(self, evt):
        wxLogMessage("OnMaximize")
        evt.Skip()




#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

class MySplashScreen(wxSplashScreen):
  def __init__(self, initPane=1):
      self.initPane = initPane # specifies the wxNotebook tabbed pane to be shown initially
      bmp = wxImage(opj("bitmaps/ACME2003.gif")).ConvertToBitmap()
      wxSplashScreen.__init__(self, bmp,
                              wxSPLASH_CENTRE_ON_SCREEN|wxSPLASH_TIMEOUT,
                              500, None, -1,
                              style = wxSIMPLE_BORDER|wxFRAME_NO_TASKBAR|wxSTAY_ON_TOP)
      EVT_CLOSE(self, self.OnClose)

  def OnClose(self, evt):
    frame = CSmarter(None, -1, "Agent Workbench", 710, self.initPane)
    frame.Show(true)
    evt.Skip()  # Make sure the default handler runs too...


class MyApp(wxApp):
    def OnInit(self):
        """
        Create and show the splash screen.  It will then create and show
        the main frame when it is time to do so.
        """
        initPane = 3
        if len(sys.argv) > 1:
          initPane = int(sys.argv[1])
        wxInitAllImageHandlers()
        splash = MySplashScreen(initPane)
        splash.Show()
        return true



#---------------------------------------------------------------------------

def main():
    try:
        demoPath = os.path.dirname(__file__)
        os.chdir(demoPath)
    except:
        pass
    app = MyApp(wxPlatform == "__WXMAC__")
    app.MainLoop()


#---------------------------------------------------------------------------

overview = """<html><body>
 <h2>CSMARTer</h2>
CSMARTer is a consolidator for several Cougaar society functions which can either be done graphically or via
scripting.  A capabilities overview is presented here; for more detailed information, please see the README file.
 <p>
 <h2>Rules</h2>
 Use the Rules tool to create new or edit existing rules and apply those rules to a society.  Steps:<br>
 <ul>
 <li>Click on Set RuleBook and select the directory that contains the rules you want to manage.</li>
 <li>Select a rule in the rule select box to display the rule text in the text box for review and/or editing.</li>
 <li>Open the society to which you want to apply these rules</li>
 <li>Check a rule to mark it for later application to the society.</li>
 <li>When all desired rules have been checked, click Apply Rules to apply the checked rules to the society.</li>
 <li>Click Save Society to make the society changes permanent.</li>
 </ul>
 <p>
 <h2>Society Editor</h2>
 Use the Society Editor to view or manually edit a society.  When viewing a society, changes just made by applying
 a rule (from the Rule Editor) are highlighted in cyan.  To manually edit the society, select an item by left clicking
 on it, then left click again to change its name and/or value, or right click to view a menu from which adds, deletes,
 and changes can be made.
 <p>
 <h2>Agent Laydown</h2>
 Use the Agent Laydown to allocate agents (from a list of agents) to hosts (from a list of hosts).  The allocation can
 be done automatically by distributing the agents evenly among the hosts or by specifying the number of agents to
 put on each host, or it can be done manually by dragging and dropping agents and/or nodes from the agent list to
 hosts on the host list.  There are capabilities for quickly creating societies and for adding/removing/editing facets.
 When society manipulation is complete, the new or revised society can be saved to an XML file.  Agent Laydown
 does not permit working with society entities below the Agent level, but for operations at or above that level,
 Agent Laydown is more versatile than Society Editor.
 </body></html>
 """

#----------------------------------------------------------------------------

if __name__ == '__main__':
  main()
