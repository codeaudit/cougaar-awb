#Component.py
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
from argument import Argument

class Component:
   # Construct a plugin
   #
   # data:: [String] the plugin data
   #
  def __init__(self, name=None, klass=None, priority = None, order=None, insertionpoint=None, rule='BASE'):
    self.name = name
    self.klass = klass
    self.priority = priority
    self.order = order
    self.insertionpoint = insertionpoint
    self.arguments = []
    self.rule = str(rule)
    
  def add_argument(self, argument):
    if isinstance(argument, Argument):
      self.arguments.append(argument)

  def __str__(self):
    return "Component:"+self.name+":RULE:"+self.rule


  def clone(self):
    return Plugin(self.name)
  def to_xml(self):
    xml =  "<component name='"+str(self.name)+"' class='"+str(self.klass)+"' priority='"+str(self.priority)+"' order='"+str(self.order)+"' insertionpoint='"+str(self.insertionpoint)+"'>\n"
    for a in self.arguments[:]:
      xml = xml + a.to_xml()
    xml = xml + "</component>\n"
    return xml
    
  def to_python(self):
    script = "component = Component(name='"+self.name+"', klass='"+self.klass+"', priority='"+self.priority+"', order='"+self.order+"', insertionpoint='"+self.insertionpoint+"')\n"
    script = script + "agent.add_component(component)\n"
    for a in self.arguments:
      script = script + a.to_python()
    return script