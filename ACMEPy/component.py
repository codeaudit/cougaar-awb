#Component.py
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
import time
from argument import Argument

class Component:
   # Construct a plugin
   #
   # data:: [String] the plugin data
   #
  def __init__(self, name=None, klass=None, priority = None, insertionpoint=None, order=None, rule='BASE'):
    self.name = name
    self.klass = klass
    self.priority = priority
    self.insertionpoint = insertionpoint
    self.order = order
    self.arguments = []
    self.rule = str(rule)
    self.parent = None
    self.prev_parent = None
    # look for degenerate XML:
    if name is None: self.name = klass                     # + str(time.time())
    if priority is None: self.priority = 'COMPONENT'
    if insertionpoint is None: self.insertionpoint = 'Node.AgentManager.Agent.PluginManager.Plugin' # Good default?

  def set_attribute(self, attribute, value):
    # both args must be strings
    if attribute.lower() == 'name':
      self.name = value
    elif attribute.lower() == 'klass':
      self.klass = value
    elif attribute.lower() == 'priority':
      self.priority = value
    elif attribute.lower() == 'insertionpoint':
      self.insertionpoint = value
    elif attribute.lower() == 'order':
      self.order = value
    elif attribute.lower() == 'rule':
      self.rule = value
    else:
      raise Exception, "Attempting to set unknown Component attribute: " + attribute.lower()
    self.parent.society.isDirty = True

  def delete_entity(self):
    '''Deletes itself from component list of parent node or agent.'''
    self.parent.delete_component(self)

  def delete_from_prev_parent(self):
    if self.prev_parent is not None:
      self.prev_parent.delete_component(self)
    else:
      self.delete_entity()

  def has_changed_parent(self):
    return self.parent != self.prev_parent

  def delete_argument(self, argument):
    self.arguments.remove(argument)
    del argument
    if self.parent is not None:
      self.parent.society.isDirty = True

  def add_entity(self, entity):
    if isinstance(entity, Argument):
      entity.prev_parent = entity.parent
      self.add_argument(entity)
    else:
      raise Exception, "Attempting to add unknown Component attribute"

  def add_argument(self, argument):
    if isinstance(argument, Argument):
      self.arguments.append(argument)
      argument.parent = self
      if self.parent is not None and self.parent.society is not None:
        self.parent.society.isDirty = True
    elif type(argument) == types.StringType:  # must be a string
      arg = Argument(argument)
      self.add_argument(arg)
    else:
      raise Exception, "Attempting to add invalid Argument type"

  def get_argument(self, index):
    if len(self.arguments) > index:
      return self.arguments[index]
    return None

  def each_argument(self):
    for argument in self.arguments: # only for testing iterators
      yield argument

  def has_argument(self, argValue):
    for argument in self.arguments:
      if argument.name == argValue:
        return True
    return False

  def __str__(self):
    return "Component:"+self.name+":RULE:"+self.rule

  def set_rule(self, newRule):
    self.rule = str(newRule)
    self.parent.society.isDirty = True

  def getStrippedName(self):
    index = self.name.find('|')
    if index > -1 and self.parent is not None and self.name[:index] == self.parent.name:
      return self.name[index+1:]
    else:
      return self.name

  def rename(self, newName):
    self.name = newName
    self.parent.society.isDirty = True
    return self.name

  def clone(self, parent=None):
    component = Component(self.name, self.klass, self.priority, self.insertionpoint, self.order, self.rule)
    component.parent = parent
    for arg in self.arguments:
      new_arg = arg.clone()
      component.add_argument(new_arg)
    return component

  def getType(self):
    return 'component'

  def to_xml(self, numTabs=4):
    tab = ' ' * 4
    indent = tab * numTabs
    xml =  indent + "<component name='" + str(self.name) + "' class='" + str(self.klass) + \
        "' priority='" + str(self.priority) + "' insertionpoint='" + str(self.insertionpoint) + "'"
    if self.order and len(str(self.order)) > 0:  # order may not be present
      xml = xml + " order='" + str(self.order) + "'"
    xml = xml + ">\n"
    for a in self.arguments[:]:
      xml = xml + a.to_xml()
    xml = xml + indent + "</component>\n"
    return xml

  def to_python(self):
    script = "component = Component(name='" + self.name + "', klass='" + self.klass + \
        "', priority='" + str(self.priority) + "', insertionpoint='" + self.insertionpoint + \
        "', order='" + self.order + "')\n"
    script = script + "agent.add_component(component)\n"
    for a in self.arguments:
      script = script + a.to_python()
    return script

  def to_ruby(self, numTabs):
    if self.parent.isNodeAgent():
      # it's a component of a node
      script = "      node.agent.add_component('" + self.name + "') do |c|\n"
    else:
      #it's a component of an agent
      script = "        agent.add_component('" + self.name + "') do |c|\n"
    indent = "  " * numTabs
    script = script + indent + "c.classname = '" + self.klass + "'\n"
    script = script + indent + "c.priority = '" + self.priority + "'\n"
    script = script + indent + "c.insertionpoint = '" + self.insertionpoint + "'\n"
    if self.order and len(self.order) > 0:
      script = script + indent + "c.order = '" + self.order + "'\n"
    for a in self.arguments:
      script = script + a.to_ruby(numTabs)
    indent = "  " * (numTabs - 1)
    script = script + indent + "end\n"
    return script

  def equalsComponent(self, other):
    foo = """
          self.name = name
    self.klass = klass
    self.priority = priority
    self.insertionpoint = insertionpoint
    self.order = order
    self.arguments = []
    self.rule = str(rule)
    """
    a1 = [other.name, other.klass, other.arguments]
    a2 = [self.name, self.klass, self.arguments]
    return a1 == a2