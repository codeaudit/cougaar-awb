# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: AgentDataCollector.py,v 1.2 2004-12-06 22:22:46 damoore Exp $
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
from threading import Thread, Semaphore
from __future__ import generators\
# We will certainly need to test the release number for Python
# to eliminate/modify this import
import re
import string
import urllib
import time

concurrentProcesses = 10
mutex = Semaphore(value=concurrentProcesses)

class AgentHTMLParser(Thread):
    def __init__(self, url=0, aname="No Name"):
        Thread.__init__(self)
        self.name = aname
        self.ratio = -1
        self.totalTasks= -1
        self.unplannedTasks = -1
        self.unestimatedTasks = -1
        self.failedTasks = -1
        self.unconfidentTasks = -1
        self.siteurl = url
        self.returnlist = []
    
    def run(self):
        self.getPage()
        
    def getPage(self):

        if self.siteurl == 0:
            return
        else:
            mutex.acquire()
            self.file = urllib.urlopen(self.siteurl)
            mutex.release()
        # Parse the website and collect the data though regular expressions
        for self.i in self.file.readlines():
            totalRe = re.compile('Number of Tasks: <b>(.*)')
            ratioRe = re.compile('GLMCompletion ratio:.*<b>(.?[0-9]+)')
            unplannedRe = re.compile('<.*Unplanned Tasks\[(.*)\]')
            unestimatedRe = re.compile('<.*Unestimated Tasks\[(.*)\]')
            failRe= re.compile('<.*Failed Tasks\[(.*)\]')
            unconfidentRe = re.compile('<.*Unconfident Tasks\[(.*)\]')
            
            ans = totalRe.match(self.i)
            if ans:
                self.totalTasks = ans.group(1)
            
            ans = ratioRe.match(self.i)
            if ans:
                self.ratio = ans.group(1)
            
            ans = unplannedRe.match(self.i)
            if ans:
                self.unplannedTasks = ans.group(1)
                
            ans = unestimatedRe.match(self.i)
            if ans:
                self.unestimatedTasks = ans.group(1)
        
            ans = failRe.match(self.i)
            if ans:
                self.failedTasks = ans.group(1)
                
            ans = unconfidentRe.match(self.i)
            if ans:
                self.unconfidentTasks = ans.group(1)
                
        # Add all the elemets to a list for returning
        self.returnlist.append(str(self.totalTasks))
        self.returnlist.append(str(self.ratio))
        self.returnlist.append(str(self.unplannedTasks))
        self.returnlist.append(str(self.unestimatedTasks))
        self.returnlist.append(str(self.failedTasks))
        self.returnlist.append(str(self.unconfidentTasks))
        self.returnlist.append(self.name)
        
    def getInfo(self):
        return self.returnlist

def SocietyQuery(societyAddress):
    # Path Style
    # http://sm056:8801/$1-1-CAVSQDN.AVNBDE.1-AD.ARMY.MIL/completion?showTables=true&viewType=viewAgentBig
    # A = AgentHTMLParser("completionbft.htm")
    Agent_Names = []
    agentfile = urllib.urlopen(societyAddress)
    ThreadList = []
    MainOut = []
    QueryDictionary = {}
    start = time.clock()    
    # Read in the names of all the agents and store them to an agent list [^.comm]
    for agentline in agentfile:
        AgentNameRE = re.compile('^<.*\/\$(.*.[^com])\/list')
        AgentHostRE = re.compile('^<.*Agents on host \((.*)\)')
        agentString = AgentNameRE.match(agentline)
        hostString = AgentHostRE.match(agentline)
        if hostString:
            agentHost = hostString.group(1)
        if agentString:
            Agent_Names.append(agentString.group(1))
    # Loop though all the angets and get the information from the server
    #~ print Agent_Names
    for i in Agent_Names:
        agentInfoURL = "http://" + agentHost  + "/$" + i + "/completion?showTables=true&viewType=viewAgentBig"
        AHP = AgentHTMLParser(agentInfoURL, i)
        #~ AHP.getPage()
        #~ Out += AHP.getInfo()
        AHP.start()
        ThreadList.append(AHP)

    for retriever in ThreadList:
        retriever.join()
        agentInformation = retriever.getInfo()
        agentName = agentInformation.pop()
        QueryDictionary[agentName] = agentInformation
        
    looptime = time.clock()-start
    print "\nNumber of Agnets: \t" + str(len(Agent_Names)) + "\nProcessing Time: \t" + str(looptime) + " seconds\n" + "Society Server: \t"
    return QueryDictionary
    
#~ dict = SocietyQuery()
concurrentProcesses = 1
mutex = Semaphore(value=concurrentProcesses)
dict = SocietyQuery('http://u142:8800/agents?suffix=.')
print "Number of Threads: \t" + str(concurrentProcesses)

print str(dict)
