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
  def __init__(self, name=None, klass=None):
    self.name = name
    self.node = None
    self.uic = None
    self.klass = klass
    self.cloned = False
    self.components = []

      
  def __str__(self):
    return "Agent:"+self.name
    
  def add_component(self, component):
  # plugin is either an actual plugin or a string representing the data for a plugin.
  # handle accordingly!
    if isinstance(component, Component):
      self.components.append(component)
    else:
      self.components.append(Component(component))

  def host(self):
    return agent.node.host

  def clone(self):
    agent = Agent(self.name)
    agent.node = self.node
    agent.cloned = True
    agent.uic = self.uic
    for component in self.components:
      agent.add_component(component.clone())
    return agent
    

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

