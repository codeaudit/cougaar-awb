# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: csmarter_events.py,v 1.4 2004-12-06 22:22:46 damoore Exp $
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

import wx

wxEVT_UPDATE_SOCIETY = wx.NewEventType()
EVT_UPDATE_SOCIETY = wx.PyEventBinder(wxEVT_UPDATE_SOCIETY, 1)


#----------------------------------------------------------------------
class UpdateSocietyEvent(wx.PyEvent):
    def __init__(self, msg):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_UPDATE_SOCIETY)
        self.msg = msg

#----------------------------------------------------------------------


wxEVT_SOCIETYCONTROLLER_TEST = wx.NewEventType()
EVT_SOCIETYCONTROLLER_TEST = wx.PyEventBinder(wxEVT_SOCIETYCONTROLLER_TEST, 1)
#~ def EVT_SOCIETYCONTROLLER_TEST(win, func):
    #~ win.Connect(-1, -1, wxEVT_SOCIETYCONTROLLER_TEST, func)

#----------------------------------------------------------------------
class SocietyControllerEvent(wx.PyEvent):
    def __init__(self, msg):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_SOCIETYCONTROLLER_TEST)
        self.msg = msg

#----------------------------------------------------------------------
#----------------------------------------------------------------------


wxEVT_AGENT_TASK_COUNT = wx.NewEventType()
EVT_AGENT_TASK_COUNT = wx.PyEventBinder(wxEVT_AGENT_TASK_COUNT, 1)
#~ def EVT_AGENT_TASK_COUNT(win, func):
    #~ win.Connect(-1, -1, wxEVT_AGENT_TASK_COUNT, func)

#----------------------------------------------------------------------
class AgentTaskCountEvent(wx.PyEvent):
    def __init__(self, msg):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_AGENT_TASK_COUNT)
        self.msg = msg

