# society_factory.py
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
import sys

from xml.dom.ext.reader import PyExpat
from xml.xpath import Evaluate

from society import *
from host import *
from node import *
from agent import *
from component import *
from argument import *
from parameter import *
import types
class SocietyFactory:
  
	# if 'source' is a string assume it is a filename
	# otherwise, assume it is a stream
  def __init__(self, source):
    global dom
    if type(source) is not types.FileType:
      source = file(str(source))
    dom = PyExpat.Reader().fromStream(source)

  def parse(self):
    society = Society(dom.documentElement.getAttribute('name')) #  new society
    #print "Society Name:", (society.name)
    hosts = Evaluate('host', dom.documentElement)
    for host in hosts:
      society_host = society.add_host(str(host.getAttribute('name')))
      #print "Host Name: ", society_host.name
      nodes = Evaluate( 'node', host)
      for node in nodes:
	host_node = society_host.add_node(str(node.getAttribute('name')))
	#print "Node Element: ", host_node.name
	# get parameters for nodes
	vm_parameters = Evaluate('vm_parameter/text()', node)
	for vm_parameter in vm_parameters:
	  host_node.add_vm_parameter( VMParameter(value=vm_parameter.nodeValue.strip()) )
	  #print "vm_parameters Value:"+ vm_parameter.nodeValue.strip()
	
	env_parameters = Evaluate('env_parameter/text()', node)
	for env_parameter in env_parameters:
	  host_node.add_env_parameter( EnvParameter(value=env_parameter.nodeValue.strip()) )
	  #print "env_parameters Value:"+ env_parameter.nodeValue.strip()    
	
	prog_parameters = Evaluate('prog_parameter/text()', node)
	for prog_parameter in prog_parameters:
	  host_node.add_prog_parameter( ProgParameter(value=prog_parameter.nodeValue.strip()) )
	  #print "prog_parameters Value:"+ prog_parameter.nodeValue.strip()   
	    
	klasses = Evaluate('class/text()', node)
	#for klass in klasses:
	#  print "klass Value:"+ klass.nodeValue.strip()
	# get Agents
	agents = Evaluate( 'agent', node)
	for agent in agents:
	  node_agent = host_node.add_agent(str(agent.getAttribute('name')))
	  node_agent.klass = str(agent.getAttribute('class'))
	  #print "\nAgent: ", agent.getAttribute('name')," Class:", agent.getAttribute('class')
	  components = Evaluate( 'component', agent)
	  for component in components:
	    name = component.getAttribute('name')
	    klass = component.getAttribute('class')
	    priority = component.getAttribute('priority')
	    order = component.getAttribute('order')
	    insertionpoint = component.getAttribute('insertionpoint')
	    c = Component(name, klass, priority, order, insertionpoint)
	    node_agent.add_component(c)
	    arguments = Evaluate('argument', component)
	    for argument in arguments:
	      order = str(argument.getAttribute('order'))
	      value = str(argument.firstChild.nodeValue).strip()
	      c.add_argument(Argument(value, order))
    return society    

  def to_xml(self, society):    return self.society.to_xml
    
  def to_python(self, society): 	return self.society.to_python()
    

class TransformationRule:
  def __init__(self, name):
    global society
    self.name = name
    self.fire_count = 0
    self.rule = None
    self.fired = False
    self.society = None

  def set_rule(ruleText):
    self.rule = ruleText
    
  def fire(self):
    self.fire_count = self.fire_count + 1
    self.fired = True
    
  def reset(self):
    self.fired = False
    
  def has_fired(self):
    return self.fired
    
  def execute(self, society):
    print "running rule "+ str(self.name)+ " on society "+ str(society.name)
    exec self.rule





class TransformationEngine:
  def __init__(self, society, max_loop=300):
    self.MAXLOOP = max_loop
    self.society = society
    self.rules = []
    
  def add_rule(self, rule):
    if isinstance(rule, TransformationRule): self.rules.append(rule)
  
  def transform(self):
    loop = True
    count =0
    while loop is True and count < self.MAXLOOP:
      loop = False
      for rule in self.rules:
	rule.execute(self.society)
	if rule.fired == True:
	  rule.reset
	  loop = True
      count = count + 1
      print "loop ", count
    for rule in self.rules: print "Rule '"+ rule.name + "' fired ", rule.fire_count, " times."
    return self.society

