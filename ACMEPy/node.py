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

class Node:
  def __init__(self, name=None, rule='BASE'):
    self.name = name
    self.host = None
    self.agents = {}
    self.agentlist = []
    self.components = {}
    self.componentlist = []
    self.vm_parameters = []
    self.prog_parameters = []
    self.env_parameters = []
    self.klass = None
    self.rule = str(rule)
    self.dupe = None
    
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
      agent.node = self
      self.agents[agent.name] = agent
      self.agentlist.append(agent)
      return agent
    if isinstance(agent, types.StringType):
      newAgent = Agent(agent)
      self.agents[agent] = newAgent
      self.agentlist.append(newAgent)
      self.agents[agent].node = self
      return self.agents[agent]

  def get_agent(self, index):
    #for buddy in self.agentlist:
      #print buddy.name
    return self.agentlist[index]

  def add_component(self, component):
    if isinstance(component, Component):
      component.parent = self
      self.components[component.name] = component
      self.componentlist.append(component)
      return component
    if isinstance(component, types.StringType):
      newComponent = Component(component)
      self.components[component] = newComponent
      self.componentlist.append(newComponent)
      self.components[component].parent = self
      return self.components[component]

  def get_component(self, index):
    #for comp in self.componentlist:
      #print comp.name
    return self.componentlist[index]

  def override_parameter(self, param, value):
    # assumes that "param" is a string like "-D..."
    #  below only matches on "param"
    self.remove_parameter(VMParameter(param+"="+value))
    self.vm_parameters.append(VMParameter(param+"="+value))

  def add_vm_parameter(self, parameter):
    self.add_parameter(parameter)

  def add_vm_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      #for eachItem in params:
      self.vm_parameters = self.vm_parameters + params

  def add_env_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      self.env_parameters = self.env_parameters + params

  def add_env_parameter(self, parameter):
    self.env_parameters.append(parameter)

  def add_prog_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      self.prog_parameters = self.prog_parameters + params
 
  def add_prog_parameter(self, parameter):
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

  def add_parameter(self, param):
    self.vm_parameters.append(param)

  def add_parameters(self, params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      self.vm_parameters = self.vm_parameters + params

  def set_rule(self, newRule):
        self.rule = str(newRule)
 
  def clone(self):
    print "Cloning Node"
    if self.dupe is None:
      self.dupe = Node(self.name)
      self.dupe.host = self.host
      self.dupe.klass = self.klass
      self.dupe.rule = self.rule
      for agent in self.agentlist:
        self.dupe.add_agent(agent.clone())
      self.dupe.add_parameters(self.clone_parameters('vm'))
      self.dupe.add_prog_parameters(self.clone_parameters('prog'))
      #node.add_env_parameters(self.clone_parameters('env'))
      for comp in self.componentlist:
        self.dupe.add_component(comp.clone())
  
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
    xml = xml + "   <class>" + self.klass + "</class>\n"
    # add parameters and agents
    for p in self.prog_parameters[:]:
      xml = xml + p.to_xml()
    for p in self.env_parameters[:]:
      xml = xml + p.to_xml()
    for p in self.vm_parameters[:]:
      xml = xml + p.to_xml()
    for component in self.components.keys():
      xml = xml + self.components[component].to_xml()
    for agent in self.agents.keys():
      xml = xml + self.agents[agent].to_xml()

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
    for agent in self.agents.keys():
      script = script + self.agents[agent].to_python()  
    return script

  def each_agent(self):
    for agent in self.agentlist: # only for testing iterators
      yield agent



