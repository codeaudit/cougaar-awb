#argument.py
#
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

class Argument:
  
  def __init__(self, value, rule='BASE'):
    self.name = value
    self.rule = str(rule)
    self.parent = None
    self.prev_parent = None
  
  def __str__(self):
    return "Argument:"+self.name+":RULE:"+self.rule

  def set_attribute(self, attribute, value):
    # both args must be strings
    if attribute.lower() == 'value':
      self.name = value
    elif attribute.lower() == 'rule':
      self.rule = value
    else:
      raise Exception, "Attempting to set unknown Argument attribute: " + attribute.lower()
    self.parent.parent.society.isDirty = True

  def delete_entity(self):
    self.parent.delete_argument(self)
  
  def delete_from_prev_parent(self):
    if self.prev_parent is not None:
      self.prev_parent.delete_argument(self)
    else:
      self.delete_entity()
  
  def has_changed_parent(self):
    return self.parent != self.prev_parent
  
  def set_rule(self, newRule):
    self.rule = str(newRule)
    self.parent.parent.society.isDirty = True
  
  def rename(self, newName):
    self.name = newName
    self.parent.parent.society.isDirty = True
    return self.name
  
  def clone(self):
    return Argument(self.name, self.rule)
  
  def to_xml(self, numTabs=5):
    tab = ' ' * 4
    indent = tab * numTabs
    return indent + "<argument>" + str(self.name) + "</argument>\n"
    
  def to_python(self):
    script = "argument = Argument('"+self.name+"','"+self.rule+"')\n"
    script = script + "component.add_argument(argument)\n"
    return script
  
  def to_ruby(self, numTabs):
    indent = "  " * numTabs
    return indent + "c.add_argument('" + self.name + "')\n"
