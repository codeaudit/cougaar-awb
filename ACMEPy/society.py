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
import types


class Society:
    
  def __init__(self, name):
    DEFAULT_PORT = 8800
    self.name = name
    self.agents = None 
    self.nodes = None
    self.hosts = {}
    self.cougaar_port  = DEFAULT_PORT
    self.controller = None
    self.hostlist = []
    self.rule = "BASE"
    
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
