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
from facet import Facet

class Agent:
  def __init__(self, name=None, klass=None, rule='BASE'):
    self.name = name
    self.parent = None
    self.society = None
    self.uic = None
    self.klass = klass
    self.facets = []
    self.components = []
    self.rule = str(rule)
      
  def __str__(self):
    return "Agent:"+self.name+":RULE:"+self.rule
    
  def add_entity(self, entity):  
    if type(entity) == types.ListType:  # will be a list of Facet objects
      for each_thing in entity:
        self.add_facet(each_thing)
    elif isinstance(entity, Component):
      self.add_component(entity)
    else:
      raise Exception, "Attempting to add unknown Agent attribute"
  
  def delete_entity(self):
    self.parent.delete_agent(self)
  
  def remove_entity(self):
    self.parent.remove_agent(self)
  
  ##
  # Iteratively returns each facet on this Agent instance as a Dictionary
  #
  def each_facet(self):
    for facet in self.facets: 
      yield facet

  def remove_facet(self, component_classname):
    print "Agent::remove_facet() not implemented"

  def remove_all_facets(self):
    for facet in self.facets:
      del facet
    self.facets = []

  def delete_facet(self, facet):
    self.facets.remove(facet)

  def add_facet(self, facet):
    #facet arg could be either a Facet instance or a facet value string
    if isinstance(facet, Facet):
      facet.parent = self
      self.facets.append(facet)
    else:
      fac = Facet(facet)
      fac.parent = self
      self.facets.append(fac)

  def get_facet(self, index):
    return self.facets[index]

  def get_facet_values(self, key):
    valList = []
    for facet in self.facets:
      if facet.has_key(key):
        valList.append(facet.get(key))
    return valList

  def each_component(self):
    for component in self.components:
      yield component

  def remove_component(self, component_classname):
    for c in self.components:
      if (c.klass == component_classname):
        self.components.remove(c)

  def delete_component(self, component):
    # Destroys the component object
    if component in self.components:
      for argument in component.each_argument():
        component.delete_argument(argument)
      self.components.remove(component)
      del component
    else:
      print "WARNING: Attempt to delete non-existent Component. Could be an error."

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

  def has_component(self, componentName):
    for component in self.components:
      if component.getStrippedName() == componentName:
        return True
    return False
  
  def set_rule(self, newRule):
        self.rule = str(newRule)

  def set_attribute(self, attribute, value):
    # both args must be strings
    if attribute.lower() == 'name':
      self.name = value
    elif attribute.lower() == 'parent':
      self.parent == value
    elif attribute.lower() == 'uic':
      self.uic == value
    elif attribute.lower() == 'klass':
      self.klass = value
    elif attribute.lower() == 'rule':
      self.rule = value
    else:
      raise Exception, "Attempting to set unknown Agent attribute: " + attribute.lower()
  
  def host(self):
    return self.parent.parent

  ##
  # Renames this agent if the new name is not already taken by another agent.
  # Returns the agent's name; will be the old name if the
  # newName was already taken, or the newName if the rename was successful
  #
  # newName:: [String] the new name for this agent
  #
  def rename(self, newName):
    agentNameCheck = self.society.get_agent(newName)
    if agentNameCheck is None:
      # name is not taken, so it's OK
      self.name = newName
    return self.name
  
  def isNodeAgent(self):
    if self == self.parent.nodeAgent:
      return True
    return False
  
  def clone(self):
    agent = Agent(self.name, self.klass, self.rule)
    agent.uic = self.uic
    for component in self.components:
      new_component = component.clone()
      agent.add_component(new_component)
      new_component.parent = agent
    for facet in self.facets:
      new_facet = facet.clone()
      agent.add_facet(new_facet)
      new_facet.parent = agent
    return agent
    
  def set_society(self, society):
    self.society = society
  
  def to_xml(self, hnaOnly=False):
    xml = "   <agent name='"+ self.name + "'"
    if hnaOnly:
      xml = xml + "/>\n"
      return xml
    else:
      if self.klass is not None:
        xml = xml + " class='"+str(self.klass)+"'"
      if len(self.facets) == 0 and len(self.components) == 0:
        xml = xml + "/>\n"
        return xml
      else:
        xml = xml + ">\n"
      for facet in self.facets:
        xml = xml + facet.to_xml()
      for component in self.components:
        xml = xml + component.to_xml()
      xml = xml +  "   </agent>\n"
      return xml   

  def to_python(self):
    script = "agent = Agent('"+self.name+"')\n"
    script = script + "node.add_agent(agent)\n"
    for f in self.facets:
      script = script + f.to_python()
    for c in self.components:
      script = script + c.to_python()
    return script
  
  def to_ruby(self):
    if self.klass is None and self.uic is None and len(self.facets) == 0 and len(self.components) == 0:
      script = "      node.add_agent('" + self.name + "')\n"
    else:
      script = "      node.add_agent('" + self.name + "') do |agent|\n"
      if self.klass is not None:
        script = script + "        agent.classname = '" + self.klass + "'\n"
      if self.uic is not None:
        script = script + "        agent.uic = '" + self.uic + "'\n"
      for facet in self.facets:
        script = script + "        agent.add_facet do |facet|\n"
        script = script + facet.to_ruby(5)
        script = script + "        end\n"
      for c in self.components:
        script = script + c.to_ruby(5)
      script = script + "      end\n"
    return script
