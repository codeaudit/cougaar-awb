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
from rule_text import RuleText

from society_factory import SocietyFactory
from society_factory import TransformationEngine
from society_factory import TransformationRule



import sys
import re
generator_file = sys.argv[1]
m = re.compile('\.', re.IGNORECASE).split(str(generator_file))
baseName = str(m[0])

print "creating society from  %s" % baseName
society = SocietyFactory(generator_file).parse()

print "\n\nPrettyPrint test:\n\n"
text = society.prettyPrint()


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

f = file(baseName+'.txt', 'w+')
for a in society.each_agent():
  f.write(str(a))
  f.write('\n')
f.close()

print "\n\nto xml-----------------"
xml = society.to_xml()
f = file(baseName+'-out.xml', 'w+')
f.write(xml)
f.close()

print "to python-----------------"

script = society.to_python()
f = file(baseName+'.py', 'w+')
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
	c = Component(name, klass="org.cougaar.blah.blah", priority = "COMPONENT", insertionpoint="Node.AgentManager.Agent.PluginManager.Plugin", rule=self.name)
	agent.add_component(c)
	c.add_argument(Argument("Parameter1", "1.0", rule=self.name))
	self.fire()

"""
rule01 = TransformationRule("Add Arg2 to certain Components.")
rule01.rule = """
for agent in society.each_agent():
  hascomp = False
  for component in agent.components:
    if str(component.klass) == "org.cougaar.blah.blah": hascomp = True
    if hascomp is True:
      component.add_argument(Argument("Parameter2", "1.0", rule=self.name))
      self.fire()
"""
rule02 = TransformationRule("Override Parameters.")
rule02.rule = """
for host in society.each_host():
	for node in host.each_node():
		self.fire()
		node.remove_parameter(VMParameter("-Dorg.cougaar.control.port"))
		node.override_parameter("-Dorg.cougaar.node.InitializationComponent","XML")
		node.set_rule(self.name)
		for agent in node.each_agent():
			agent.remove_component("org.cougaar.core.topology.TopologyReaderServlet")
			agent.set_rule(self.name)
			for comp in agent.each_component():
				if (comp.klass == "org.cougaar.mlm.plugin.ldm.LDMSQLPlugin"):
					comp.arguments[0].value = "fdm_equip_ref.q"
					comp.set_rule(self.name)
				if (comp.klass == "org.cougaar.mlm.plugin.organization.GLSInitServlet"):
					comp.arguments[0].value = "093FF.oplan.noncsmart.q"
					comp.set_rule(self.name)
"""

engine = TransformationEngine(society, 100)
### the 'real' rules
newRule = RuleText("C:\\Dana\\Rulebook\\rule1.rul")
rule00 = TransformationRule(newRule.description)
rule00.rule = (newRule.rule)
newRule = RuleText("C:\\Dana\\Rulebook\\args.rul")
rule01 = TransformationRule(newRule.description,)
rule01.rule = (newRule.rule)
newRule = RuleText("C:\\Dana\\Rulebook\\Override.rul")
rule02 = TransformationRule(newRule.description)
rule02.rule = (newRule.rule)

engine.add_rule(rule00)
engine.add_rule(rule01)
engine.add_rule(rule02)
soc = engine.transform()

text = soc.prettyFormat()
f = file(baseName+'-prettyFormat.txt', 'w+')
f.write(text)
f.close()
print "to python-----------------"

script = soc.to_python()
f = file(baseName+'-out.py', 'w+')
f.write(script)
f.close()

print "transformation ==> xml-----------------"
xml = soc.to_xml()
f = file(baseName+'-xform.xml', 'w+')
f.write(xml)
f.close()
print "Transformation Done!"

print "into and back from prettyFormat ---------------"
soc0 = soc.fromPrettyFormat(text)
text = soc0.prettyFormat()
f = file(baseName+'-fromPrettyFormat.txt', 'w+')
f.write(text)
f.close()
