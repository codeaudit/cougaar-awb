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
    self.parent = None
    self.nodelist = [] 
    self.facets = []
    self.rule = str(rule)

  def __str__(self):
    return "Host:"+ self.name+":RULE:"+self.rule
    
  def add_entity(self, entity, orderAfterObj=None):  
    if type(entity) == types.ListType:  # will be a list of facet objects
      for each_thing in entity:
        self.add_facet(each_thing)
    elif isinstance(entity, Node):
      if entity.society.name == self.parent.name:  # it's a reordering w/in same society
         return self.add_node(entity, orderAfterObj, True)
      else:
        return self.add_node(entity, orderAfterObj)
    else:
      raise Exception, "Attempting to add unknown Host attribute"
  
  def add_node(self, node, orderAfterObj=None, reorder=False):
    if isinstance(node, Node):
      isDupe = False
      # Check if we've already got a node by that name; but if this
      # is a reordering, dupes are ok, so we leave isDupe set to false
      if not reorder and self.parent is not None:
        for existingNode in self.parent.each_node():
          if node.name == existingNode.name:
            isDupe = True
            break
      if not isDupe:
        # We don't have it, so add it
        if orderAfterObj is not None:
          # User  wants to add it at a particular place
          index = -1
          if isinstance(orderAfterObj, Node) and orderAfterObj in self.nodelist:
            index = self.nodelist.index(orderAfterObj)
          self.nodelist.insert(index + 1, node)
        else:
          # User doesn't care where it's added, so add at the end
          self.nodelist.append(node) 
        node.parent = self
        node.society = self.parent
        node.nodeAgent.society = self.parent
        return node
      else:
        print "Unable to add duplicate Node."
        return None
    if isinstance(node, types.StringType):
      newNode = Node(node)
      return self.add_node(newNode)
  
  def delete_entity(self, saveAgents=False):
    '''Deletes itself from its parent society'''
    self.parent.delete_host(self, saveAgents)
  
  def delete_node(self, node, saveAgents=False):
    if node in self.nodelist:
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
    if node in self.nodelist:
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
  
  ##
  # Iteratively returns each facet on this Host instance as a Dictionary
  #
  def each_facet(self):
    for facet in self.facets: 
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

  ##
  # Returns a list containing all the values for the specified key
  #
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
  
  ##
  # Renames this host if the new name is not already taken by another host.
  # Returns the host's name; will be the old name if the newName was  
  # already taken, or the newName if the rename was successful.
  #
  # newName:: [String] the new name for this host
  #
  def rename(self, newName):
    if not self.parent.has_host(newName):
      # name is not taken, so it's OK
      oldName = self.name
      self.name = newName
      if oldName == self.parent.nameserver_host:
        self.parent.set_nameserver(newName + self.parent.nameserver_suffix)
        for node in self.parent.each_node():
          node.updateNameServerParam(self.parent.get_nameserver())
    return self.name
  
  def each_node(self):
    for node in self.nodelist: 
      yield node

  def clone(self):
    host = Host(self.name, self.rule)
    for node in self.nodelist:
      new_node = node.clone()
      host.add_node(new_node)
      new_node.parent = host
    for facet in self.facets:
      new_facet = facet.clone()
      host.add_facet(new_facet)
      new_facet.parent = host
    return host
  
  def set_parent(self, society):
    self.parent = society
    for node in self.nodelist:
      node.set_society(society)
  
  def to_xml(self, hnaOnly=False):
    xml = "  <host name='"+ self.name + "'"
    if len(self.nodelist) == 0:
      xml = xml + "/"
    xml = xml + ">\n"
    if not hnaOnly:
      for facet in self.facets:
        xml = xml + facet.to_xml()
    for node in self.nodelist:
      xml = xml + node.to_xml(hnaOnly)
    if len(self.nodelist) > 0:
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
  
  def to_ruby(self):
    script = "  society.add_host('" + self.name + "') do |host|\n"
    for facet in self.facets:
      script = script + "    host.add_facet do |facet|\n"
      script = script + facet.to_ruby(3)
      script = script + "    end\n"
      #~ for keyvalue in facet.each_facet_pair():
        #~ script = script + "host.add_facet(\"" + keyvalue + "\")\n"
    for node in self.nodelist:
      script = script + node.to_ruby()
    #~ script = script + "society.add_host(host)\n"
    script = script + "  end\n"
    return script
  
