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
    self.prev_parent = None
    self.society = None
    self.uic = None
    self.klass = klass
    self.facets = []
    self.components = []
    self.rule = str(rule)
    self.isExcluded = False
      
  def __str__(self):
    return "Agent:"+self.name+":RULE:"+self.rule
    
  def add_entity(self, entity, orderAfterObj=None, isCopyOperation=False):
    if type(entity) == types.ListType:  # will be a list of Facet objects
      for each_thing in entity:
        self.add_facet(each_thing)
    elif isinstance(entity, Component):
      entity.prev_parent = entity.parent
      isReordering = False
      print "isCopyOperation:", isCopyOperation  # prg debug
      if entity.parent == self and not isCopyOperation:  
        print "It's a reordering w/in the same agent" # prg debug  ## Just take out 'print' stmt ##
        self.remove_component(entity)  # we'll be adding it back again in a new location
        isReordering = True
        #~ return self.add_component(entity, orderAfterObj, True)
      print "isReordering =", isReordering  # prg debug
      return self.add_component(entity, orderAfterObj, isReordering)
    else:
      raise Exception, "Attempting to add unknown Node attribute"
  
  def delete_entity(self):
    self.parent.delete_agent(self)
  
  def delete_from_prev_parent(self):
    if self.prev_parent is not None:
      self.prev_parent.remove_agent(self)
    else:
      self.remove_entity()
  
  def has_changed_parent(self):
    return self.parent != self.prev_parent
  
  def remove_entity(self):
    self.parent.remove_agent(self)
  
  ##
  # Iteratively returns each facet on this Agent instance as a Dictionary
  #
  def each_facet(self):
    for facet in self.facets: 
      yield facet

  def remove_facet(self, keyValueString):
    for facet in self.facets:
      if facet.contains_entry(keyValueString):
        facet.remove_entry(keyValueString)
        self.society.isDirty = True
        break
  
  def replace_facet(self, oldEntry, newEntry):
    for facet in self.facets:
      if facet.contains_entry(oldEntry):
        facet.replace_entry(oldEntry, newEntry)
        self.society.isDirty = True
        break
  
  def remove_all_facets(self):
    for facet in self.facets:
      del facet
      self.society.isDirty = True
    self.facets = []

  def delete_facet(self, facet):
    self.facets.remove(facet)
    self.society.isDirty = True

  def add_facet(self, facet, rule='BASE'):
    #facet arg could be either a Facet instance or a facet value string
    if isinstance(facet, Facet):
      facet.parent = self
      facet.rule = rule
      self.facets.append(facet)
      if self.society is not None:
        self.society.isDirty = True
    else:
      fac = Facet(facet)
      self.add_facet(fac, rule)

  ##
  # Adds the list of facets passed in as the argument to this
  # agent's list of facets.  Dupes are ignored; i.e., not added.
  #
  # facetList:: [List] a list of facets
  # 
  def add_facets(self, facetList):
    if facetList is not None and len(facetList) > 0:
      # check for dupes
      for facet in facetList:
        if not isinstance(facet, Facet):
          facet = Facet(facet)
        keyList = facet.keys()
        for key in keyList:
          values = self.get_facet_values(key)
          if len(values) > 0:     # check for a key match
            match = False
            for value in values:  # have a key match; check if value is the same
              if value == facet.get(key):
                match = True  # it's a dupe
                break
            if not match:
              # it's a new key=value pair for this host
              self.add_facet(key + '=' + facet.get(key))
          else:  # no key match; this is a new key=value pair for this host
            self.add_facet(key + '=' + facet.get(key))
  
  def get_facet(self, index):
    return self.facets[index]

  ##
  # Returns the list of facets on this host.
  #
  def get_facets(self):
    return self.facets
  
  ##
  # Returns True if this agent has a facet matching the facet value
  # specified in the argument; otherwise, returns False.
  #
  # keyValuePair:: [String] Facet in 'key=value' format
  #
  def has_facet(self, keyValuePair):
    for facet in self.each_facet():
      if facet.contains_entry(keyValuePair):
        return True
    return False
  
  ##
  # Returns a list containing all the values for the specified key
  #
  def get_facet_values(self, key):
    valList = []
    for facet in self.facets:
      if facet.has_key(key):
        valList.append(facet.get(key))
    return valList

  ##
  # Returns a list containing all the facet keys used in this agent
  # (minus duplicates).
  #
  def get_facet_keys(self):
    facetKeyList = []
    for facet in self.facets:
      facetKeys = facet.keys()
      for key in facetKeys:
        if key not in facetKeyList:  # eliminate dupes
          facetKeyList.append(key)
    return facetKeyList
  
  def each_component(self):
    for component in self.components:
      yield component

  def remove_component(self, component_classname):
    for c in self.components:
      if (c.klass == component_classname):
        self.components.remove(c)
        self.society.isDirty = True

  def delete_component(self, component):
    # Destroys the component object
    if component in self.components:
      for argument in component.each_argument():
        component.delete_argument(argument)
      self.components.remove(component)
      del component
      self.society.isDirty = True
    else:
      print "WARNING: Attempt to delete non-existent Component. Could be an error."

  def add_component(self, component, orderAfterObj=None, reorder=False):
    if isinstance(component, Component):
      isDupe = False
      # Check if we've already got a component by that name; but if this
      # is a reordering, dupes are ok, so we leave isDupe set to false
      #~ if not reorder and self.society is not None:
      if not reorder:
        for existingComp in self.components:
          if component.name == existingComp.name:
            isDupe = True
            break
      if not isDupe:
        # We don't have it, so add it
        if orderAfterObj is not None:
          # User  wants to add it at a particular place
          index = -1
          if isinstance(orderAfterObj, Component) and orderAfterObj in self.components:
            index = self.components.index(orderAfterObj)
          self.components.insert(index + 1, component)
        else:
          # User doesn't care where it's added , so add at the end
          self.components.append(component)
        component.parent = self
        if self.society is not None:
          self.society.isDirty = True
        return component
      else:
        print "Unable to add duplicate component:", component.name
        return None
    elif isinstance(component, types.StringType):
      newComp = Component(component)
      return self.add_component(newComp)
    else:
      raise Exception, "Attempting to add unknown type as a component"

  def get_component(self, index):
    if len(self.components) > index:
      return self.components[index]
    return None
  
  def has_component(self, componentName):
    for component in self.components:
      if component.getStrippedName() == componentName:
        return True
    return False
  
  def set_rule(self, newRule):
    self.rule = str(newRule)
    self.society.isDirty = True
  
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
    self.society.isDirty = True
  
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
      self.society.isDirty = True
    return self.name
  
  def isNodeAgent(self):
    if self == self.parent.nodeAgent:
      return True
    return False
  
  def clone(self, inclComponents=True, parent=None):
    agent = Agent(self.name, self.klass, self.rule)
    agent.uic = self.uic
    agent.isExcluded = self.isExcluded
    agent.parent = parent
    agent.society = parent.society
    if inclComponents:
      for component in self.components:
        new_component = component.clone(agent)
        agent.add_component(new_component)
    for facet in self.facets:
      new_facet = facet.clone()
      agent.add_facet(new_facet)
      new_facet.parent = agent
    return agent
    
  def set_society(self, society):
    self.society = society
    self.society.isDirty = True
  
  def getType(self):
    return 'agent'
  
  def to_xml(self, hnaOnly=False):
    tab = ' ' * 4
    indent = tab * 3
    xml = indent + "<agent name='"+ self.name + "'"
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
        xml = xml + facet.to_xml(4)
      for component in self.components:
        xml = xml + component.to_xml()
      xml = xml +  indent + "</agent>\n"
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
