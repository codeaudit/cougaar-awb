#!/bin/env python
#----------------------------------------------------------------------------
# Name:         
# Purpose:      
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: societyFactoryServer.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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


#import threading 
import sys, thread, traceback
#~ import Queue

from ACMEPy.rule_text import RuleText
from ACMEPy.society_factory2 import *
#~ from ACMEPy import SocietyFactory
#~ from ACMEPy import TransformationRule
#~ from ACMEPy import TransformationEngine
from csmarter_events import *
from insertion_dialog import CougaarMessageDialog

#----------------------------------------------------------------------
class SocietyFactoryServer:
    def __init__(self, path, parent, log, xmlString=None):
      # Should only get a path OR an xmlString, but not both.  If
      # user is parsing an XML file, a path will be passed in; else
      # if user is parsing a string of XML-formatted text, an
      # xmlString will be passed in.
      self._parent = parent
      self.keepRunning = 1
      self.filename = path
      self.log = log
      self.xmlString = xmlString
      
    def Start(self):
      self.keepGoing = self.running = true
      thread.start_new_thread(self.Run, ())

    def Stop(self):
      self.keepGoing = false
      #~ self.log.WriteText("Thread done...\n")
      
    def IsRunning(self):
      return self.running
    
    def Run(self):
      #~ self.log.WriteText( "Thread starting...\n")
      while self.keepGoing:
        evt = None
        society = None
        try:
          if self.filename is not None:
            # Parsing an XML file
            self.filename = "file:" + self.filename  # req'd by the Domlette parser
            society = SocietyFactory(self.filename).parse() 
          elif self.xmlString is not None:
            # Parsing a string of XML-formatted text
            society = SocietyFactory(xmlString=self.xmlString).parse()
        except Exception, args:
          print "ERROR parsing XML document"
          traceback.print_exc()
          self.log.WriteText("*** ERROR parsing XML document; society creation aborted.  See next line for details. ***\n")
          self.log.WriteText("%s\n" % str(args))   
        evt = UpdateSocietyEvent(society)
        wxPostEvent(self._parent, evt)
        self.keepGoing = false  #  ?
      self.running = false
 

#----------------------------------------------------------------------
class SocietyTransformServer:
  
    def __init__(self, society, rulesToApply, parent, log):
      self._parent = parent
      self.keepRunning = 1
      self.ruleList = rulesToApply
      self.log = log
      self.society = society
###
      #print "TransformationRule.name\n-------------------------------------------\n%s " % transform.name
      #print "TransformationRule.rule\n-------------------------------------------\n%s " % transform.rule
      #print "\n-----------------------------------------------------------------------\n"
      
      max_loops = len(self.ruleList) * 3  # limit number of loops to 3 loops per rule
      self.engine = TransformationEngine(self.society, self._parent, max_loops)
      for rule in self.ruleList:
        newRule = RuleText(rule)
        transform = TransformationRule(newRule.description)
        #transform.rule = str(newRule.rule)
        transform.set_rule(newRule)
        self.engine.add_rule(transform)
        #print "TransformationRule.name: %s\n" % transform.name  #  debug
###

    def Start(self):
      self.keepGoing = self.running = true
      thread.start_new_thread(self.Run, ())
#---------------------------------------
    def Stop(self):
      self.keepGoing = false
      self.log.WriteText("transform Thread done...\n")
      
    def IsRunning(self):
      return self.running
#---------------------------------------
    def Run(self):
      #self.log.WriteText( "Thread starting...")
      print "Thread starting..."
      soc = None
      while self.keepGoing:
        print "transforming>>>"
        try:
          soc = self.engine.transform()
        except Exception, args:
          print "ERROR transforming the Society"
          traceback.print_exc()  # prints to stderr
          # We're not sending the following msg to the log file because logging from a thread may be
          # causing a deadlock (see wxPython bug 496697).
          #~ wxLogError("Transformation failed.\n")  # print to log 
          self.log.WriteText("Transformation failed.\n")
          self.log.WriteText("%s\n" % str(args))
          # format traceback and send to log
          #~ stackTrace = traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback)
          #~ traceStr = ''
          #~ for line in stackTrace:
            #~ traceStr = traceStr + line
          #~ wxLogError(traceStr)  # log the exception and the traceback
          # Notify user in a dialog box
          msg = 'ERROR transforming the Society.\nTransformation failed.'
          errorDialog = CougaarMessageDialog(self._parent, "error", msg)
          errorDialog.display()
        
        evt = UpdateSocietyEvent(soc)
        wxPostEvent(self._parent, evt)
        self.keepGoing = False  #  ?
      self.running = false
