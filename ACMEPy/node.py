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

class Node:
  def __init__(self, name=None):
    self.name = name
    self.host = None
    self.agents = {}
    self.agentlist = []
    self.parameters = []
    self.vm_parameters = []
    self.prog_parameters = []
    self.env_parameters = []
    self.rule = "BASE"
    
  def __str__(self):
    return ("Node:"+self.name)
    
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

  def override_parameter(param, value):
    for p in self.parameters:
      args = p.split('=')
      if len(p) > 0 and (args[0] == param):
	self.parameters.remove(p)
	self.parameters.append(param +'='+value)

  def add_vm_parameter(self, parameter):
    self.vm_parameters.append(parameter)

  def add_env_parameter(self, parameter):
    self.env_parameters.append(parameter)

  def add_prog_parameter(self, parameter):
    self.prog_parameters.append(parameter)

  def add_parameter(param):
    parameters.append(param)

  def add_parameters(params):
    # params is intended to be of type list
    if isinstance(params, types.ListType):
      self.parameters = self.parameters + params
 
  def clone(self):
    node = Node(self.name)
    node.host = self.host
    for agent in agents:
      node.add_agent(agent.clone())
    node.add_parameters(self.parameters)
      
  def to_xml(self):
    xml = "  <node name='"+ self.name + "'>\n"
    # add parameters and agents
    for p in self.prog_parameters[:]:
      xml = xml + "<prog_parameter>\n" + str(p) +"</prog_parameter>\n"
    for p in self.env_parameters[:]:
      xml = xml + "<env_parameter>\n" + str(p) +"</env_parameter>\n"
    for p in self.vm_parameters[:]:
      xml = xml + "<vm_parameter>\n" + str(p) +"</vm_parameter>\n"
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



