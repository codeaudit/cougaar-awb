#!/bin/env python
#----------------------------------------------------------------------------
# Name:         societyBuilder.py
# Purpose:      
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: societyBuilder.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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
from wxPython.wx import *
from wxPython.stc import *
from wxPython.lib.rcsizer import RowColSizer
import images
from gizmo import Gizmo
import gizmoImages

import os
import os.path
import re
import time
import types

from ACMEPy.rule_text import RuleText
from societyFactoryServer import *
from csmarter_events import *
from editorTextControl import EditorControl
from societyViewer import SocietyViewer
from insertion_dialog import CougaarMessageDialog
#~ from rulebook import Rulebook
#~ from societyFactoryServer import SocietyTransformServer
#~ from societyFactoryServer import SocietyFactoryServer

SHOW_BACKGROUND = 1
#----------------------------------------------------------------------

class SocietyBuilderPanel(wxPanel):
  def __init__( self, parent, frame, log ):

### instance variables
    self.maxWidth  = 1280
    self.maxHeight = 1000
    self.parent = parent
    self.frame = frame # top-level frame containing this wxPanel
    self.transformServer = None # for transforming societies with rules
    self.aRuleIsChecked = False
    self.filename = None
    self.ruleBooks = []
    self.ruleIndex = {}
    self.tempSociety = None

### static layout items
    wxPanel.__init__( self, parent, -1 )
    self.log = log
    self.winCount = 0
    sizer = RowColSizer()
    
    #RuleBook button
    tID = wxNewId()
    self.ruleBookButton = wxButton(self, tID, "Open RuleBook") 
    EVT_BUTTON(self, tID, self.OnOpenRuleBook)
    self.ruleBookButton.SetBackgroundColour(wxBLUE)
    self.ruleBookButton.SetForegroundColour(wxWHITE)
    self.ruleBookButton.SetDefault()
    sizer.Add(self.ruleBookButton, flag=wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 
                  pos=(1,1), colspan=2)

    #Rule CheckListBox
    tID = wxNewId()
    rules = []
    self.lb = wxCheckListBox(self, tID, size=(-1,250), choices=rules, 
                                         style=wxLB_NEEDED_SB|wxLB_HSCROLL)
                                         #~ style=wxLB_NEEDED_SB|wxLB_HSCROLL|wxLB_SORT)
    sizer.Add(self.lb, flag=wxEXPAND, pos=(2,1), colspan=2, rowspan=11)
    EVT_LISTBOX(self, tID, self.OnListBox)
    EVT_CHECKLISTBOX(self, tID, self.OnChecklistBox)
###    
    EVT_UPDATE_SOCIETY(self, self.OnUpdate)

    # Rule Description label
    tID = wxNewId()
    self.descLabel = wxStaticText(self, tID, "Rule Description:") 
    sizer.Add(self.descLabel, flag=wxALIGN_CENTER_VERTICAL, pos=(1,4))
    
    # Rule Description text box
    tID = wxNewId()
    self.ruleDescription = wxTextCtrl(self, tID, "", size=(220, -1), style=wxTE_READONLY)
    self.ruleDescription.SetInsertionPoint(0)
    sizer.Add(self.ruleDescription, pos=(2,4), colspan=2)
    
    #Society name label
    tID = wxNewId()
    self.societyNameLabel = wxStaticText(self, tID, "Current Society:")
    sizer.Add(self.societyNameLabel, flag = wxLEFT | wxALIGN_CENTER_VERTICAL | wxALIGN_LEFT, 
                  border=20, pos=(1, 6))
    
    # Society name text box
    tID = wxNewId()
    self.societyName = wxTextCtrl(self, tID, "", size=(180, -1), style=wxTE_READONLY)
    self.societyName.SetStyle(0, len(self.societyName.GetValue()), wxTextAttr(wxBLUE))
    sizer.Add(self.societyName, flag = wxLEFT | wxALIGN_CENTER_VERTICAL | wxALIGN_LEFT, 
                  border=20, pos=(2,6), colspan=2)
    
    # Rule label
    tID = wxNewId()
    self.ruleLabel = wxStaticText(self, tID, "Rule:") 
    sizer.Add(self.ruleLabel, flag=wxALIGN_CENTER_VERTICAL, pos=(3,4))
    
    # Rule styled text box
    tID = wxNewId()
    self.rule = EditorControl(self, tID, self.log) 
    sizer.Add(self.rule, flag=wxEXPAND, pos=(4,4), colspan=6, rowspan=11)
    
    # Apply Rules button
    tID = wxNewId()
    self.applyRulesButton = wxButton(self, tID, "Apply Rules")
    EVT_BUTTON(self, tID, self.OnApplyRules)
    self.applyRulesButton.Enable(false)
    sizer.Add(self.applyRulesButton, flag=wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 
                pos=(14,1), colspan=2, rowspan=1)
    
    # Create New Rule button
    tID = wxNewId()
    createRuleButton = wxButton(self, tID, "Create New Rule")
    EVT_BUTTON(self, tID, self.OnCreateRule)
    sizer.Add(createRuleButton, flag=wxALIGN_CENTER_HORIZONTAL|wxALIGN_CENTER_VERTICAL, 
                pos=(16,1), colspan=2, rowspan=1)
    
    #Button sizer to hold buttons along bottom
    self.btnSizer = wxBoxSizer(wxHORIZONTAL)
    
    # Save Rule button
    tID = wxNewId()
    self.saveRuleButton = wxButton(self, tID, "Save Rule")
    EVT_BUTTON(self, tID, self.OnSaveRule)
    self.saveRuleButton.Enable(false)
    self.btnSizer.Add(self.saveRuleButton, flag=wxLEFT | wxRIGHT, border=20)
  
    # Open Society button
    tID = wxNewId()
    self.openSocietyButton = wxButton(self, tID, "Open Society")
    EVT_BUTTON(self, tID, self.OnOpenSociety)
    self.openSocietyButton.SetBackgroundColour(wxGREEN)
    self.btnSizer.Add(self.openSocietyButton, flag=wxLEFT | wxRIGHT, border=20)
 
    # Save Society button
    tID = wxNewId()
    self.saveSocietyButton = wxButton(self, tID, "Save Society")
    EVT_BUTTON(self, tID, self.OnSaveSociety)
    self.saveSocietyButton.Enable(false)
    self.btnSizer.Add(self.saveSocietyButton, flag=wxLEFT | wxRIGHT, border=20)

    # Undo Transform button
    tID = wxNewId()
    self.undoTransformButton = wxButton(self, tID, "Undo Transform")
    EVT_BUTTON(self, tID, self.OnUndoTransform)
    self.undoTransformButton.Enable(false)
    self.btnSizer.Add(self.undoTransformButton, flag=wxLEFT | wxRIGHT, border=20)

    sizer.Add(self.btnSizer, pos=(16,4), colspan=6)

    # Progress gizmo image
    tID = wxNewId()
    lesImages = [gizmoImages.catalog[i].getBitmap() for i in gizmoImages.index]        
    self.gizmo = Gizmo(self, -1, lesImages, size=(36, 36), frameDelay = 0.1)
    sizer.Add(self.gizmo, pos=(2,9), flag=wxALIGN_RIGHT, rowspan=2)

    if SHOW_BACKGROUND:
      self.bg_bmp = images.getGridBGBitmap()
      EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)

    # Add finishing touches to the layout
    sizer.AddGrowableCol(7) # makes rule styled text box and Society Viewer expand to the right on window resize
    sizer.AddGrowableRow(4) # makes Society Viewer expand downward on window resize
    sizer.AddSpacer(10,10, pos=(1,10)) # adds a constant size border along top and right side
    sizer.AddSpacer(10,10, pos=(17,1)) # adds a constant size border along bottom and left side
    
    self.SetSizer(sizer)
    self.SetAutoLayout(true)
    
    EVT_RIGHT_DOWN(self.lb, self.OnRightDown)  # emits a wxMouseEvent
    EVT_RIGHT_UP(self.lb, self.OnRightUp)  # emits a wxMouseEvent
  

#---------------------------------------------------------------------------------------------------

  def OnOpenRuleBook(self, event):
    dlg = wxDirDialog(self, "Choose a RuleBook:", os.getcwd(), style=wxDD_DEFAULT_STYLE|wxDD_NEW_DIR_BUTTON)
    if dlg.ShowModal() == wxID_OK:
      ruleBookPath = dlg.GetPath()
      # check if this rulebook already open
      for rulebook in self.ruleBooks:
        if ruleBookPath == rulebook.getPath():
          dlg.Destroy()
          self.log.WriteText("Ignored attempt to open an already opened Rulebook (%s)\n" % rulebook.getName())
          return
      # Must not be already open, so continue
      ruleBook = Rulebook(ruleBookPath)
      # Next, if there are no [.rul | .rule] files in the dir, show user a dialog and return.
      if ruleBook.isEmpty():
        emptyRulebookDialog = CougaarMessageDialog(self, "info", "The selected rulebook is empty.")
        emptyRulebookDialog.display()
        dlg.Destroy()
        return
      # Wasn't empty, so continue
      self.ruleBooks.append(ruleBook)
      for rule in ruleBook.each_rule():
        self.lb.Append(rule)
        self.ruleIndex[rule] = ruleBook  # links rules to their containing rulebook
      addRulebook = True
      self.frame.updateCloseRulebookMenuItem(addRulebook)
    dlg.Destroy()
    
#---------------------------------------------------------------------- 

  def OnSaveRule(self, event):
    self.SaveRule()

#---------------------------------------------------------------------- 

  def OnCreateRule(self, event):
    #First check for changes to current rule
    if self.rule.textIsDirty:
      msg = 'Save changes to rule?'
      dlg = wxMessageDialog(self, msg, style = wxCAPTION | wxYES_NO | 
                     wxNO_DEFAULT | wxTHICK_FRAME | wxICON_EXCLAMATION)
      
      val = dlg.ShowModal()
      if val == wxID_YES:
        self.SaveRule()
    
    self.clearRule()
  
#---------------------------------------------------------------------- 
  
  def clearRule(self):
    self.rule.SetText("")
    self.ruleDescription.SetValue("")
    self.frame.enableRuleSaveMenuItems()
    item = self.lb.GetSelection()
    if item > -1:
      # if an item is selected, deselect it
      self.lb.SetSelection(item, FALSE)
    self.rule.textIsDirty = False
    self.rule.SetFocus()
    self.frame.enableRuleSaveMenuItems(False)
    self.filename = None

#---------------------------------------------------------------------- 

  def OnOpenSociety(self, event):
    self.frame.openSocietyFile(self, "society")
    if self.aRuleIsChecked:
      self.applyRulesButton.Enable(true)

#------------------------------------------------------------------------------

  def OnSaveSociety(self, event):
    if not self.frame.societyOpen:
        dlg = wxMessageDialog(self, 'No society is open. You must open a society before you can save it.',
                'No Society Open', wxOK | wxICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()
    else:
      self.frame.saveSociety()
      self.tempSociety = None  # clear out the backup copy
  
  #------------------------------------------------------------------------------
  
  def OnUndoTransform(self, event):
    msg = '''
Are you sure you want to undo the transformation?

You will lose all changes made to the society since the transformation.'''
    choice = CougaarMessageDialog(self, 'confirm', msg).getUserInput()
    if choice == wxID_YES:
      self.frame.society = self.tempSociety
      self.frame.societyViewer.UpdateControl(self.frame.society, true)
      self.frame.ruleEditor.societyName.SetValue(self.frame.society.name)
      for node in self.frame.society.each_node():
        node.updateNameServerParam(self.frame.society.get_nameserver())
      self.undoTransformButton.Disable()
  
  #-------------------------------------------------------------------------------
  
  def OnListBox(self, event):
    #self.log.WriteText('EvtListBox: %s\n' % event.GetString())
    if self.rule.textIsDirty == True:
      msg = 'Save changes to rule?'
      dlg = wxMessageDialog(self, msg, style = wxCAPTION | wxYES_NO | 
                     wxNO_DEFAULT | wxTHICK_FRAME | wxICON_EXCLAMATION)
      val = dlg.ShowModal()
      if val == wxID_YES:
        self.SaveRule()
    
    selectedRule = self.lb.GetStringSelection()
    rulebook = self.ruleIndex[selectedRule]  # get this rule's associated rulebook
    self.filename = os.path.join(rulebook.getPath(), selectedRule)
    self.ruleText = RuleText(self.filename)
    #~ if self.filename.endswith(".rule"):
      #~ self.rule.SetLexer(wxSTC_LEX_RUBY)
      #~ print "Lexer set to Ruby"
    #~ else:
      #~ self.rule.SetLexer(wxSTC_LEX_PYTHON)
    self.rule.SetLexer(wxSTC_LEX_PYTHON)
    self.rule.SetText(self.ruleText.rule)
    self.rule.EmptyUndoBuffer()
    self.rule.Colourise(0, -1)
    self.ruleDescription.SetValue(self.ruleText.description)
    # line numbers in the margin
    self.rule.SetMarginType(1, wxSTC_MARGIN_NUMBER)
    self.rule.SetMarginWidth(1, 25)     
    self.rule.textIsDirty = False
    self.frame.enableRuleSaveMenuItems(False)
    self.frame.enableRuleSaveAs(True)
    self.frame.enableRuleMenuItems()
  
#-------------------------------------------------------------------------------

  def OnChecklistBox(self,event):
    # event.IsChecked() returns true regardless of whether checkbox was checked or unchecked!!!
    # So, we'll just have to search the whole list and see if anything is checked.
    self.aRuleIsChecked = false
    for item in range(self.lb.GetCount()):
      if self.lb.IsChecked(item):
        # a rule is checked; set the flag and stop searching
        self.aRuleIsChecked = true
        break
    if self.frame.societyOpen and self.aRuleIsChecked:
      self.applyRulesButton.Enable(true)
    if not self.aRuleIsChecked:
      # no rules were checked; disable the button
      self.applyRulesButton.Enable(false)

#-------------------------------------------------------------------------------

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
#--------------------------------------------------------------------------------------------

  def OnApplyRules(self, event):
    self.tempSociety = self.frame.society.clone()  # save a copy in case we must restore
    numRules = self.lb.GetCount()
    if numRules > 0:
      checkedRules = []  # will hold a string path/filename for ea rule checked 
      ruleFilename = None
      for item in range(numRules):
        if self.lb.IsChecked(item):
          ruleFilename = self.lb.GetString(item)
          wxLogMessage("Applying rule " + str(item) + ": " + ruleFilename + "\n")
          if self.lb.Selected(item) and self.rule.textIsDirty == True:
            msg = "The rule you are applying has been changed. If you wish " + \
                      "to apply the changed version, you must first save the rule. "  + \
                      "Would you like to save the rule now?"
            dlg = wxMessageDialog(self, msg, style = wxCAPTION | wxYES_NO | 
                           wxNO_DEFAULT | wxTHICK_FRAME | wxICON_EXCLAMATION)
            
            val = dlg.ShowModal()
            if val == wxID_YES:
              self.SaveRule()
          rulebook = self.ruleIndex[ruleFilename]  # get this rule's associated rulebook
          checkedRules.append(os.path.join(rulebook.getPath(), ruleFilename))
      
      if len(checkedRules) > 0:
        self.frame.ruleApplied = True
        if ruleFilename.endswith('rule'):  # just sample the last rule checked
          # They're Ruby rules
          rubyArgs = 'ruby ../../ruby/acme_scripting/src/lib/cougaar/py_society_builder.rb '
          rubyArgs = rubyArgs + ' '.join(checkedRules)
          self.log.WriteText("Transformation in progress...please wait\n")
          # Call a Ruby program that receives the society (in Ruby code) as a string from Python, 
          # creates a Ruby society object, transforms that society per rules passed as args,
          # then outputs it back to Python as a string of xml-formatted text
          input, output = os.popen2(rubyArgs)  
          input.write(self.frame.society.to_ruby())  # sends society as Ruby code to Ruby
          input.close()
          xmlSocietyList = output.readlines()  # transformed society as a list of  XML strings from Ruby
          output.close()
          
          # Check if Ruby threw an exception during transformation
          if xmlSocietyList[0].lower().find('error') >= 0:
            self.log.WriteText("Transformation failed.\n")
            msg = 'ERROR parsing XML document.\nSociety creation/transformation failed.'
            wxLogError(msg)
            errorDialog = CougaarMessageDialog(self.frame, "error", msg)
            errorDialog.display()            
            return
          else:
            #codeObj = "".join(codeObjList)  # for use when output from Ruby program is Python code
            #exec codeObj     # for use when output from Ruby program is Python code
            xmlSociety = "".join(xmlSocietyList)  # join list elements into a single string; for use when output from Ruby program is XML
            # Now parse the xml string and create the new, transformed society
            self.frame.server = SocietyFactoryServer(None, self, self.log, xmlSociety)
            self.frame.server.Start()
            # NOTE: The animation doesn't work while the Ruby process is executing.  I presume it's
            # because the animation is a thread of the Python process, and while the Ruby process
            # is executing, the Python process is blocked waiting for output from Ruby.  I'm guessing that
            # as long as the Python process is blocked, all its threads are also blocked.  However, I've
            # noticed that once the Ruby process completes, many, many gizmo events arrive all at once.  
            # So it may be that the animation thread continues to run, but its events are not handled till 
            # after the Ruby process completes.  
        else:
          # They're Python rules, so...
          # Create one SocietyTransformServer instance and pass it a list of rules to execute
          self.transformServer = SocietyTransformServer(self.frame.society, checkedRules, self, self.log)
          self.transformServer.Start()
        #~ self.StartAnimation()
        self.log.WriteText("Transformation complete.\n")
        self.undoTransformButton.Enable(True)
        doneDialog = CougaarMessageDialog(self, "info", "Transformation complete.")
        doneDialog.display()
  
  #--------------------------------------------------------------------------------------------
  
  def OnRightDown(self, event):
    if wxPlatform == '__WXMSW__':
      pt = event.GetPosition()
      itemId = self.lb.HitTest(pt)
      self.lb.SetSelection(itemId, True)
      self.OnListBox(None)
  
  #--------------------------------------------------------------------------------------------
  
  def OnRightUp(self, event):
    if wxPlatform == '__WXMSW__':
      x = event.GetX()
      y = event.GetY()
      #~ point = wxPoint(x, y+20)
      point = wxPoint(x, y)
      menu = wxMenu()
      menuItem = wxMenuItem(menu, 200, "Delete Rule")
      menu.AppendItem(menuItem)  
      menuItem = wxMenuItem(menu, 210, "Rename Rule")
      menu.AppendItem(menuItem)  
      EVT_MENU(self, 200, self.OnDeleteRule)
      EVT_MENU(self, 210, self.OnRenameRule)
      self.PopupMenu(menu, point)
      menu.Destroy()
      event.Skip()
  
  #--------------------------------------------------------------------------------------------
  
  def OnDeleteRule(self, event):
    ruleIdToDelete = self.lb.GetSelection()
    if ruleIdToDelete < 0:
      self.log.WriteText("Unable to delete rule: no rule selected\n")
      return
    ruleNameToDelete = self.lb.GetString(ruleIdToDelete)
    rulebook = self.ruleIndex[ruleNameToDelete]  # get this rule's associated rulebook
    msg = '''Are you sure you want to delete this rule?
Doing so will permanently delete it from disk.'''
    dlg = CougaarMessageDialog(self, "delete", msg)
    response = dlg.getUserInput()
    if response == wxID_YES:
      self.lb.Delete(ruleIdToDelete)  # remove it from the list box
      os.remove(os.path.join(rulebook.getPath(), ruleNameToDelete))  # delete from disk
      self.clearRule()  # clear the rule text
    self.frame.enableRuleMenuItems(False)
    rulebook.removeRule(ruleNameToDelete)
    if rulebook.size() == 0:
      self.removeRulebook(rulebook)
  
#--------------------------------------------------------------------------------------------
  
  def OnRenameRule(self, event):
    ruleIdToRename = self.lb.GetSelection()
    if ruleIdToRename < 0:
      self.log.WriteText("Unable to rename rule: no rule selected\n")
      return
    ruleNameToRename = self.lb.GetString(ruleIdToRename)
    rulebook = self.ruleIndex[ruleNameToRename]  # get this rule's associated rulebook
    # Get the new rule name from the user
    newRuleName = []
    msg = "Current rule name: " + ruleNameToRename + "\nNew rule name:"
    renameDialog = wxTextEntryDialog(self, msg, 'Rename Rule')
    renameDialog.SetSize((175, -1))
    if renameDialog.ShowModal() == wxID_OK:
      newRuleName.append(renameDialog.GetValue())
    renameDialog.Destroy()
    if len(newRuleName) > 0:
      self.lb.InsertItems(newRuleName, ruleIdToRename) # This messes up the sort order. Is that OK?
      self.lb.Delete(ruleIdToRename+1)
      # Replace the old rule name with the new in the ruleIndex dictionary
      del self.ruleIndex[ruleNameToRename] 
      self.ruleIndex[newRuleName[0]] = rulebook
      # Update rulebook with new rule name
      rulebook.replaceRule(ruleNameToRename, newRuleName[0])
      os.chdir(rulebook.path)
      os.rename(ruleNameToRename, newRuleName[0])
  
#--------------------------------------------------------------------------------------------

  def StartAnimation(self):
    self.gizmo.Start()
#--------------------------------------------------------------------------------------------

  def StopAnimation(self):
    self.gizmo.Rest()
#----------------------------------------------------------------------

  def SaveRule(self):
    if self.filename is None:
      wildcard = "Rule File (*.rule)|*.rule|" \
                      "All files (*.*)|*.*"
      rulePath = os.getcwd()
      if len(self.ruleBooks) > 1:
        rulePath = self.ruleBooks[-1].path
      dlg = wxFileDialog(self, "Save Rule As", rulePath, "", wildcard, wxSAVE)
      try:
        if dlg.ShowModal() == wxID_OK:
          self.filename = dlg.GetPath()
          self.save_rule()
      finally:
        dlg.Destroy()
    else:
      self.save_rule()
      
#---------------------------------------------------------------------- 

  def save_rule(self):
    ruleText = RuleText(None, description=self.ruleDescription.GetValue(), rule=self.rule.GetText())
    ruleText.saveRule(self.filename)
    self.log.WriteText("Rule saved as %s\n" % self.filename)
    rulebook = self.addToRulebook()
    dir, file = os.path.split(self.filename)
    if self.lb.FindString(file) < 0:
      # Add rule to list box only if it's not already there
      self.lb.Append(file)
      self.ruleIndex[file] = rulebook  # links rule to its containing rulebook
    self.ruleDescription.SetValue(ruleText.getDescription())
    self.rule.textIsDirty = False
    self.frame.enableRuleSaveMenuItems(False)
    self.frame.enableRuleSaveAs(True)
  
#---------------------------------------------------------------------- 

  def removeRulebook(self, rulebook):
    if isinstance(rulebook, Rulebook):
      # if rule in editor window is in this rulebook, clear the editor window
      if self.filename is not None:
        dir, rule = os.path.split(self.filename)
        if rulebook.containsRule(rule):
          if self.rule.textIsDirty:
            # First give user a chance to save rule
            msg = 'Closing this rulebook will also close the\ncurrently open rule. Save rule first?'
            dlg = CougaarMessageDialog(self, "close", msg)
            disposition = dlg.getUserInput()
            if disposition == wxID_CANCEL:
              return
            elif disposition == wxID_YES:
              self.save_rule()
          self.clearRule()
      for rule in rulebook.each_rule():
        item = self.lb.FindString(rule)
        if item >= 0:
          self.lb.Delete(item)
      self.ruleBooks.remove(rulebook)
      removeRulebook = False
      self.frame.updateCloseRulebookMenuItem(removeRulebook)
    else:  # must be a rulebook name (String)
      aRulebook = self.getRulebook(rulebook)
      if aRulebook is not None:
        self.removeRulebook(aRulebook)

#---------------------------------------------------------------------- 

  def getRulebook(self, rulebookName):
    for rulebook in self.ruleBooks:
      if rulebook.name == rulebookName:
        return rulebook
    return None
  
#---------------------------------------------------------------------- 
  
  def getRulebookNames(self):
    rbookNames = []
    for rulebook in self.ruleBooks:
      rbookNames.append(rulebook.name)
    return rbookNames
  
#---------------------------------------------------------------------- 
  
  def addToRulebook(self):
    dir, file = os.path.split(self.filename)
    for rulebook in self.ruleBooks:
      if rulebook.path == dir:
        if not rulebook.containsRule(file):
          rulebook.addRule(file)
        return rulebook
      # If no rulebook found (i.e., this is the first rule in a new rulebook dir),
      # create a new rulebook
      rulebook = Rulebook(dir)
      rulebook.addRule(file)
      self.ruleBooks.append(rulebook)
      return rulebook
  
  #---------------------------------------------------------------------- 
  
  def OnUpdate(self, event):
    #~ self.log.WriteText("Stop time: %s\n" % time.ctime())
    self.StopAnimation() 
    if self.transformServer is not None and self.transformServer.IsRunning():
      self.transformServer.Stop()
    if self.frame.server is not None and self.frame.server.IsRunning():
      self.frame.server.Stop()
    self.frame.society = event.msg
    if self.frame.society is not None:
      self.societyName.SetValue(self.frame.society.name)
      viewer = self.frame.societyViewer
      viewer.UpdateControl(self.frame.society, true)
      if self.frame.ruleApplied:  # if we're updating due to rule application, make a log entry
        num = self.frame.societyViewer.getNumEntitiesChanged()
        wxLogMessage('Number of society entities modified: ' + str(num))
        self.frame.ruleApplied = False
      self.frame.enableSocietySaveMenuItems()
      self.setNextHighlightButton()
      self.frame.societyOpen = true
  
  #---------------------------------------------------------------------- 
  
  # All we're trying to do here is determine if the Next Highlight button
  # should be enabled or not.  Also, if there are highlighted items that
  # are already visible, increment the colourisedItemIndex to
  # the first non-visible item's position in the colourisedItemsList.
  #
  def setNextHighlightButton(self):
    viewer = self.frame.societyViewer
    btn = self.frame.societyEditor.nextHighlightButton
    if viewer.colourisedItemIndex < len(viewer.colourisedItemsList):  # if we've got some highlighted items
      hiItem = viewer.colourisedItemsList[viewer.colourisedItemIndex]  # get the first one
      
      while viewer.IsVisible(hiItem):
        # while there are more highlighted items and they are already visible:
        viewer.colourisedItemIndex += 1  # increment index to look at the next one
        if viewer.colourisedItemIndex < len(viewer.colourisedItemsList):
          hiItem = viewer.colourisedItemsList[viewer.colourisedItemIndex]
        else:
          btn.Enable(False)
          break
      
      else:   # there is another highlighted item that is not visible
        btn.Enable(True)
    else:
      btn.Enable(False)
  
#***********************************************

class Rulebook:
  '''Represents a directory containing Ruby or Python "rules" which
are used to transform a Cougaar society.  A Rulebook instance
contains the following attributes:
    path [String]: The path to the rule file.  Contains the drive, but not the filename
    rules [List]: Contains the String filenames for each file in the directory specified
                      in the path that has an extension of ".rul" or ".rule"
    name [String]: The name of the subdirectory containing the rule files
'''
  def __init__(self, path):
    
    self.path = path
    self.rules = []
    index = path.rfind(os.sep)
    if index >= 0:
      self.name = path[index+1:]    # String; the immediate directory containing the rules
    files = os.listdir(path)               # List; contains filenames of each of the rules
    
    self.fileTypes = re.compile('^.*\.rul', re.IGNORECASE)
    for file in files: 
      filename = str(file)
      if self.fileTypes.search(filename) is not None:
        self.rules.append(filename)
  
  def getPath(self):
    return self.path
  
  def getName(self):
    return self.name
  
  def setRules(self, rules):
    self.rules = rules
  
  def getRules(self):
    return self.rules
  
  def addRule(self, ruleName):
    self.rules.append(ruleName)
  
  def removeRule(self, ruleName):
    for rule in self.rules:
      if rule == ruleName:
        self.rules.remove(rule)
        return
  
  def each_rule(self):
    for rule in self.rules:
      yield rule

  def containsRule(self, ruleName):
    for rule in self.rules:
      if rule == ruleName:
        return True
    return False
  
  def isEmpty(self):
    if len(self.rules) > 0:
      return False
    return True
  
  def size(self):
    return len(self.rules)
  
  def replaceRule(self, oldRule, newRule):
    self.removeRule(oldRule)
    self.addRule(newRule)

#***********************************************

def runApp( frame, nb, log ):
  win = SocietyBuilderPanel( nb, log )
  return win

#----------------------------------------------------------------------

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])])
