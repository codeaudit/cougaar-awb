#Node.py
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
from agent import Agent
from parameter import *
from component import *
from facet import Facet

class Node:
  def __init__(self, name=None, rule='BASE'):
    self.name = name
    self.parent = None
    self.prev_parent = None
    self.agentlist = []
    self.facets = []
    self.vm_parameters = []
    self.prog_parameters = []
    self.env_parameters = []
    self.klass = None
    self.rule = str(rule)
    self.society = None
    self.isExcluded = False
    self.nodeAgent = self.add_agent(Agent(self.name, 'org.cougaar.core.agent.SimpleAgent', "Auto-Create(Node Agent)"))
  
  def __str__(self):
    return "Node:"+self.name+":RULE:"+self.rule
  
  def set_attribute(self, attribute, value):
    # both args must be strings
    value = str(value)
    if attribute.lower() == 'name':
      self.name = value
    elif attribute.lower() == 'klass':
      self.klass = value
    elif attribute.lower() == 'rule':
      self.rule = value
    elif attribute.lower() == 'prog_parameter':
      self.prog_parameters[0] = ProgParameter(value)
    else:
      raise Exception, "Attempting to set unknown Node attribute: " + attribute.lower()
    if self.society is not None:
      self.society.isDirty = True

  def add_agent(self, agent, orderAfterObj=None, reorder=False):
    if isinstance(agent, Agent):
      isDupe = False
      # Check if we've already got an agent by that name; but if this
      # is a reordering, dupes are ok, so we leave isDupe set to false
      if not reorder and self.society is not None:
        for existingAgent in self.society.each_agent():
          if agent.name == existingAgent.name:
            isDupe = True
            break
      if not isDupe:
        # We don't have it, so add it
        if orderAfterObj is not None:
          # User  wants to add it at a particular place
          index = -1
          if isinstance(orderAfterObj, Agent) and orderAfterObj in self.agentlist:
            index = self.agentlist.index(orderAfterObj)
          self.agentlist.insert(index + 1, agent)
        else:
          # User doesn't care where it's added , so add at the end
          self.agentlist.append(agent)
        agent.parent = self
        agent.society = self.society
        if self.society is not None:
          self.society.isDirty = True
        return agent
      else:
        print "Unable to add duplicate agent:", agent.name
        return None
    if isinstance(agent, types.StringType):
      newAgent = Agent(agent)
      return self.add_agent(newAgent)

  def add_entity(self, entity, orderAfterObj=None, isCopyOperation=False):
    if type(entity) == types.ListType:  # parameters or facets
      self.add_parameters(entity)
    elif isinstance(entity, Component):
      self.add_component(entity)
    elif isinstance(entity, Agent):
      entity.prev_parent = entity.parent
      if entity.society is not None and entity.society.name == self.society.name and not isCopyOperation:  
        # it's a reordering w/in same society
        if entity.parent == self:
          # it's a reordering w/in the same node
          self.remove_agent(entity)  # we'll be adding it back again in a new location
        return self.add_agent(entity, orderAfterObj, True)
      self.society.adjustAgentCount(True)  # True = increment by one
      return self.add_agent(entity, orderAfterObj)
    else:
      raise Exception, "Attempting to add unknown Node attribute"
  
  def delete_entity(self, saveAgents=False):
    '''Deletes itself from node list of parent host.'''
    self.parent.delete_node(self, saveAgents)
  
  def delete_from_prev_parent(self, saveAgents=False):
    if self.prev_parent is not None:
      self.prev_parent.remove_node(self)
    else:
      self.remove_entity()
  
  def has_changed_parent(self):
    return self.parent != self.prev_parent
  
  def remove_entity(self):
    self.parent.remove_node(self)
  
  def remove_agent(self, agent):
    # Note that this doesn't destroy the agent object, just removes it from this 
    # node's agentlist
    if agent in self.agentlist:
      self.agentlist.remove(agent)
      if self.society is not None:
        self.society.isDirty = True
  
  def delete_agent(self, agent):
    # Destroys the agent object
    if agent in self.agentlist:
      for component in agent.each_component():
        agent.delete_component(component)
      agent.remove_all_facets()
      self.remove_agent(agent)
      del agent
      if self.society is not None:
        self.society.isDirty = True
  
  def get_agent(self, index):
    return self.agentlist[index]
  
  def get_node_agent(self):
    return self.nodeAgent
  
  def has_agent(self, agentName):
    for agent in self.agentlist:
      if agent.name == agentName:
        return True
    return False
  
  def countAgents(self, onlyIfIncluded=False, inclNodeAgent=False):
    nodeAgentAdjustment = 1
    if inclNodeAgent:
      nodeAgentAdjustment = 0
    if onlyIfIncluded:
      numAgents = 0
      for agent in self.agentlist:
        if not agent.isExcluded:
          numAgents += 1
      return numAgents - nodeAgentAdjustment
    return len(self.agentlist) - nodeAgentAdjustment
  
  ##
  # Iteratively returns each facet on this Node instance as a Dictionary
  #
  def each_facet(self):
    for facet in self.facets: 
      yield facet

  def remove_facet(self, keyValueString):
    for facet in self.facets:
      if facet.contains_entry(keyValueString):
        facet.remove_entry(keyValueString)
        if self.society is not None:
          self.society.isDirty = True
        break
  
  def replace_facet(self, oldEntry, newEntry):
    for facet in self.facets:
      if facet.contains_entry(oldEntry):
        facet.replace_entry(oldEntry, newEntry)
        if self.society is not None:
          self.society.isDirty = True
        break
  
  def remove_all_facets(self):
    for facet in self.facets: 
      del facet
      if self.society is not None:
        self.society.isDirty = True
    self.facets = []

  def delete_facet(self, facet):
    self.facets.remove(facet)
    del facet
    if self.society is not None:
      self.society.isDirty = True

  ##
  # Adds the list of facets passed in as the argument to this
  # node's list of facets.  Dupes are ignored; i.e., not added.
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
  
  def add_facet(self, facet, rule='BASE'):
    #facet arg could be either a Facet instance or a facet value string of format "key=value"
    if isinstance(facet, Facet):
      facet.rule = rule
      facet.parent = self
      self.facets.append(facet)
      if self.society is not None:
        self.society.isDirty = True
    else:  # it's a Dictionary or String type
      fac = Facet(facet)
      self.add_facet(fac, rule)
  
  def get_facet(self, index):
    return self.facets[index]
  
  def get_facet_values(self, key):
    valList = []
    for facet in self.facets:
      if facet.has_key(key):
        valList.append(facet.get(key))
    return valList
  
  def add_component(self, component):
    self.nodeAgent.add_component(component)
  
  def delete_component(self, component):
    self.nodeAgent.delete_component(component)
  
  def get_component(self, index):
    return self.nodeAgent.get_component(index)
  
  def override_parameter(self, param, value):
    # assumes that "param" is a string like "-D..."
    #  below only matches on "param"
    self.remove_parameter(param)
    parameter = VMParameter(param+"="+value) #construct a new one
    parameter.parent = self
    self.vm_parameters.append(parameter)
    if self.society is not None:
      self.society.isDirty = True

  def add_vm_parameter(self, parameter):
    parameter.parent = self
    self.vm_parameters.append(parameter)
    if self.society is not None:
      self.society.isDirty = True

  def add_vm_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.vm_parameters = self.vm_parameters + params
      if self.society is not None:
        self.society.isDirty = True

  def add_env_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.env_parameters = self.env_parameters + params
      if self.society is not None:
        self.society.isDirty = True

  def add_env_parameter(self, parameter):
    parameter.parent = self
    self.env_parameters.append(parameter)
    if self.society is not None:
      self.society.isDirty = True

  def add_prog_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.prog_parameters = self.prog_parameters + params
      if self.society is not None:
        self.society.isDirty = True
 
  def add_prog_parameter(self, parameter):
    parameter.parent = self
    self.prog_parameters.append(parameter)
    if self.society is not None:
      self.society.isDirty = True

  def remove_parameter(self, param):
    # Assumes that arg "param" is only the key of the parameter, not the value
    i = -1  # we'll return the index of the removed item
    for p in self.vm_parameters[:]:
      i += 1
      args = p.value.split('=')
      if len(p.value) > 0 and (args[0] == param):
        self.vm_parameters.remove(p)
        self.society.isDirty = True
        break
    return i

  def remove_all_parameters(self):
    self.vm_parameters = []
    self.env_parameters = []
    self.prog_parameters = []
    self.society.isDirty = True
  
  def delete_parameter(self, param):
    if isinstance(param, VMParameter):
      self.vm_parameters.remove(param)
    elif isinstance(param, EnvParameter):
      self.env_parameters.remove(param)
    elif isinstance(param, ProgParameter):
      self.prog_parameters.remove(param)
    else:
      raise Exception, "Attempting to delete parameter of unknown type"
    self.society.isDirty = True

  def add_parameter(self, param):
    param.parent = self
    if isinstance(param, VMParameter):
      self.add_vm_parameter(param)
    elif isinstance(param, ProgParameter):
      self.add_prog_parameter(param)
    elif isinstance(param, EnvParameter):
      self.add_env_parameter(param)
  
  def add_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType) and len(params) > 0:
      if isinstance(params[0], VMParameter):
        self.add_vm_parameters(params)
      elif isinstance(params[0], ProgParameter):
        self.add_prog_parameters(params)
      elif isinstance(params[0], EnvParameter):
        self.add_env_parameters(params)
      else:  # must be a facet
        self.add_facets(params)
  
  def set_rule(self, newRule):
        self.rule = str(newRule)
        self.society.isDirty = True
 
  def updateNameServerParam(self, nameServer):
    # Updates the namerserver parameter; for use whenever the nameserver changes
    nameServerParam = "-Dorg.cougaar.name.server="
    for vmParam in self.vm_parameters:
      if vmParam.value.startswith(nameServerParam):
        vmParam.value = nameServerParam + nameServer
        self.society.isDirty = True
        break
  
  ##
  # Renames this node if the new name is not already taken by another node.
  # Returns the node's name; will be the old name if the newName was 
  # already taken, or the newName if the rename was successful.
  #
  # newName:: [String] the new name for this node
  #
  def rename(self, newName):
    if not self.society.has_node(newName):
      # name is not taken, so it's OK
      self.name = newName
      self.nodeAgent.rename(newName)
      self.society.isDirty = True
    return self.name
  
  def clone(self, inclComponents=True, parent=None):
    node = Node(self.name)
    node.klass = self.klass
    node.rule = self.rule
    node.isExcluded = self.isExcluded
    node.parent = parent
    node.society = parent.parent
    for agent in self.agentlist:
      if agent != self.nodeAgent:
        newAgent = agent.clone(inclComponents, node)
        node.add_agent(newAgent)
    if inclComponents:
      node.add_parameters(self.clone_parameters('vm'))
      node.add_prog_parameters(self.clone_parameters('prog'))
      node.add_env_parameters(self.clone_parameters('env'))
    for facet in self.facets:
      new_facet = facet.clone()
      node.add_facet(new_facet)
      new_facet.parent = node
    return node
  
  def set_society(self, society):
    self.society = society
    for agent in self.agentlist:
      agent.set_society(society)
    self.society.isDirty = True
  
  def clone_parameters(self, type):
    dupe_params = []
    paramsList = self.vm_parameters
    if type == 'prog':
      paramsList = self.prog_parameters
    elif type == 'env':
      paramsList = self.env_parameters
    for each_param in paramsList:
      dupe_params.append(each_param.clone())
    return dupe_params
  
  def each_agent(self, inclNodeAgent=False):
    for agent in self.agentlist: # only for testing iterators
      if inclNodeAgent: 
        yield agent
      elif agent != self.nodeAgent:
        yield agent
  
  def to_xml(self, hnaOnly=False, inclNameserverFacet=False):
    tab = ' ' * 4
    indent = tab * 2
    xml = indent + "<node name='"+ self.name + "'"
    if len(self.agentlist) == 0 and len(self.facets) == 0 and (hnaOnly or (self.klass is None  \
            and len(self.prog_parameters) == 0 and len(self.env_parameters) == 0 \
            and len(vm_parameters) == 0)):
      xml = xml + "/>\n"
      return xml
    xml = xml + ">\n"
    if not hnaOnly:
      if self.klass is not None:
        indent = tab * 3
        xml = xml + indent + "<class>" + self.klass + "</class>\n"
      # add parameters and agents
      for p in self.prog_parameters[:]:
        xml = xml + indent + p.to_xml()
      for p in self.env_parameters[:]:
        xml = xml + indent + p.to_xml()
      for p in self.vm_parameters[:]:
        xml = xml + indent + p.to_xml()
    if inclNameserverFacet:
      indent = tab * 3
      xml = xml + indent + "<facet role='NameServer'/>\n"
    for facet in self.facets:
      xml = xml + facet.to_xml(3)
    for agent in self.agentlist:
      if agent == self.nodeAgent:
        for component in agent.components:
          xml = xml + component.to_xml(3)
      else:
        xml = xml + agent.to_xml(hnaOnly)
    indent = tab * 2
    xml = xml +  indent + "</node>\n"
    return xml

  def to_python(self):
    script = "node = Node('"+self.name+"')\n"
    script = script + "host.add_node(node)\n"
    for p in self.prog_parameters[:]:
      script = script + "node.add_prog_parameter('" + str(p) +"')\n"
    for p in self.env_parameters[:]:
      script = script + "node.add_env_parameter('" + str(p) +"')\n"
    for p in self.vm_parameters[:]:
      script = script + "node.add_vm_parameter('" + str(p) +"')\n"
    for agent in self.agentlist:
      script = script + agent.to_python()  
    return script
  
  def to_ruby(self):
    script = "    host.add_node('" + self.name + "') do |node|\n"
    if self.klass is not None:
      script = script + "      node.classname = '" + self.klass + "'\n"
    for p in self.vm_parameters:
      script = script + "      node.add_parameter('" + p.value + "')\n"
    for p in self.prog_parameters:
      script = script + "      node.add_prog_parameter('" + p.value + "')\n"
    for p in self.env_parameters:
      script = script + "      node.add_env_parameter('" + p.value + "')\n"
    for facet in self.facets:
      script = script + "      node.add_facet do |facet|\n"
      script = script + facet.to_ruby(4)
      script = script + "      end\n"
    for c in self.nodeAgent.each_component():
      script = script + c.to_ruby(4)
    for agent in self.each_agent(False):  # exclude node agent
      script = script + agent.to_ruby()
    script = script + "    end\n"
    return script
