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
from facet import Facet

class Host:

  def __init__(self, name=None, rule='BASE'):
    """Constructs a host with the optional name  """
    self.name = name
    #~ self.society = None
    self.parent = None
    #~ self.nodes = {}
    self.nodelist = [] # for testing iterators
    self.facets = []
    self.rule = str(rule)
    #~ self.enclaveFacetShowing = False
    #~ self.serviceFacetShowing = False

  def __str__(self):
    return "Host:"+ self.name+":RULE:"+self.rule
    
  def add_entity(self, entity):  
    if type(entity) == types.ListType:  # will be a list of facet objects
      for each_thing in entity:
        self.add_facet(each_thing)
    elif isinstance(entity, Node):
      self.add_node(entity)
    else:
      raise Exception, "Attempting to add unknown Host attribute"
  
  def add_node(self, node):
    if isinstance(node, Node):
      #~ self.nodes[node.name] = node
      self.nodelist.append(node) # only for testing iterators
      node.parent = self
      return node
    if isinstance(node, types.StringType):
      newNode = Node(node)
      #~ self.nodes[node] = newNode
      self.nodelist.append(newNode) # only for testing iterators     
      newNode.parent = self
      return newNode

  def delete_entity(self, saveAgents=False):
    '''Deletes itself from its parent society'''
    self.parent.delete_host(self, saveAgents)
  
  def delete_node(self, node, saveAgents=False):
    for agent in node.each_agent():
      if saveAgents:
        node.remove_agent(agent)
      else:
        node.delete_agent(agent)
    node.remove_all_facets()
    node.remove_all_parameters()
    self.nodelist.remove(node)
    del node
  
  def remove_entity(self):
    self.parent.remove_host(self)
  
  def remove_node(self, node):
    self.nodelist.remove(node)
  
  def get_node(self, index):
    return self.nodelist[index]

  def get_nodes(self):
    return self.nodelist

  def add_nodes(self, nodes):
    if isinstance(nodes, types.ListType):
      for n in nodes: self.add_node(n)

  def has_node(self, nodeName):
    for node in self.nodelist:
      if node.name == nodeName:
        return True
    return False
  
  def each_facet(self):
    for facet in self.facets: # only for testing iterators
      yield facet

  def remove_facet(self, component_classname):
    print "Host::remove_facet() not implemented"

  def remove_all_facets(self):
    for facet in self.facets:
      del facet
    self.facets = []

  def delete_facet(self, facet):
    self.facets.remove(facet)
    del facet

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

  def set_rule(self, newRule):
        self.rule = str(newRule)

  def countNodes(self):
    return len(self.nodelist)
  
  def clone(self):
    host = Host(self.name, self.rule)
    for node in self.nodelist:
      new_node = node.clone()
      host.add_node(new_node)
      new_node.host = host
    for facet in self.facets:
      new_facet = facet.clone()
      host.add_facet(new_facet)
      new_facet.parent = host
    return host
    
  def to_xml(self):
    xml = "  <host name='"+ self.name + "'>\n"
    #for node in self.nodes.keys():
      #xml = xml + self.nodes[node].to_xml()
    for facet in self.facets:
      xml = xml + facet.to_xml()
    for node in self.nodelist:
      xml = xml + node.to_xml()
    xml = xml +  "  </host>\n"
    return xml

  def to_python(self):
    script = "host = Host('"+self.name+"')\n"
    script = script + "society.add_host(host)\n"
    for facet in self.facets:
      script = script + facet.to_python()
    for node in self.nodelist:
      script = script + node.to_python()   
    return script
    
    
  def each_node(self):
    for node in self.nodelist: # for testing iterators
      yield node


