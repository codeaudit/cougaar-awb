#!/bin/env python
#----------------------------------------------------------------------------
# Name:         CS03.py
# Purpose:      AWB umbrella
#
# Author:       ISAT (D. Moore
#
# RCS-ID:       $Id: AWB.py,v 1.6 2004-11-22 18:44:12 damoore Exp $
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

import sys, os, time
import wx # from   wxPython.wx import *
import wx.html as html # from   wxPython.html import wxHtmlWindow
from societyBuilder import SocietyBuilderPanel
from agentLaydown import AgentLaydownPanel
from societyEditor import SocietyEditorPanel
from insertion_dialog import CougaarMessageDialog
from insertion_dialog import FindItemDialog
from societyFactoryServer import SocietyFactoryServer
from agentController import AgentControllerViewer
from ACMEPy.node import Node
import images

#---------------------------------------------------------------------------

class MyLog(wx.PyLog):
    def __init__(self, textCtrl, logTime=0):
        wx.PyLog.__init__(self)
        self.tc = textCtrl
        self.logTime = logTime
        self.logFile = open('AWB.log', 'w')

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

class MyTP(wx.PyTipProvider):
    def GetTip(self):
        return "This is my tip"

#---------------------------------------------------------------------------

def opj(path):
    """Convert paths to the platform-specific separator"""
    return apply(os.path.join, tuple(path.split('/')))


#---------------------------------------------------------------------------

class AWB(wx.Frame):
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
      wx.Frame.__init__(self, parent, -1, title, size = (800, initHeight),
                       style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

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
      self.agentControllerViewer = None  # wxTreeCtrl for displaying initial agent list in Agent Laydown tab
      self.laydownViewer = None  # wxTreeCtrl for displaying host-node-agent laydown
      self.societyOpen = False  # for the Society Editor
      self.agentSocietyOpen = False  # for the Agent List in Agent Laydown tab
      self.mappedSocietyOpen = False  # for the HNA Map in Agent Laydown tab
      self.societyFile = None  # string name of xml file for self.society
      self.agentSocietyFile = None  # string name of xml file for self.agentSociety
      self.societyHnaFile = None  # string name of xml file for self.mappedSociety
      self.controlFile = None # string name of xml file for self.controlFile
      self.ruleOpen = False
      self.ruleApplied = False
      self.currentPage = AWB.RULE_EDITOR
      self.currentTree = None
      self.undoBuffer = []
      self.rulebookId = AWB.CLOSE_RULEBOOK * 10

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
        if wx.Platform == '__WXMSW__':
            # setup a taskbar icon, and catch some events from it
            self.tbicon = wx.TaskBarIcon()
            self.tbicon.SetIcon(icon, "CS03")
            
            
            wx.EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.OnTaskBarActivate)
            wx.EVT_TASKBAR_RIGHT_UP(self.tbicon, self.OnTaskBarMenu)
            wx.EVT_MENU(self.tbicon, self.TBMENU_RESTORE, self.OnTaskBarActivate)
            wx.EVT_MENU(self.tbicon, self.TBMENU_CLOSE, self.OnTaskBarClose)

        wx.CallAfter(self.ShowTip)

        self.otherWin = None
        wx.EVT_IDLE(self, self.OnIdle)
        wx.EVT_CLOSE(self, self.OnCloseWindow)
        wx.EVT_ICONIZE(self, self.OnIconfiy)
        wx.EVT_MAXIMIZE(self, self.OnMaximize)

        self.Centre(wx.BOTH)
        self.CreateStatusBar(1, wx.ST_SIZEGRIP)

        splitterId = wx.NewId()
        self.splitter2 = wx.SplitterWindow(self, splitterId, style=wx.NO_3D|wx.SP_3D)
        wx.EVT_SIZE(self, self.OnSplitterResize)

        def EmptyHandler(evt):
          pass

        wx.EVT_ERASE_BACKGROUND(self.splitter2, EmptyHandler)

        #---------------------------------------------------------------------------

        # Make a File menu
        self.mainmenu = wx.MenuBar()
        fileMenu = wx.Menu()

        fileMenu.Append(AWB.SAVE_RULE, 'Save &Rule\tCtrl+R', 'Save an existing rule')
        wx.EVT_MENU(self, AWB.SAVE_RULE, self.OnRuleSave)

        fileMenu.Append(AWB.SAVE_AS_RULE, 'Save R&ule As...\tAlt+R', 'Save as a new rule')
        wx.EVT_MENU(self, AWB.SAVE_AS_RULE, self.OnRuleSaveAs)

        fileMenu.Append(AWB.SAVE_SOCIETY, '&Save Society\tCtrl+S', 'Save an existing society')
        wx.EVT_MENU(self, AWB.SAVE_SOCIETY, self.OnSocietySave)

        fileMenu.Append(AWB.SAVE_AS_SOCIETY, 'Save Society &As...\tAlt+S', 'Save as a new society')
        wx.EVT_MENU(self, AWB.SAVE_AS_SOCIETY, self.OnSocietySaveAs)

        fileMenu.Append(AWB.SAVE_AS_HNA_SOCIETY, 'Save HNA &Map As...\tAlt+M', 'Save as a new society')
        wx.EVT_MENU(self, AWB.SAVE_AS_HNA_SOCIETY, self.OnHnaMapSaveAs)

        exitID = wx.NewId()
        fileMenu.Append(exitID, 'E&xit\tAlt+X', 'Get the heck outta here!')
        wx.EVT_MENU(self, exitID, self.OnFileExit)

        if not self.ruleOpen:
          fileMenu.Enable(AWB.SAVE_RULE, False)
          fileMenu.Enable(AWB.SAVE_AS_RULE, False)
        if not self.societyOpen:
          fileMenu.Enable(AWB.SAVE_SOCIETY, False)
          fileMenu.Enable(AWB.SAVE_AS_SOCIETY, False)
        if not self.mappedSocietyOpen:
          fileMenu.Enable(AWB.SAVE_AS_HNA_SOCIETY, False)

        self.mainmenu.Append(fileMenu, '&File')

        #---------------------------------------------------------------------------

        # Make an Edit menu
        self.editMenu = wx.Menu()

        self.editMenu.Append(AWB.UNDO, '&Undo\tCtrl+Z', 'Undo last edit')
        wx.EVT_MENU(self, AWB.UNDO, self.OnUndo)
        self.editMenu.Enable(AWB.UNDO, False)

        self.editMenu.Append(AWB.SORT, '&Sort selected item', 'Sort entities in selected item')
        wx.EVT_MENU(self, AWB.SORT, self.OnSort)
        self.editMenu.Enable(AWB.SORT, False)

        self.editMenu.Append(AWB.CHANGE_NAMESERVER, 'Change &name server', 'Specify a new name server')
        wx.EVT_MENU(self, AWB.CHANGE_NAMESERVER, self.OnChangeNameServer)
        self.editMenu.Enable(AWB.CHANGE_NAMESERVER, False)

        self.editMenu.Append(AWB.FIND, '&Find\tCtrl+F', 'Find a specific society entity by name')
        wx.EVT_MENU(self, AWB.FIND, self.OnFind)
        self.editMenu.Enable(AWB.FIND, False)

        self.editMenu.Append(AWB.FIND_NEXT, 'Find &Next\tF3', 'Find the next occurrence of a specific society entity by name')
        wx.EVT_MENU(self, AWB.FIND_NEXT, self.OnFindNext)
        self.editMenu.Enable(AWB.FIND_NEXT, False)

        self.editMenu.Append(AWB.RENAME_RULE, '&Rename Rule\tCtrl+R', 'Rename a society transformation rule')
        wx.EVT_MENU(self, AWB.RENAME_RULE, self.OnRenameRule)
        self.editMenu.Enable(AWB.RENAME_RULE, False)

        self.editMenu.Append(AWB.DELETE_RULE, '&Delete Rule\tAlt+D', 'Delete a society transformation rule')
        wx.EVT_MENU(self, AWB.DELETE_RULE, self.OnDeleteRule)
        self.editMenu.Enable(AWB.DELETE_RULE, False)

        self.mainmenu.Append(self.editMenu, '&Edit')

        #---------------------------------------------------------------------------

        # Make an View menu
        self.viewMenu = wx.Menu()

        self.viewMenu.Append(AWB.SHOW_SOCIETY, 'Show &Entire Society\tCtrl+E', 'Expand entire Society tree')
        wx.EVT_MENU(self, AWB.SHOW_SOCIETY, self.OnShowSociety)

        self.viewMenu.Append(AWB.SHOW_NODES, 'Show All &Nodes\tCtrl+N', 'Show All Nodes')
        wx.EVT_MENU(self, AWB.SHOW_NODES, self.OnShowNodes)

        self.viewMenu.Append(AWB.SHOW_AGENTS, 'Show All &Agents\tCtrl+A', 'Show All Agents')
        wx.EVT_MENU(self, AWB.SHOW_AGENTS, self.OnShowAgents)

        self.viewMenu.Append(AWB.SHOW_COMPONENTS, 'Show All &Components\tCtrl+C', 'Show All Components')
        wx.EVT_MENU(self, AWB.SHOW_COMPONENTS, self.OnShowComponents)

        self.viewMenu.Append(AWB.COLLAPSE_HOSTS, 'Collapse To &Hosts\tAlt+O', 'Collapse To Hosts')
        wx.EVT_MENU(self, AWB.COLLAPSE_HOSTS, self.OnCollapseHosts)

        self.viewMenu.Append(AWB.COLLAPSE_NODES, 'Collapse To &Nodes\tAlt+N', 'Collapse To Nodes')
        wx.EVT_MENU(self, AWB.COLLAPSE_NODES, self.OnCollapseNodes)

        self.viewMenu.Append(AWB.COLLAPSE_AGENTS, 'Collapse To &Agents\tAlt+A', 'Collapse To Agents')
        wx.EVT_MENU(self, AWB.COLLAPSE_AGENTS, self.OnCollapseAgents)

        self.viewMenu.Append(AWB.COLLAPSE_COMPONENTS, 'Collapse To &Components\tAlt+C', 'Collapse To Components')
        wx.EVT_MENU(self, AWB.COLLAPSE_COMPONENTS, self.OnCollapseComponents)

        self.viewMenu.AppendSeparator()

        helpText = "Removes rules belonging to the chosen rulebook from the Rulebook window"
        self.viewMenu.Append(AWB.CLOSE_RULEBOOK, "Close RuleBook\tCtrl+B", helpText)
        wx.EVT_MENU(self, AWB.CLOSE_RULEBOOK, self.OnCloseRulebook)

        self.viewMenu.Enable(AWB.SHOW_SOCIETY, False)
        self.viewMenu.Enable(AWB.SHOW_NODES, False)
        self.viewMenu.Enable(AWB.SHOW_AGENTS, False)
        self.viewMenu.Enable(AWB.SHOW_COMPONENTS, False)
        self.viewMenu.Enable(AWB.COLLAPSE_HOSTS, False)
        self.viewMenu.Enable(AWB.COLLAPSE_NODES, False)
        self.viewMenu.Enable(AWB.COLLAPSE_AGENTS, False)
        self.viewMenu.Enable(AWB.COLLAPSE_COMPONENTS, False)
        self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, False)

        self.mainmenu.Append(self.viewMenu, '&View')

        #---------------------------------------------------------------------------

        # Make a Help menu
        helpMenu = wx.Menu()

        debugMenu = wx.Menu()

        printSocModelId = wx.NewId()
        debugMenu.Append(printSocModelId, 'Print society model (plain text)\tF11', 'Print plain text to console window.')
        wx.EVT_MENU(self, printSocModelId, self.OnPrintSocietyModelPlain)

        printSocModelXmlId = wx.NewId()
        debugMenu.Append(printSocModelXmlId, 'Print society model (XML)\tF12', 'Print XML text to console window.')
        wx.EVT_MENU(self, printSocModelXmlId, self.OnPrintSocietyModelXML)

        debugId = wx.NewId()
        helpMenu.AppendMenu(debugId, "Debug", debugMenu)

        helpId = wx.NewId()
        helpMenu.Append(helpId, '&About\tF1', 'wxPython RULES!!!')
        wx.EVT_MENU(self, helpId, self.OnHelpAbout)

        self.mainmenu.Append(helpMenu, '&Help')

        #---------------------------------------------------------------------------

        self.SetMenuBar(self.mainmenu)

        # set the menu accellerator table...
        aTable = wx.AcceleratorTable([(wx.ACCEL_ALT,  ord('X'), exitID),
                                     (wx.ACCEL_CTRL, ord('H'), helpId)])
        self.SetAcceleratorTable(aTable)

        #---------------------------------------------------------------------------


        # Create a Notebook to go in top of wxSplitterWindow
        self.nb = wx.Notebook(self.splitter2, -1, style=wx.CLIP_CHILDREN)
        wx.EVT_NOTEBOOK_PAGE_CHANGED(self, -1, self.OnPageChange)

        # Set up a log on the View Log Notebook page to go in bottom of wxSplitter Window
        self.log = wx.TextCtrl(self.splitter2, -1,
                              style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # Set the wxWindows log target to be this textctrl
        #wxLog_SetActiveTarget(wxLogTextCtrl(self.log))

        # But instead of the above we want to show how to use our own wxLog class
        self.logger = MyLog(self.log)
        wx.Log_SetActiveTarget(self.logger)

        #~ wxLogChain(wxLogStderr())
        #~ wxLogChain(self.logger)

        #~ wxLog_SetLogLevel(wxLOG_Warning)
        wx.Log_SetLogLevel(wx.LOG_Message)

        # for serious debugging
        #wxLog_SetActiveTarget(wxLogStderr())
        #wxLog_SetTraceMask(wxTraceMessages)

        # Notebook page 0:  AWB Overview
        if 0:  # the old way
            self.ovr = html.HtmlWindow(self.nb, -1, size=(400, 400))
            self.nb.AddPage(self.ovr, self.overviewText)

        else:  # hopefully I can remove this hacky code soon, see bug #216861
            panel = wx.Panel(self.nb, -1, style=wx.CLIP_CHILDREN)
            self.ovr = html.HtmlWindow(panel, -1, size=(400, 400))
            self.nb.AddPage(panel, self.overviewText)

            def OnOvrSize(evt, ovr=self.ovr):
                ovr.SetSize(evt.GetSize())

            wx.EVT_SIZE(panel, OnOvrSize)
            wx.EVT_ERASE_BACKGROUND(panel, EmptyHandler)

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
        self.agentControllerViewer = AgentControllerViewer(self.nb, self, self.log)
        self.nb.AddPage(self.agentControllerViewer, 'Agent Viewer')

        self.Show(True)

        # add the windows to the splitter and split it.
        self.splitter2.SplitHorizontally(self.nb, self.log, 560)
        self.splitter2.SetMinimumPaneSize(20)

        # select initial items
        self.nb.SetSelection(self.initialPane)

        #wxLogMessage('window handle: %s' % self.GetHandle())
        wx.LogMessage('AWB initialized.')

      except Exception:
        import traceback
        traceback.print_exc()

    #---------------------------------------------
    def WriteText(self, text):
        if text[-1:] == '\n':
            text = text[:-1]
        wx.LogMessage(text)

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
      self.mainmenu.Enable(AWB.UNDO, False)

    def OnSort(self, event):
      if self.currentPage == AWB.AGENT_LAYDOWN:
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
      self.win = wx.Dialog(self, -1, "Change name server", size=wx.Size(350, 200),
                     style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

      sizer = wx.BoxSizer(wx.VERTICAL)

      label = wx.StaticText(self.win, -1, "Select a new name server")
      sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      ### ------------------------------------

      textBox = wx.BoxSizer(wx.HORIZONTAL)

      hostLabel = wx.StaticText(self.win, -1, "Host:")
      textBox.Add(hostLabel, 0, wx.ALIGN_CENTRE)

      hostList = []
      for host in self.society.each_host():
        hostList.append(host.name)
      value = self.society.nameserver_host
      if len(hostList) == 0:
        hostList.append(value)

      self.cb = wx.ComboBox(self.win, 500, value, wx.DefaultPosition, wx.Size(65, -1),
                      hostList, wx.CB_DROPDOWN | wx.CB_READONLY)
      wx.EVT_COMBOBOX(self, 500, self.EvtComboBox)
      wx.EVT_TEXT_ENTER(self, 500, self.EvtTextEnter)
      textBox.Add(self.cb, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

      portLabel = wx.StaticText(self.win, -1, "Ports:")
      textBox.Add(portLabel, 0, wx.ALIGN_CENTRE | wx.LEFT, 5)

      portValue = self.society.nameserver_suffix
      self.portText = wx.TextCtrl(self.win, 505, portValue, wx.DefaultPosition, wx.Size(75, -1))
      textBox.Add(self.portText, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

      sizer.AddSizer(textBox, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

      ### ------------------------------------

      box = wx.BoxSizer(wx.HORIZONTAL)
      btn = wx.Button(self.win, wx.ID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      btn = wx.Button(self.win, wx.ID_CANCEL, " Cancel ")
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      sizer.AddSizer(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

      self.win.SetSizer(sizer)
      self.win.SetAutoLayout(True)
      sizer.Fit(self.win)

      val = self.win.ShowModal()
      if val == wx.ID_OK:
        self.society.set_nameserver(self.cb.GetValue() + self.portText.GetValue())
        #Now change the nameserver parameter in each node in the society:
        for node in self.society.each_node():
          node.updateNameServerParam(self.society.get_nameserver())

    def OnFind(self, event):
      showViewerRadio = (self.currentPage == AWB.AGENT_LAYDOWN)
      FindItemDialog(self, showViewerRadio)
      if len(self.searchLabel) > 0:
        self.currentTree.findItem(self.searchLabel, self.caseSearchDesired)
        #~ self.mainmenu.Enable(AWB.FIND_NEXT, True)

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
      closeRulesDialog = wx.Dialog(self, -1, "Close Rulebook", size=wx.Size(350, 200),
                     style = wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME)

      sizer = wx.BoxSizer(wx.VERTICAL)

      label = wx.StaticText(closeRulesDialog, -1, "Select one or more Rulebooks to close")
      sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      # wxListBox to allow user to select rulebook to close
      rulebooks = self.ruleEditor.getRulebookNames()
      listBox = wx.ListBox(closeRulesDialog, 550, wx.DefaultPosition, wx.Size(85, -1),
                      rulebooks, wx.LB_EXTENDED | wx.LB_NEEDED_SB | wx.LB_HSCROLL | wx.LB_SORT )

      sizer.Add(listBox, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      box = wx.BoxSizer(wx.HORIZONTAL)
      btn = wx.Button(closeRulesDialog, wx.ID_OK, " OK ")
      btn.SetDefault()
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      btn = wx.Button(closeRulesDialog, wx.ID_CANCEL, " Cancel ")
      box.Add(btn, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

      sizer.AddSizer(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

      closeRulesDialog.SetSizer(sizer)
      closeRulesDialog.SetAutoLayout(True)
      sizer.Fit(closeRulesDialog)

      val = closeRulesDialog.ShowModal()
      if val == wx.ID_OK:
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

      if self.currentPage == AWB.OVERVIEW:
        self.currentTree = None
        self.editMenu.Enable(AWB.SORT, False)
        self.mainmenu.Enable(AWB.FIND, False)
        self.mainmenu.Enable(AWB.FIND_NEXT, False)
        self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, False)
        self.enableRuleMenuItems(False)

      if self.currentPage == AWB.RULE_EDITOR:
        self.currentTree = None
        self.enableTreeViews(False)
        if self.societyOpen and self.ruleEditor.aRuleIsChecked:
          self.ruleEditor.applyRulesButton.Enable(True)
        else:
          self.ruleEditor.applyRulesButton.Enable(False)
        self.editMenu.Enable(AWB.SORT, False)
        self.mainmenu.Enable(AWB.FIND, False)
        self.mainmenu.Enable(AWB.FIND_NEXT, False)
        if self.openRulebookCount > 0:
          self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, True)
        else:
          self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, False)
        if self.ruleEditor.lb.GetSelection() >= 0:
          self.enableRuleMenuItems(True)

      elif self.currentPage == AWB.SOCIETY_EDITOR:
        self.currentTree = self.societyViewer
        if self.societyOpen:
          self.enableTreeViews(True)
          self.editMenu.Enable(AWB.CHANGE_NAMESERVER, True)
          if len(self.currentTree.GetSelections()) > 0:
            self.editMenu.Enable(AWB.SORT, True)
          else:
            self.editMenu.Enable(AWB.SORT, False)
          self.mainmenu.Enable(AWB.FIND, True)
          if len(self.searchLabel) > 0:
            self.mainmenu.Enable(AWB.FIND_NEXT, True)
        else:
          self.editMenu.Enable(AWB.SORT, False)
          self.mainmenu.Enable(AWB.FIND, False)
          self.mainmenu.Enable(AWB.FIND_NEXT, False)
        self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, False)
        self.enableRuleMenuItems(False)

      elif self.currentPage == AWB.AGENT_LAYDOWN:
        if self.agentLaydown.currentViewer is None:
          self.currentTree = self.laydownViewer
        else:
          self.currentTree = self.agentLaydown.currentViewer
        if self.currentTree is not None: # and len(self.currentTree.GetSelections()) > 0:
          self.editMenu.Enable(AWB.SORT, True)
        else:
          self.editMenu.Enable(AWB.SORT, False)
        if self.mappedSocietyOpen or self.agentSocietyOpen:
          self.mainmenu.Enable(AWB.FIND, True)
          if len(self.searchLabel) > 0:
            self.mainmenu.Enable(AWB.FIND_NEXT, True)
        else:
          self.mainmenu.Enable(AWB.FIND, False)
          self.mainmenu.Enable(AWB.FIND_NEXT, False)
        if self.mappedSocietyOpen:
          self.enableTreeViews(True)
          self.mainmenu.Enable(AWB.SHOW_COMPONENTS, False)
          self.mainmenu.Enable(AWB.COLLAPSE_COMPONENTS, False)
          self.mainmenu.Enable(AWB.COLLAPSE_AGENTS, False)
          if self.agentSocietyOpen:
            self.agentLaydown.setSpinnerValue()
            self.agentLaydown.distroAgentsButton.Enable(True)
        else:
          self.enableTreeViews(False)
        if self.editMenu.IsEnabled(AWB.CHANGE_NAMESERVER):
          self.editMenu.Enable(AWB.CHANGE_NAMESERVER, False)
        self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, False)
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
      dlg = wx.FileDialog(self, "Choose a society", "", "", wildcard, wx.OPEN|wx.MULTIPLE)
      try:
        if dlg.ShowModal() == wx.ID_OK:
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
          self.mainmenu.Enable(AWB.UNDO, False)
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
          dlg = wx.FileDialog(self, "Choose a file to save", "", "", wildcard, wx.OPEN|wx.MULTIPLE)
          try:
            if dlg.ShowModal() == wx.ID_OK:
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
          if disposition == wx.ID_CANCEL:
            return
          if disposition == wx.ID_YES:
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
          self.enableHnaSaveMenuItems(False)
          if not self.agentSocietyOpen:
            self.editMenu.Enable(AWB.SORT, False)
        elif societyId == "society":
          self.society = None
          self.societyOpen = 0
          self.societyFile = None
          self.ruleEditor.societyName.SetValue("")
          self.nameServer = None
          self.enableSocietySaveMenuItems(False)
          if not self.mappedSocietyOpen:
            self.editMenu.Enable(AWB.SORT, False)
        elif societyId == "controller":
          print "Controller File"

      else:  # societyId == "agentSociety"
        if self.agentControllerViewer is not None:
          self.agentControllerViewer.DeleteAllItems()  # delete the tree
        if self.agentSociety is not None:  # shouldn't ever be None...but it sometimes is!
          # Delete the society object in memory
          self.agentSociety.close()
          self.agentSociety = None
        self.agentSocietyOpen = 0
        self.agentSocietyFile = None
        if len(self.undoBuffer) > 0:
          self.undoBuffer.pop()  # empty it out
        self.mainmenu.Enable(AWB.UNDO, False)
        self.enableAgentSocietySaveMenuItems(False)
        if not self.mappedSocietyOpen:
          self.editMenu.Enable(AWB.SORT, False)

    #------------------------------------------------------------------

    def enableRuleSaveMenuItems(self, enable=True):
      self.mainmenu.Enable(AWB.SAVE_RULE, enable)
      self.mainmenu.Enable(AWB.SAVE_AS_RULE, enable)
      self.ruleEditor.saveRuleButton.Enable(enable)

    #---------------------------------------------

    def enableRuleSaveAs(self, enable=True):
      self.mainmenu.Enable(AWB.SAVE_AS_RULE, enable)

    #---------------------------------------------

    def enableSocietySaveMenuItems(self, enable=True):
      self.mainmenu.Enable(AWB.SAVE_SOCIETY, enable)
      self.mainmenu.Enable(AWB.SAVE_AS_SOCIETY, enable)
      self.mainmenu.Enable(AWB.CHANGE_NAMESERVER, enable)
      self.mainmenu.Enable(AWB.FIND, enable)
      #~ if enable and len(self.searchLabel) > 0:
      self.mainmenu.Enable(AWB.FIND_NEXT, False)
      self.ruleEditor.saveSocietyButton.Enable(enable)
      self.ruleEditor.openSocietyButton.Enable(not enable)
      self.societyEditor.saveSocietyButton.Enable(enable)
      self.societyEditor.openSocietyButton.Enable(not enable)
      self.societyEditor.closeSocietyButton.Enable(enable)
      if self.currentPage == AWB.SOCIETY_EDITOR:
        self.enableTreeViews(enable)

    #---------------------------------------------

    def enableAgentSocietySaveMenuItems(self, enable=True):
      self.agentLaydown.openAgentListButton.Enable(not enable)
      self.agentLaydown.closeAgentSocietyButton.Enable(enable)
      self.mainmenu.Enable(AWB.FIND, enable)
      self.mainmenu.Enable(AWB.FIND_NEXT, False)

    #---------------------------------------------

    def enableHnaSaveMenuItems(self, enable=True):
      self.mainmenu.Enable(AWB.SAVE_AS_HNA_SOCIETY, enable)
      self.agentLaydown.saveHnaButton.Enable(enable)
      self.agentLaydown.openHnaButton.Enable(not enable)
      self.agentLaydown.closeHnaButton.Enable(enable)
      self.societyEditor.getHnaMapButton.Enable(enable)
      self.enableTreeViews(enable)
      self.mainmenu.Enable(AWB.SHOW_COMPONENTS, False)
      self.mainmenu.Enable(AWB.COLLAPSE_COMPONENTS, False)
      self.mainmenu.Enable(AWB.COLLAPSE_AGENTS, False)
      self.mainmenu.Enable(AWB.FIND, enable)
      self.mainmenu.Enable(AWB.FIND_NEXT, False)

    #---------------------------------------------

    def enableTreeViews(self, enable=True):
      self.mainmenu.Enable(AWB.SHOW_SOCIETY, enable)
      self.mainmenu.Enable(AWB.SHOW_NODES, enable)
      self.mainmenu.Enable(AWB.SHOW_AGENTS, enable)
      self.mainmenu.Enable(AWB.SHOW_COMPONENTS, enable)
      self.mainmenu.Enable(AWB.COLLAPSE_HOSTS, enable)
      self.mainmenu.Enable(AWB.COLLAPSE_NODES, enable)
      self.mainmenu.Enable(AWB.COLLAPSE_AGENTS, enable)
      self.mainmenu.Enable(AWB.COLLAPSE_COMPONENTS, enable)

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
      self.viewMenu.Enable(AWB.CLOSE_RULEBOOK, actionFlag)

    #---------------------------------------------

    def enableRuleMenuItems(self, enable=True):
      self.editMenu.Enable(AWB.DELETE_RULE, enable)
      self.editMenu.Enable(AWB.RENAME_RULE, enable)

    #---------------------------------------------

    def enableFindNextMenuItem(self, enable=True):
      self.mainmenu.Enable(AWB.FIND_NEXT, enable)

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
            tp = wx.CreateFileTipProvider(opj("data/tips.txt"), index)
            ##tp = MyTP(0)
            showTip = wx.ShowTip(self, tp)
            index = tp.GetCurrentTip()
            open(opj("data/showTips"), "w").write(str( (showTip, index) ))

    #---------------------------------------------
    def OnTaskBarActivate(self, evt):
        if self.IsIconized():
            self.Iconize(False)
        if not self.IsShown():
            self.Show(True)
        self.Raise()

    #---------------------------------------------

    TBMENU_RESTORE = 1000
    TBMENU_CLOSE   = 1001

    def OnTaskBarMenu(self, evt):
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, "Restore CS03")
        menu.Append(self.TBMENU_CLOSE,   "Close")
        self.tbicon.PopupMenu(menu)
        menu.Destroy()

    #---------------------------------------------
    def OnTaskBarClose(self, evt):
        self.Close()

        # because of the way wxTaskBarIcon.PopupMenu is implemented we have to
        # prod the main idle handler a bit to get the window to actually close
        wx.GetApp().ProcessIdle()


    #---------------------------------------------
    def OnIconfiy(self, evt):
        wx.LogMessage("OnIconfiy")
        evt.Skip()

    #---------------------------------------------
    def OnMaximize(self, evt):
        wx.LogMessage("OnMaximize")
        evt.Skip()




#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

class MySplashScreen(wx.SplashScreen):
  def __init__(self, initPane=1):
      self.initPane = initPane # specifies the wxNotebook tabbed pane to be shown initially
      bmp = wx.Image(opj("bitmaps/AWB.gif")).ConvertToBitmap()
      wx.SplashScreen.__init__(self, bmp,
                              wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT,
                              500, None, -1,
                              style = wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
      wx.EVT_CLOSE(self, self.OnClose)

  def OnClose(self, evt):
    frame = AWB(None, -1, "Agent Workbench", 710, self.initPane)
    frame.Show(True)
    evt.Skip()  # Make sure the default handler runs too...


class MyApp(wx.App):
    def OnInit(self):
        """
        Create and show the splash screen.  It will then create and show
        the main frame when it is time to do so.
        """
        initPane = 3
        if len(sys.argv) > 1:
          initPane = int(sys.argv[1])
        wx.InitAllImageHandlers()
        splash = MySplashScreen(initPane)
        splash.Show()
        return True



#---------------------------------------------------------------------------

def main():
    try:
        demoPath = os.path.dirname(__file__)
        os.chdir(demoPath)
    except:
        pass
    app = MyApp(wx.Platform == "__WXMAC__")
    app.MainLoop()


#---------------------------------------------------------------------------

overview = """<html><body>
 <h2>AWB</h2>
AWB is a consolidator for several Cougaar society functions which can either be done graphically or via
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
