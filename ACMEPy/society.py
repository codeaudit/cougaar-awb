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
    self.cougaar_port  = DEFAULT_PORT
    self.controller = None
    self.hostlist = []
    self.rule = str(rule)
    self.nameserver_host = "localhost"
    self.nameserver_suffix = ":8888:5555"
    
  def __str__(self):
    return "Society:"+ self.name+":RULE:"+self.rule
    
  def add_host(self, host, orderAfterObj=None, reorder=False):
    # is this really a 'Host' instance?
    if isinstance(host, Host):
      if len(self.hostlist) == 0:  # if this is first host, make it the nameserver
        self.nameserver_host = host.name
      isDupe = False
      # Check if we've already got a host by that name; but if this
      # is a reordering, dupes are ok, so we leave isDupe set to false
      if not reorder:
        for existingHost in self.hostlist:
          if host.name == existingHost.name:
            isDupe = True
            break
      if not isDupe:
        # We don't have it, so add it
        if orderAfterObj is not None:
          # User wants to add it at a particular place
          index = -1
          if isinstance(orderAfterObj, Host) and orderAfterObj in self.hostlist:
            index = self.hostlist.index(orderAfterObj)
          self.hostlist.insert(index + 1, host)
        else:
          # User doesn't care where it's added, so add at the end
          self.hostlist.append(host)
        host.parent = self
        return host
      else:
        return None
    if isinstance(host,types.StringType):
      h = Host(host)
      return self.add_host(h)
  
  def add_entity(self, host, orderAfterObj=None):
    if isinstance(host, Host):
      if host.parent.name == self.name:  # it's a reordering
        self.add_host(host, orderAfterObj, True)
      else:  #  we're adding a new host
        self.add_host(host, orderAfterObj)
    else:
      raise Exception, "Attempting to add unknown Society attribute"
  
  def get_nameserver(self):
    return self.nameserver_host + self.nameserver_suffix
  
  def set_nameserver(self, nameserver):
    # nameserver is assumed to be in the format '<hostname>:8888:5555'
    colon = nameserver.find(':')
    if colon < 0:
      self.nameserver_host = nameserver
    else:
      self.nameserver_host = nameserver[:colon]
      self.nameserver_suffix = nameserver[colon:]
  
  def set_nameserver_host(self, hostname):
    self.nameserver_host = hostname
  
  def has_host(self, hostName):
    for host in self.hostlist:
      if host.name == hostName:
        return True
    return False
  
  def get_host(self, index):
    return self.hostlist[index]

  def delete_host(self, host, saveAgents=False):
    for node in host.each_node():
      host.delete_node(node, saveAgents)
    host.remove_all_facets()
    self.remove_host(host)
    del host
  
  def remove_host(self, host):
    if host in self.hostlist:
      self.hostlist.remove(host)
    # If we've removed the host that's the nameserver, designate the 
    # next host in the list as the new nameserver
    if len(self.hostlist) == 0:
      self.nameserver_host = "localhost"
    elif self.nameserver_host == host.name:
      self.nameserver_host = self.hostlist[0].name
      for node in self.each_node():
        node.updateNameServerParam(self.get_nameserver())
  
  def set_rule(self, newRule):
        self.rule = str(newRule)
      
  def active_hosts():
    actives = []
    for host in self.hostlist:
      if len(host.nodelist) > 0: 
        actives.append(host.clone)
    return actives 

  def each_host(self):
    for host in self.hostlist:
      yield host

  def has_node(self, nodeName):
    for node in self.each_node():
      if node.name == nodeName:
        return True
    return False
  
  def each_node(self):
    for host in self.each_host():
      for node in host.each_node():
        yield node

  def get_node(self, nodeName):
    for node in self.each_node():
      if node.name == nodeName:
        return node
    return None
  
  def has_agent(self, agentName):
    for agent in self.each_agent():
      if agent.name == agentName:
        return True
    return False
  
  def each_agent(self, inclNodeAgent=False):
    for host in self.each_host():
      for node in host.each_node():
        for agent in node.each_agent(inclNodeAgent):
          yield agent

  def get_agent(self, agentName):
    for agent in self.each_agent():
      if agent.name == agentName:
        return agent
    return None
  
  def each_component(self, inclNodeAgent=False):
    for host in self.each_host():
      for node in host.each_node():
        for agent in node.each_agent(inclNodeAgent):
          for component in agent.each_component():
            yield component

  def get_node_list(self):
    nodeList = []
    for node in self.each_node():
      nodeList.append(node)
    return nodeList
  
  def get_agent_list(self, inclNodeAgent=False):
    agentList = []
    for agent in self.each_agent(inclNodeAgent):
      agentList.append(agent)
    return agentList
  
  def countHosts(self):
    return len(self.hostlist)
  
  def countNodes(self):
    nodelist = self.get_node_list()
    return len(nodelist)
  
  def countAgents(self):
    count = 0
    for agent in self.each_agent():
      count += 1
    return count
  
  def clone(self):
    society = Society(self.name, self.rule)
    for host in self.hostlist:
      new_host = host.clone()
      new_host.parent = society
      society.add_host(new_host)
    return society
  
  def remove_node(self, node):
    # This does not delete the node object,
    # but just removes it from the nodelist of its host.  The node obj may continue
    # to exist in the nodelist of another host. Even if the node obj is NOT in the
    # nodelist of another host, it will survive because its agents and facets
    # (if any) hold references to it, thus preventing it from being garbage
    # collected.  This can be a memory leak if not properly managed.
    for host in self.each_host():
      if host.has_node(node.name):
        host.remove_node(node)
        return
  
  def remove_agent(self, agent):
    # This does not delete the agent object,
    # but just removes it from the agentlist of its node.  The agent obj may continue
    # to exist in the agentlist of another node. Even if the agent obj is NOT in the
    # agentlist of another node, it will survive because its components and facets
    # (if any) hold references to it, thus preventing it from being garbage
    # collected.  This can be a memory leak if not properly managed.
    for host in self.each_host():
      for node in host.each_node():
        if node.has_agent(agent.name):
          node.remove_agent(agent)
          return
  
  def rename(self, newName):
    self.name = newName
  
  def to_xml(self):
    xml = "<?xml version='1.0'?>\n"
    xml = xml + "<society name='"+ self.name +"'\n"
    xml = xml + "  xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'\n" 
    xml = xml + "  xsi:schemaLocation='society.xsd'>\n"
    for host in self.hostlist:
      xml = xml + host.to_xml()
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
    for host in self.hostlist:
      script = script + host.to_python()   
    return script

  def prettyPrint(self):
    print self
    for host in self.hostlist:
      print "\t", host
      for facet in host.facets:
        print "\t\t", facet
      for node in host.nodelist:
        print "\t\t", node
        for facet in node.facets:  
          print "\t\t\t", facet
        for agent in node.agentlist:
          print "\t\t\t", agent
          for facet in agent.facets:
            print "\t\t\t\t", facet
          for component in agent.components:
            print "\t\t\t\t", component
            for argument in component.arguments:
              print "\t\t\t\t\t", argument
    
  def prettyFormat(self):
    text = str(self)+"\n"
    for host in self.hostlist:
      text = text+str(host)+"\n"
      for facet in host.facets:
        text = text + str(facet) + "\n"
      for node in host.nodelist:
        text = text+str(node)+"\n"
        for facet in node.facets:
          text = text + str(facet) + "\n"
        for agent in node.agentlist:
          text = text + str(agent)+"\n"
          for facet in agent.facets:
            text = text + str(facet) + "\n"
          for component in agent.components:
            text = text + str(component)+"\n"
            for argument in component.arguments:
              text = text + str(argument)+"\n"
    return text

  def toString(self):
    text = str(self)+"\n"
    for host in self.hostlist:
      text = text+str(host)+"\n"
      for facet in host.facets:
        text = text + str(facet) + "\n"
      for node in host.nodelist:
        text = text+str(node)+"\n"
        for facet in node.facets:
          text = text + str(facet) + "\n"
        for agent in node.agentlist:
          text = text + str(agent)+"\n"
          for facet in agent.facets:
            text = text + str(facet) + "\n"
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
 
  # Causes a society to delete references to all its components (hosts, nodes, agents, etc.).
  # Note that if we're closing a laydown mapping society, we may not want to delete the 
  # agents because that would also kill them from the original society from which we
  # got them, hence the "saveAgents" parameter.
  def close(self, saveAgents=False):
    for host in self.each_host():
      self.delete_host(host, saveAgents)
