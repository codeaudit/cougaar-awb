#argument.py
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

class Argument:
  
  def __init__(self, value, rule='BASE', order ='1.0'):
    self.value = value
    self.rule = str(rule)
    self.order = str(order)
    
  def __str__(self):
    return "Argument:"+self.value+":RULE:"+self.rule+":ORDER:"+self.order

  def set_rule(self, newRule):
        self.rule = str(newRule)
          
  def to_xml(self):
    xml = "<argument order=\""+self.order+"\">"
    xml = xml + str(self.value) + "</argument>\n"
    return xml
    
  def to_python(self):
    script = "argument = Argument('"+self.value+"','"+self.rule+"','"+self.order+"')\n"
    script = script + "component.add_argument(argument)\n"
    return script
