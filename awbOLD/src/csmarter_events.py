#!/bin/env python
#----------------------------------------------------------------------------
# Name:
# Purpose:
#
# Author:       ISAT (D. Moore/P. Gardella)
#
# RCS-ID:       $Id: csmarter_events.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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
from wxPython import  events


wxEVT_UPDATE_SOCIETY = wxNewEventType()

def EVT_UPDATE_SOCIETY(win, func):
    win.Connect(-1, -1, wxEVT_UPDATE_SOCIETY, func)

#----------------------------------------------------------------------
class UpdateSocietyEvent(wxPyEvent):
    def __init__(self, msg):
        wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_UPDATE_SOCIETY)
        self.msg = msg

#----------------------------------------------------------------------


wxEVT_SOCIETYCONTROLLER_TEST = wxNewEventType()

def EVT_SOCIETYCONTROLLER_TEST(win, func):
    win.Connect(-1, -1, wxEVT_SOCIETYCONTROLLER_TEST, func)

#----------------------------------------------------------------------
class SocietyControllerEvent(wxPyEvent):
    def __init__(self, msg):
        wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_SOCIETYCONTROLLER_TEST)
        self.msg = msg

#----------------------------------------------------------------------
#----------------------------------------------------------------------


wxEVT_AGENT_TASK_COUNT = wxNewEventType()

def EVT_AGENT_TASK_COUNT(win, func):
    win.Connect(-1, -1, wxEVT_AGENT_TASK_COUNT, func)

#----------------------------------------------------------------------
class AgentTaskCountEvent(wxPyEvent):
    def __init__(self, msg):
        wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_AGENT_TASK_COUNT)
        self.msg = msg

