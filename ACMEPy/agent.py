#Agent.py
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
from __future__ import generators
import types
from component import Component

class Agent:
  def __init__(self, name=None, klass=None, rule='BASE'):
    self.name = name
    self.node = None
    self.uic = None
    self.klass = klass
    self.cloned = False
    self.components = []
    self.rule = str(rule)
    self.dupe = None

      
  def __str__(self):
    return "Agent:"+self.name+":RULE:"+self.rule
    
  def delete_entity(self):
    self.node.delete_agent(self)
  
  def each_component(self):
    for component in self.components: # only for testing iterators
      yield component

  def remove_component(self, component_classname):
    for c in self.components:
      if (c.klass == component_classname):
        self.components.remove(c)

  def delete_component(self, component):
    self.components.remove(component)

  def add_component(self, component):
  # plugin is either an actual plugin or a string representing the data for a plugin.
  # handle accordingly!
    if isinstance(component, Component):
      component.parent = self
      self.components.append(component)
    else:
      comp = Component(component)
      comp.parent = self
      self.components.append(comp)

  def get_component(self, index):
    return self.components[index]

  def set_rule(self, newRule):
        self.rule = str(newRule)

  def set_attribute(self, attribute, value):
    # both args must be strings
    if attribute.lower() == 'name':
      self.name = value
    elif attribute.lower() == 'node':
      self.node == value
    elif attribute.lower() == 'uic':
      self.uic == value
    elif attribute.lower() == 'klass':
      self.klass = value
    elif attribute.lower() == 'rule':
      self.rule = value
    else:
      raise Exception, "Attempting to set unknown Agent attribute: " + attribute.lower()
  
  def host(self):
    return agent.node.host

  def clone(self):
    print "Cloning Agent"
    if self.dupe is None:
      self.dupe = Agent(self.name)
      self.dupe.node = self.node
      self.dupe.cloned = True
      self.dupe.uic = self.uic
      for component in self.components:
        self.dupe.add_component(component.clone())
    return self.dupe
    
  def each_component(self):
    for component in self.components: # iterators
      yield component

  def to_xml(self):
    xml = "  <agent name='"+ self.name + "' class='"+str(self.klass)+"'>\n"
    for component in self.components:
      xml = xml + component.to_xml()
    xml = xml +  "  </agent>\n"
    return xml   

  def to_python(self):
    script = "agent = Agent('"+self.name+"')\n"
    script = script + "node.add_agent(agent)\n"
    for c in self.components:
      script = script + c.to_python()
    return script

