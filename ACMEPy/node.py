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
    #~ self.agents = {}
    self.agentlist = []
    self.facets = []
    self.vm_parameters = []
    self.prog_parameters = []
    self.env_parameters = []
    self.klass = None
    self.rule = str(rule)
    self.nodeAgent = self.add_agent(Agent(self.name, 'org.cougaar.core.agent.SimpleAgent', self.rule))
  
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

  def add_agent(self, agent, klass = None):
    if isinstance(agent, Agent):
      agent.parent = self
      #~ self.agents[agent.name] = agent
      self.agentlist.append(agent)
      return agent
    if isinstance(agent, types.StringType):
      newAgent = Agent(agent)
      #~ self.agents[agent] = newAgent
      self.agentlist.append(newAgent)
      newAgent.parent = self
      return newAgent

  def delete_entity(self):
    '''Deletes itself from node list of parent host.'''
    self.parent.delete_node(self)
  
  def add_entity(self, entity):
    if type(entity) == types.ListType:  # parameters or facets
      self.add_parameters(entity)
    elif isinstance(entity, Component):
      self.add_component(entity)
    elif isinstance(entity, Agent):
      self.add_agent(entity)
    else:
      raise Exception, "Attempting to add unknown Node attribute"
  
  def get_agent(self, index):
    return self.agentlist[index]
  
  def remove_agent(self, agent):
    # Note that this doesn't destroy the agent object, just removes it from this 
    # node's agentlist
    self.agentlist.remove(agent)
  
  def delete_agent(self, agent):
    # Destroys the agent object
    if agent in self.agentlist:
      for component in agent.each_component():
        agent.delete_component(component)
      agent.remove_all_facets()
      self.remove_agent(agent)
      del agent
  
  def has_agent(self, agentName):
    for agent in self.agentlist:
      if agent.name == agentName:
        return True
    return False
  
  def each_facet(self):
    for facet in self.facets: # only for testing iterators
      yield facet

  def remove_facet(self, component_classname):
    print "Node::remove_facet() not implemented"

  def remove_all_facets(self):
    for facet in self.facets: 
      del facet
    self.facets = []

  def delete_facet(self, facet):
    self.facets.remove(facet)
    del facet

  def add_facets(self, facetList):
    for facet in facetList:
      self.add_facet(facet)
  

  def add_facet(self, facet):
    #facet arg could be either a Facet instance or a facet value string of format "key=value"
    if isinstance(facet, Facet):
      facet.parent = self
      self.facets.append(facet)
    elif isinstance(facet, types.DictType):
      fac = Facet( facet )
      fac.parent = self
      self.facets.append(fac)
    else:
      facetDict = {}
      facetList = facet.split("=")
      facetDict[facetList[0]] = facetList[1]
      fac = Facet(facetDict)
      fac.parent = self
      self.facets.append(fac)

  def get_facet(self, index):
    return self.facets[index]

  def get_facet_value(self, key):
    for facet in self.facets:
      if facet.has_key(key):
        return facet[key]
    return None

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

  def add_vm_parameter(self, parameter):
    parameter.parent = self
    self.vm_parameters.append(parameter)

  def add_vm_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.vm_parameters = self.vm_parameters + params

  def add_env_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.env_parameters = self.env_parameters + params

  def add_env_parameter(self, parameter):
    parameter.parent = self
    self.env_parameters.append(parameter)

  def add_prog_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      for each_param in params:
        each_param.parent = self
      self.prog_parameters = self.prog_parameters + params
 
  def add_prog_parameter(self, parameter):
    parameter.parent = self
    self.prog_parameters.append(parameter)

  def remove_parameter(self, param):
    # Assumes that arg "param" is only the key of the parameter, not the value
    i = -1  # we'll return the index of the removed item
    for p in self.vm_parameters[:]:
      i += 1
      args = p.value.split('=')
      if len(p.value) > 0 and (args[0] == param):
        self.vm_parameters.remove(p)
        break
    return i

  def delete_parameter(self, param):
    if isinstance(param, VMParameter):
      self.vm_parameters.remove(param)
    elif isinstance(param, EnvParameter):
      self.env_parameters.remove(param)
    elif isinstance(param, ProgParameter):
      self.prog_parameters.remove(param)
    else:
      raise Exception, "Attempting to delete parameter of unknown type"

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
 
  def updateNameServerParam(self, nameServer):
    nameServerParam = "-Dorg.cougaar.name.server="
    for vmParam in self.vm_parameters:
      if vmParam.value.startswith(nameServerParam):
        vmParam.value = nameServerParam + nameServer + ":8888:5555"
        break
    
  
  def clone(self):
    node = Node(self.name)
    node.parent = self.parent
    node.klass = self.klass
    node.rule = self.rule
    for agent in self.agentlist:
      if agent != self.nodeAgent:
        node.add_agent(agent.clone())
    node.add_parameters(self.clone_parameters('vm'))
    node.add_prog_parameters(self.clone_parameters('prog'))
    node.add_env_parameters(self.clone_parameters('env'))
    return node
  
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
  
  def to_xml(self):
    xml = "  <node name='"+ self.name + "'>\n"
    if self.klass is not None:
      xml = xml + "   <class>" + self.klass + "</class>\n"
    # add parameters and agents
    for facet in self.facets:
      xml = xml + facet.to_xml()
    for p in self.prog_parameters[:]:
      xml = xml + p.to_xml()
    for p in self.env_parameters[:]:
      xml = xml + p.to_xml()
    for p in self.vm_parameters[:]:
      xml = xml + p.to_xml()
    for agent in self.agentlist:
      if agent == self.nodeAgent:
        for component in agent.components:
          xml = xml + component.to_xml()
      else:
        xml = xml + agent.to_xml()

    xml = xml +  "  </node>\n"
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

  def each_agent(self, inclNodeAgent=False):
    for agent in self.agentlist: # only for testing iterators
      if inclNodeAgent: 
        yield agent
      elif agent != self.nodeAgent:
        yield agent


