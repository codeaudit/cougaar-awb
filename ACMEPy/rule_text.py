# rule_text.py
from string import *
class RuleText:
  def __init__(self, filename, description=None, rule=None):
    if filename is None:
      self.description = description
      self.rule = rule
    else:
      readingRule = False
      in_file = open(filename,"r")
      while True:
	in_line = in_file.readline()
	if in_line == "": 
	  in_file.close()
	  break
	if readingRule is True:
	  self.rule = self.rule + in_line
	if find (lower(in_line),'description:') == 0:
	  list = split(in_line, ':')
	  self.description = str(list[1])
	if find (lower(in_line),'rule:') == 0:
	  readingRule = True

  def saveRule(self, filename):
    f = open(filename, 'w+')
    f.writelines("description: "+str(self.description))
    f.writelines("rule:\n"+str(self.rule))
    f.close()
  def __str__(self):
    print "DESC:", self.description
    print "RULE:\n", self.rule



