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
import sys

from society_factory import SocietyFactory
from society_factory import TransformationEngine
from society_factory import TransformationRule

def setup_the_show:
  generator_file = sys.argv[1]
  directory_spec = sys.argv[2]
  print "creating agents from ",generator_file
  society = SocietyFactory(generator_file).parse()

def create_agent_xml:
  print "\n\n Saving Agents to xml-----------------"
  for a in society.each_agent(): 
    print a, "\n"
  


xml = society.to_xml()
f = file('tiny-out.xml', 'w+')
f.write(xml)
f.close()

