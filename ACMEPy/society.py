# Society.py
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
from host import Host
from node import Node  
from agent import Agent
from component import Component
from argument import Argument
from types import *
import types


class Society:
    
  def __init__(self, name, rule='BASE'):
    DEFAULT_PORT = 8800
    self.name = name
    self.agents = None 
    self.nodes = None
    self.hosts = {}
    self.cougaar_port  = DEFAULT_PORT
    self.controller = None
    self.hostlist = []
    self.rule = str(rule)
    
  def __str__(self):
    return "Society:"+ self.name+":RULE:"+self.rule
    
  def add_host(self, host):
    # is this really a 'Host' instance?
    if isinstance(host, Host):
      self.hosts[host.name] = host
      self.hostlist.append(host)
      host.society = self
      return host
    if isinstance(host,types.StringType):
      h = Host(host)
      self.hosts[host] = h # Host(host)
      self.hostlist.append(h) # (host)      
      self.hosts[host].society = self
      return self.hosts[host]
    
  def get_host(self, index):
    return self.hostlist[index]

  def set_rule(self, newRule):
        self.rule = str(newRule)
      
  def active_hosts():
    actives = []
    for host in self.hosts.keys():
      if len(hosts.nodes) > 0: 
        actives.append(host.clone)
    return actives 

  def each_host(self):
    for host in self.hostlist:
      yield host

  def each_node(self):
    for host in self.each_host():
      for node in host.each_node():
        yield node

  def each_agent(self):
    for host in self.each_host():
      for node in host.each_node():
        for agent in node.each_agent():
          yield agent

  def each_component(self):
    for host in self.each_host():
      for node in host.each_node():
        for agent in node.each_agent():
          for component in agent.each_component():
            yield component


  def to_xml(self):
    xml = "<?xml version='1.0'?>\n"
    xml = xml + "<society name='"+ self.name +"'\n"
    xml = xml + "  xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\n" 
    xml = xml + "  xsi:schemaLocation='society.xsd'>\n"
    for host in self.hosts.keys():
      xml = xml + self.hosts[host].to_xml()
    xml = xml + "</society>"
    return xml

  def to_python(self):
    script = "from society import Society\n"
    script = script + "from host import Host\n"
    script = script + "from node import Node\n"
    script = script + "from agent import Agent\n"
    script = script + "from component import Component\n"
    script = script + "from argument import Argument\n\n"
    script = script + "society = Society('"+str(self.name)+"')\n"
    for host in self.hosts.keys():
      script = script + self.hosts[host].to_python()   
    return script

  def prettyPrint(self):
    print self
    for host in self.hosts.keys():
      print "\t", self.hosts[host]
      for node in self.hosts[host].nodes.keys():
        theNode = self.hosts[host].nodes[node]
        print "\t\t", theNode
        for agent in self.hosts[host].nodes[node].agents.keys():
          print "\t\t\t", theNode.agents[agent]
          for component in theNode.agents[agent].components:
            print "\t\t\t\t", component
    
  def prettyFormat(self):
    text = str(self)+"\n"
    for host in self.hosts.keys():
      text = text+str(self.hosts[host])+"\n"
      for node in self.hosts[host].nodes.keys():
        theNode = self.hosts[host].nodes[node]
        text = text+str(theNode)+"\n"
        for agent in self.hosts[host].nodes[node].agents.keys():
          text = text + str(theNode.agents[agent])+"\n"
          for component in theNode.agents[agent].components:
            text = text + str(component)+"\n"
            for argument in component.arguments:
              text = text + str(argument)+"\n"
    return text

  def toString(self):
    text = str(self)+"\n"
    for host in self.hostlist:
      text = text+str(host)+"\n"
      for node in host.nodelist:
        text = text+str(node)+"\n"
        for agent in node.agentlist:
          text = text + str(agent)+"\n"
          for component in agent.components:
            text = text + str(component)+"\n"
            for argument in component.arguments:
              text = text + str(argument)+"\n"
    return text

  def fromPrettyFormat(self, text):
    # reverse of prettyFormat. We need to flesh out the detail of attributes and elements for each of these
    # this is just the bare backbones!!!
    # should we do a recursive descent like we do with everything else? this sort of looks flat to me :-(
    rowList =   rowList = str(text).split('\n')
    for item in rowList:
      data = str(item).split(':')
      if len(data) < 4:
	print "??? Malformed text ???:<", item, ">" 
	continue
      if data[0].lower() == 'society':
	society = Society(data[1])
      if data[0].lower() == 'host':
	host = Host(data[1])
	society.add_host(host)
      if data[0].lower() == 'node':
	node = Node(data[1])
	host.add_node(node)
      if data[0].lower() == 'agent':
	agent = Agent(data[1])
	node.add_agent(agent)
      if data[0].lower() == 'component':
	component = Component(data[1])
	agent.add_component(component)
      if data[0].lower() == 'argument':
	argument = Argument(data[1], data[5])
	component.add_argument(argument)
    return society
 