from ACMEPy.society import Society
from ACMEPy.host import Host
from ACMEPy.node import Node
from ACMEPy.agent import Agent
from ACMEPy.component import Component
from ACMEPy.argument import Argument
from ACMEPy.parameter import *


class AgentMetadata:
    def __init__(self, orgId, agentName):
        self.agentName = agentName
        self.org_id = orgId[0]
        self.subordinates = []
        self.superior = None # even tho the agent.get_fact_values() returns a list, we coerce into a single value, by ignoring all members but the zero'th
        self.level = 0
    def addSubordinates(self, subordinates):        self.subordinates += subordinates
    def addSuperior(self, superior):
        if len(superior) == 0:        self.superior = ""
        else:        self.superior = (superior[0])
    def getSubordinates(self):         return self.subordinates
    def getSuperior(self):        return self.superior
    def hasSubordinate(self, subordinate):
        for s in self.subordinates:
            if s == subordinate: return True
        return False
    def setLevel(self, level): self.level = level
    def __str__(self):
        return "AgentMetadata:Agent:"+str(self.agentName)+" organisation: "+str(self.org_id)+" superior "+str(self.superior)+  " subordinates: "+str(self.subordinates)+"Level "+str(self.level)+"\n"
        #~ return "AgentMetadata:Agent:"+self.agentName+"organisation:"+self.org_id+"\n"




class MilitaryHierarchy:
    def __init__(self, society): # consumes a python society model
        self.hierarchy = {}
        self.levelMap = {}
        for a in society.each_agent():
            self.addAgent(a)
        self.highestLevel = 0
        for a in self.hierarchy.iterkeys():
            self.lvl = 0
            self.calcLevel(a)
            if self.lvl > self.highestLevel: self.highestLevel = self.lvl
            if self.levelMap.has_key(self.lvl):
                self.levelMap[self.lvl] += 1
            else: self.levelMap[self.lvl] = 1
            self.hierarchy[a].setLevel(self.lvl)
        print "Highest Level:", self.highestLevel
        print "levelMap:", self.levelMap

    def addAgent(self, agent):
        org = agent.get_facet_values("org_id")
        if org == None: return # silently? or complain of an ill-formed XML stanza? TODO: resolve this
        rel = AgentMetadata(org, agent.name)
        subs = agent.get_facet_values("subordinate_org_id")
        superiors = agent.get_facet_values("superior_org_id")
        if (len(subs) > 0): rel.addSubordinates(subs)
        if (len(superiors) > 0): rel.addSuperior(superiors)
        self.hierarchy[agent.name] = rel

    def calcLevel(self, agentName):
        if agentName is None:          return
        self.lvl += 1
        self.calcLevel(self.hierarchy[agentName].getSuperior())
    
    def __str__(self):
        rtnString =  "MilitaryHierarchy==>\n"
        for iter in self.hierarchy.iterkeys(): 
            rtnString = rtnString +  str(self.hierarchy[iter])
        return rtnString

