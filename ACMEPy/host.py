#Host.py
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
from node import Node
class Host:

  def __init__(self, name=None, rule='BASE'):
    """Constructs a host with the optional name  """
    self.name = name
    self.society = None
    self.nodes = {}
    self.nodelist = [] # for testing iterators
    self.rule = str(rule)


  def __str__(self):
    return "Host:"+ self.name+":RULE:"+self.rule
    
    
  def delete_entity(self):
    self.society.delete_host(self)
  
  def add_node(self, node):
    if isinstance(node, Node):
      node.host = self
      self.nodes[node.name] = node
      self.nodelist.append(node) # only for testing iterators
      return node
    if isinstance(node, types.StringType):
      newNode = Node(node)
      self.nodes[node] = newNode
      self.nodelist.append(newNode) # only for testing iterators     
      self.nodes[node].host = self
      return self.nodes[node]

  def delete_node(self, node):
    del self.nodes[node.name]
    self.nodelist.remove(node)
  
  def get_node(self, index):
    return self.nodelist[index]

  def add_nodes(self, nodes):
    if isinstance(nodes, types.ListType):
      for n in nodes: self.add_node(n)


  def set_rule(self, newRule):
        self.rule = str(newRule)

  def clone(self):
    host = Host(self.name)
    host.add_nodes(self.nodes)
    return host
    
  def to_xml(self):
    xml = "  <host name='"+ self.name + "'>\n"
    for node in self.nodes.keys():
      xml = xml + self.nodes[node].to_xml()
    xml = xml +  "  </host>\n"
    return xml

  def to_python(self):
    script = "host = Host('"+self.name+"')\n"
    script = script + "society.add_host(host)\n"
    for node in self.nodes.keys():
      script = script + self.nodes[node].to_python()   
    return script
    
    
  def each_node(self):
    for node in self.nodelist: # for testing iterators
      yield node


