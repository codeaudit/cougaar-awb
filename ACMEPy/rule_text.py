#----------------------------------------------------------------------------
# Name:         rule_text.py
# Purpose:      
#
# Author:       ISAT (D. Moore/P. Gardella)
#
# RCS-ID:       $Id: rule_text.py,v 1.8 2003-07-01 16:15:37 pgardella Exp $
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

from string import *
import os

class RuleText:

  def __init__(self, filename, description=None, rule=None):
    self.description = self.rule = ""
    if filename is None:
      # for use when saving a rule (rather than reading one)
      self.description = description
      self.rule = rule
    else:
      # for use when reading a stored rule
      readingRule = False
      in_file = open(filename,"r")
      lineNum = 1
      while True:
        in_line = in_file.readline()
        if in_line == "":
          in_file.close()
          break
        if lineNum == 1 and in_line == "\n": 
          # skip leading blank lines
          continue
        if readingRule:
          self.rule = self.rule + in_line
        elif lineNum == 1 and in_line.lower().find('description:') == 0:
          list = split(in_line, ':')
          self.description = str(list[1]).strip()
          self.rule = self.rule + "# " + self.description + "\n"
        elif in_line.lower().find('rule:') == 0:
          readingRule = True # indicates a Python rule; what follows is rule text
        elif in_line.startswith('#'):
          descFound = self.findDescription(in_line)
          self.rule = self.rule + in_line
          if descFound:
            readingRule = True
        else:
          # There are no leading comments, so create a placeholder
          # description and get on with reading the rule.
          self.description = '<A short descriptive comment should be here.>'
          self.rule = self.rule + in_line
          readingRule = True
        
        lineNum += 1
      
      # write a final newline to assure outdenting in Python
      self.rule = self.rule + "\n"
  
  def saveRule(self, filename):
    f = open(filename, 'w+')
    f.writelines(str(self.rule))
    f.close()
    #~ if self.description == "":
      #~ self.extractDescription()
    self.updateDescription()
    
  def updateDescription(self):
    lines = self.rule.split("\n")
    for line in lines:
      descFound = self.findDescription(line)
      if descFound:
        break
      #~ if self.description == "":
        #~ self.findDescription(line)
      
  def findDescription(self, aLine):
    # If it's not a complete line of #'s, start reading text wherever it starts
    # in the line and use the first sentence (or first line if no sentence) of
    # that text as the description
    index = 0
    end = aLine.find('.')
    for char in aLine:
      if char.isalnum():
        self.description = aLine[index:end].strip()
        return True
      else:
        index += 1
    return False
  
  def getDescription(self):
    return self.description
  
  def __str__(self):
    print "DESC:", self.description
    print "RULE:\n", self.rule
  
