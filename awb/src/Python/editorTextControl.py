#!/bin/env python
#----------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: editorTextControl.py,v 1.3 2004-10-25 21:00:55 jnilsson Exp $
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
from wxPython.stc import *
from wxPython.lib.anchors import LayoutAnchors

import keyword

if wxPlatform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }


#---------------------------------------------------------------------

class EditorControl(wxStyledTextCtrl):
  def __init__(self, parent,  ID, log, size=None, pos=None):
    self.parent = parent
    self.log = log
    self.textIsDirty = False
    if size is not None:
      theSize = size
    else:
      theSize = wxSize(100,100)
    if pos is not None:
      thePos = pos
    else:
      thePos = wxPoint(10,10)
    self.stc = wxStyledTextCtrl.__init__(self, parent, ID, pos=thePos, size=theSize, style = wxSUNKEN_BORDER)

    self.CmdKeyAssign(ord('B'), wxSTC_SCMOD_CTRL, wxSTC_CMD_ZOOMIN)
    self.CmdKeyAssign(ord('N'), wxSTC_SCMOD_CTRL, wxSTC_CMD_ZOOMOUT)

    self.SetLexer(wxSTC_LEX_PYTHON)
    #self.SetLexer(wxSTC_LEX_RUBY)
    self.SetKeyWords(0, " ".join(keyword.kwlist))

    self.SetProperty("fold", "1")
    self.SetProperty("tab.timmy.whinge.level", "1")
    self.SetMargins(0,0)

    self.SetViewWhiteSpace(false)
    #self.SetBufferedDraw(false)

    self.SetEdgeMode(wxSTC_EDGE_BACKGROUND)
    self.SetEdgeColumn(78)

    self.adjustEOL()
    #self.SetViewEOL(1)
    # Setup a margin to hold fold markers
    #self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
    self.SetMarginType(2, wxSTC_MARGIN_SYMBOL)
    self.SetMarginMask(2, wxSTC_MASK_FOLDERS)
    self.SetMarginSensitive(2, true)
    self.SetMarginWidth(2, 12)

    if 0: # simple folder marks, like the old version
      self.MarkerDefine(wxSTC_MARKNUM_FOLDER, wxSTC_MARK_ARROW, "navy", "navy")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPEN, wxSTC_MARK_ARROWDOWN, "navy", "navy")
      # Set these to an invisible mark
      self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPENMID, wxSTC_MARK_BACKGROUND, "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERMIDTAIL, wxSTC_MARK_BACKGROUND, "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERSUB, wxSTC_MARK_BACKGROUND, "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERTAIL, wxSTC_MARK_BACKGROUND, "white", "black")

    else: # more involved "outlining" folder marks
      self.MarkerDefine(wxSTC_MARKNUM_FOLDEREND,     wxSTC_MARK_BOXPLUSCONNECTED,  "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPENMID, wxSTC_MARK_BOXMINUSCONNECTED, "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERMIDTAIL, wxSTC_MARK_TCORNER,  "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERTAIL,    wxSTC_MARK_LCORNER,  "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDERSUB,     wxSTC_MARK_VLINE,    "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDER,        wxSTC_MARK_BOXPLUS,  "white", "black")
      self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPEN,    wxSTC_MARK_BOXMINUS, "white", "black")

    EVT_STC_UPDATEUI(self,    ID, self.OnUpdateUI)
    EVT_STC_MARGINCLICK(self, ID, self.OnMarginClick)
    EVT_STC_MODIFIED(self, ID, self.OnModified)



    # Make some styles,  The lexer defines what each style is used for, we
    # just have to define what each style looks like.  This set is adapted from
    # Scintilla sample property files.

    self.StyleClearAll()

    # Global default styles for all languages
    self.StyleSetSpec(wxSTC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
    self.StyleSetSpec(wxSTC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
    self.StyleSetSpec(wxSTC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
    self.StyleSetSpec(wxSTC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
    self.StyleSetSpec(wxSTC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

    # Python styles
    # White space
    self.StyleSetSpec(wxSTC_P_DEFAULT, "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
    # Comment
    self.StyleSetSpec(wxSTC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # Number
    self.StyleSetSpec(wxSTC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
    # String
    self.StyleSetSpec(wxSTC_P_STRING, "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
    # Single quoted string
    self.StyleSetSpec(wxSTC_P_CHARACTER, "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
    # Keyword
    self.StyleSetSpec(wxSTC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
    # Triple quotes
    self.StyleSetSpec(wxSTC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
    # Triple double quotes
    self.StyleSetSpec(wxSTC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
    # Class name definition
    self.StyleSetSpec(wxSTC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
    # Function or method name definition
    self.StyleSetSpec(wxSTC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
    # Operators
    self.StyleSetSpec(wxSTC_P_OPERATOR, "bold,size:%(size)d" % faces)
    # Identifiers
    self.StyleSetSpec(wxSTC_P_IDENTIFIER, "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
    # Comment-blocks
    self.StyleSetSpec(wxSTC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
    # End of line where string is not closed
    self.StyleSetSpec(wxSTC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)


    self.SetCaretForeground("BLUE")

    EVT_KEY_DOWN(self, self.OnKeyPressed)

  def convertEOL(self):
    if wxPlatform == '__WXMSW__':
      self.ConvertEOLs(wxSTC_EOL_CRLF)
    else:
      self.ConvertEOLs(wxSTC_EOL_CR)

  def adjustEOL(self):
    note = """
    wxSTC_EOL_CR   : CR only
    wxSTC_EOL_CRLF : CRLF
    wxSTC_EOL_LF   : LF only
    """
    if wxPlatform == '__WXMSW__':
        self.SetEOLMode(wxSTC_EOL_CRLF)
    else:
        self.SetEOLMode(wxSTC_EOL_CR)


  def OnKeyPressed(self, event):
    #self.textIsDirty = True
    if self.CallTipActive():
      self.CallTipCancel()
    key = event.KeyCode()
    if key == 32 and event.ControlDown():
      pos = self.GetCurrentPos()
      # Tips
      if event.ShiftDown():
        self.CallTipSetBackground("yellow")
        self.CallTipShow(pos, 'param1, param2')
      # Code completion
      #else:
          #lst = []
          #for x in range(50000):
          #    lst.append('%05d' % x)
          #st = " ".join(lst)
          #print len(st)
          #self.AutoCompShow(0, st)
          #self.AutoCompSetIgnoreCase(false)  # so this needs to match
    else:
      event.Skip()

  def OnKeyPressed_old(self, event):
    #self.textIsDirty = True
    if self.CallTipActive():
      self.CallTipCancel()
    key = event.KeyCode()
    if key == 32 and event.ControlDown():
	pos = self.GetCurrentPos()
	# Tips
	if event.ShiftDown():
	    self.CallTipSetBackground("yellow")
	    self.CallTipShow(pos, 'param1, param2')
	# Code completion
	#else:
	    #lst = []
	    #for x in range(50000):
	    #    lst.append('%05d' % x)
	    #st = " ".join(lst)
	    #print len(st)
	    #self.AutoCompShow(0, st)
	    #self.AutoCompSetIgnoreCase(false)  # so this needs to match
    else:
      event.Skip()


  def OnUpdateUI(self, evt):
      # check for matching braces
      braceAtCaret = -1
      braceOpposite = -1
      charBefore = None
      caretPos = self.GetCurrentPos()
      if caretPos > 0:
        charBefore = self.GetCharAt(caretPos - 1)
        styleBefore = self.GetStyleAt(caretPos - 1)

      # check before
      if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wxSTC_P_OPERATOR:
        braceAtCaret = caretPos - 1

      # check after
      if braceAtCaret < 0:
        charAfter = self.GetCharAt(caretPos)
        styleAfter = self.GetStyleAt(caretPos)
        if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wxSTC_P_OPERATOR:
          braceAtCaret = caretPos

      if braceAtCaret >= 0:
        braceOpposite = self.BraceMatch(braceAtCaret)

      if braceAtCaret != -1  and braceOpposite == -1:
        self.BraceBadLight(braceAtCaret)
      else:
        self.BraceHighlight(braceAtCaret, braceOpposite)
        #pt = self.PointFromPosition(braceOpposite)
        #self.Refresh(true, wxRect(pt.x, pt.y, 5,5))
        #print pt
        #self.Refresh(false)

  def OnMarginClick(self, evt):
      # fold and unfold as needed
      if evt.GetMargin() == 2:
	  if evt.GetShift() and evt.GetControl():
	      self.FoldAll()
	  else:
	      lineClicked = self.LineFromPosition(evt.GetPosition())
	      if self.GetFoldLevel(lineClicked) & wxSTC_FOLDLEVELHEADERFLAG:
		  if evt.GetShift():
		      self.SetFoldExpanded(lineClicked, true)
		      self.Expand(lineClicked, true, true, 1)
		  elif evt.GetControl():
		      if self.GetFoldExpanded(lineClicked):
			  self.SetFoldExpanded(lineClicked, false)
			  self.Expand(lineClicked, false, true, 0)
		      else:
			  self.SetFoldExpanded(lineClicked, true)
			  self.Expand(lineClicked, true, true, 100)
		  else:
		      self.ToggleFold(lineClicked)


  def OnModified(self, event):
    self.textIsDirty = True
    self.parent.frame.enableRuleSaveMenuItems()

  def FoldAll(self):
      lineCount = self.GetLineCount()
      expanding = true

      # find out if we are folding or unfolding
      for lineNum in range(lineCount):
	  if self.GetFoldLevel(lineNum) & wxSTC_FOLDLEVELHEADERFLAG:
	      expanding = not self.GetFoldExpanded(lineNum)
	      break;

      lineNum = 0
      while lineNum < lineCount:
	  level = self.GetFoldLevel(lineNum)
	  if level & wxSTC_FOLDLEVELHEADERFLAG and \
	     (level & wxSTC_FOLDLEVELNUMBERMASK) == wxSTC_FOLDLEVELBASE:

	      if expanding:
		  self.SetFoldExpanded(lineNum, true)
		  lineNum = self.Expand(lineNum, true)
		  lineNum = lineNum - 1
	      else:
		  lastChild = self.GetLastChild(lineNum, -1)
		  self.SetFoldExpanded(lineNum, false)
		  if lastChild > lineNum:
		      self.HideLines(lineNum+1, lastChild)

	  lineNum = lineNum + 1



  def Expand(self, line, doExpand, force=false, visLevels=0, level=-1):
      lastChild = self.GetLastChild(line, level)
      line = line + 1
      while line <= lastChild:
	  if force:
	      if visLevels > 0:
		  self.ShowLines(line, line)
	      else:
		  self.HideLines(line, line)
	  else:
	      if doExpand:
		  self.ShowLines(line, line)

	  if level == -1:
	      level = self.GetFoldLevel(line)

	  if level & wxSTC_FOLDLEVELHEADERFLAG:
	      if force:
		  if visLevels > 1:
		      self.SetFoldExpanded(line, true)
		  else:
		      self.SetFoldExpanded(line, false)
		  line = self.Expand(line, doExpand, force, visLevels-1)

	      else:
		  if doExpand and self.GetFoldExpanded(line):
		      line = self.Expand(line, true, force, visLevels-1)
		  else:
		      line = self.Expand(line, false, force, visLevels-1)
	  else:
	      line = line + 1;

      return line

