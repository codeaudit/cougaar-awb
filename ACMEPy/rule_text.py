# rule_text.py
from string import *
class RuleText:
  def __init__(self, filename, description=None, rule=None):
    self.description = self.rule = ""
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
	  self.description = str(list[1]).strip()
	if find (lower(in_line),'rule:') == 0:
	  readingRule = True
      ### write a final newline to assure outdenting in Python
      self.rule = self.rule + "\n"

  def saveRule(self, filename):
    f = open(filename, 'w+')
    f.writelines("description: "+str(self.description)+'\n')
    f.writelines("rule:\n"+str(self.rule))
    f.close()
  def __str__(self):
    print "DESC:", self.description
    print "RULE:\n", self.rule



