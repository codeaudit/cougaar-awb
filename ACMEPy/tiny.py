# tinyTester.py
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
from society import Society
from host import Host
from node import Node
from agent import Agent
from component import Component

from society_factory import SocietyFactory
from society_factory import TransformationEngine
from society_factory import TransformationRule

import sys
generator_file = sys.argv[1]

print "creating society from ",generator_file
society = SocietyFactory(generator_file).parse()

society.prettyPrint()
#print society
#for host in society.hosts.keys():
#  print "\t", society.hosts[host]
#  for node in society.hosts[host].nodes.keys():
#    theNode = society.hosts[host].nodes[node]
#    print "\t\t", theNode
#    for agent in society.hosts[host].nodes[node].agents.keys():
#      print "\t\t\t", theNode.agents[agent]
#      for component in agent.components:
#	print "\t\t\t\t", component

print "\n\nIterator test:\n\n"

#for h in society.each_host(): 
#  for n in  h.each_node(): 
#    for a in n.each_agent():  print a,
#for n in society.each_node(): print n,

for a in society.each_agent(): print a,

print "\n\nto xml-----------------"
xml = society.to_xml()
f = file('tiny-out.xml', 'w+')
f.write(xml)
f.close()

print "to python-----------------"

script = society.to_python()
f = file('tiny-out.py', 'w+')
f.write(script)
f.close()

print "transformation test-----------------"
rule00 = TransformationRule("Add blah blah to all agents.")
rule00.rule = """
for host in society.hosts.keys():
  for node in society.hosts[host].nodes.keys():
    for anAgent in society.hosts[host].nodes[node].agents.keys():
      agent = society.hosts[host].nodes[node].agents[anAgent]
      hascomp = False
      for component in agent.components:
	if str(component.klass) == "org.cougaar.blah.blah": hascomp = True
      if hascomp is not True:
	name = str(agent.name)+"|org.cougaar.blah.blah"
	c = Component(name, klass="org.cougaar.blah.blah", priority = "COMPONENT", order=451.0, insertionpoint="Node.AgentManager.Agent.PluginManager.Plugin", rule=self.name)
	agent.add_component(c)
	c.add_argument(Argument("Parameter1", "1.0", rule=self.name))

"""
rule01 = TransformationRule("Add foo foo to all agents.")
rule01.rule = """
for agent in society.each_agent():
  hascomp = False
  for component in agent.components:
    if str(component.klass) == "org.cougaar.foo.foo": hascomp = True
  if hascomp is not True:
    name = str(agent.name)+"|org.cougaar.foo.foo"
    c = Component(name, klass="org.cougaar.foo.foo", priority = "COMPONENT", order=451.0, insertionpoint="Node.AgentManager.Agent.PluginManager.Plugin", rule=self.name)
    agent.add_component(c)
    c.add_argument(Argument("Parameter1", "1.0", rule=self.name))

"""

engine = TransformationEngine(society, 100)
# engine.add_rule(rule00)
engine.add_rule(rule01)
soc = engine.transform()

soc.prettyPrint()

print "transformation ==> xml-----------------"
xml = soc.to_xml()
f = file('tiny-xform.xml', 'w+')
f.write(xml)
f.close()
print "Transformation Done!"
