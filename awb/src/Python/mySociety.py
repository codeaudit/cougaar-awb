#!/bin/env python
#----------------------------------------------------------------------------
# Name:         insertion_dialog.py
# Purpose:      dialogs for insertion
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: mySociety.py,v 1.5 2004-12-06 22:22:46 damoore Exp $
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
import os
from wxPython.wx import *
from wx.lib.ogl import *


#---------------------------------------------------------------------------
# The class which is a representation of the Facets in the society
class myFacet:
    # Init for a Facet
    myFacetName = "noname"
    myFacetParent = "noparent"
    myFacetType = "SOURCEFACET"
    myFacetLevel = "0"
    myFacetPen = wx.BLACK_PEN
    myFacetBrush = '#800080'
    myFacetText = "Source"
    myFacetTextColour = "LIGHT GREY"
    myFacetShow = "True"
    myFacetViewDepth = "-1"
    children = []
        
    # Set up the Facet type which initilizes all the properties of a given Facet
    def setFacetType(self, facetname, facettype, facetparent):
        if (facettype == "SOURCEFACET"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "SOURCEFACET"
            self.myFacetLevel = "0"
            self.myFacetBrush = wx.Brush("#800080", wx.SOLID)
            self.myFacetText = "Source"
            self.myFacetTextColour = "LIGHT GREY"
        elif (facettype == "HOSTFACET"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "HOSTFACET"
            self.myFacetLevel = "1"
            self.myFacetBrush = wx.Brush("#0000FF", wx.SOLID)
            self.myFacetText = "Host"
            self.myFacetTextColour = "YELLOW"
        elif (facettype == "NODEFACET"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "NODEFACET"
            self.myFacetLevel = "2"
            self.myFacetBrush = wx.Brush("#FF0000", wx.SOLID)
            self.myFacetText = "Node"
            self.myFacetTextColour = "YELLOW"
        elif  (facettype == "AGENTFACET"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "AGENTFACET"
            self.myFacetLevel = "3"
            self.myFacetBrush = wx.Brush("#008000", wx.SOLID)
            self.myFacetText = "Agent"
            self.myFacetTextColour = "YELLOW"
        elif(facettype == "COMPONENTFACET"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "COMPONENTFACET"
            self.myFacetLevel = "4"
            self.myFacetBrush = wx.Brush("#FFFF00", wx.SOLID)
            self.myFacetText = "Component"
            self.myFacetTextColour = "DARK GREEN"
        elif(facettype == "Level6"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "Level6"
            self.myFacetLevel = "5"
            self.myFacetBrush = wx.Brush("#FFFF11", wx.SOLID)
            self.myFacetText = "Component"
            self.myFacetTextColour = "DARK GREEN"
        elif(facettype == "Level7"):
            self.myFacetName = facetname
            self.myFacetParent = facetparent
            self.myFacetType = "Level7"
            self.myFacetLevel = "5"
            self.myFacetBrush = wx.Brush("#11FF11", wx.SOLID)
            self.myFacetText = "Component"
            self.myFacetTextColour = "DARK GREEN"

        else:
            self.myFacetName = "noname"
            self.myFacetParent = "noparent"
            self.myFacetType = "UNKNOWN"
            self.myFacetLevel = "-1"
            self.myFacetBrush = "WHITE"
            self.myFacetText = "UNK"
            self.myFacetTextColour = "BLACK"
    
    def getFacetType(self):
        return self.myFacetType

    def getFacetBrush(self):
        return self.myFacetBrush
        
    def getFacetText(self):
        return self.myFacetTextColour
#---------------------------------------------------------------------------
# This is the society class which cotains the connections within the society
# The is used to remember what levels each facet is on and what each facet is connected to
class mySociety:
    def __init__(self):
        self.maxdepth = 0
        self.facetLevelsList = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.levelIndex = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.facetList = []
        self.tempList = []
        self.removeList = []
        self.addList = []
        self.connectionsDictionary = {}
        self.hiddenConnectionsDictionary = {}
        print "New Society Created"
        self.connectionsDictionary.clear()
        
    def __del__(self):
        del self.facetLevelsList[0:]
        del self.levelIndex[0:]
        del self.tempList[0:]
        del self.removeList[0:]
        del self.addList[0:]
        self.connectionsDictionary.clear()
        self.hiddenConnectionsDictionary.clear()
        
    def ClearFacetList(self): 
        self.facetList = []
        #~ self.tempList = []
        #~ self.removeList = []
        self.addList = []
    def AddNewFacet(self, name = "noname",  type = "SOURCEFACET", level = 0, parent = "noparent"):
        newFacet = myFacet()
        newFacet.setFacetType(name, type,parent)
        self.facetList.append(newFacet)
        if (parent == "noparent"):
            self.connectionsDictionary[name] = []
            self.facetLevelsList[level] += 1
        else:
            self.facetLevelsList[level] += 1
            # if there is no key add it initilizes
            if (parent in self.connectionsDictionary.keys()):
                self.connectionsDictionary[parent] += [name]
            # else if there is a key
            else:
                self.connectionsDictionary[parent] = [name]
    
    def getFacetList(self):
        del self.tempList[0:]
        self.makeLevelIndex()
        for k in self.facetList:
            if k.myFacetShow == "True":
                self.tempList.append(-1)
        self.sortFacets("noparent", len(self.facetList),self.facetList,0)
        #~ del self.facetList[0:]
        #~ self.facetList = self.facetList + self.tempList
        #~ if self.facetList:
            #~ self.getDepth(self.facetList[0])
        return self.tempList
        
    def hideAll(self):
        self.organizeConnections(self.facetList[0].myFacetName, 0)
        self.facetList[0].myFacetShow = "False"
        self.facetLevelsList[0] = 0
    def getConnectionsDictionary(self):
        return self.connectionsDictionary
    
    def getFacetLevelList(self):
        return self.facetLevelsList

    def getFacetDepth(self, fdSearchString):
        idx = 0
        while idx < len(self.facetList):
            if self.facetList[idx].myFacetName == fdSearchString:
              idx+=1

    def makeLevelIndex(self):
        prevtotal = 0
        idx = 0
        for i in self.facetLevelsList:
            if i==0:
                continue
            self.levelIndex[idx] = prevtotal
            prevtotal+=i
            idx+=1

    def sortFacets(self,searchString, theFacetListLength, theFacetList, depth):
        if theFacetListLength == 0:
            return
        count = 0
        searhStringList = []
        delFacetsList = []
        while (count < theFacetListLength):
            if (searchString == theFacetList[count].myFacetParent and theFacetList[count].myFacetShow == "True"):
                self.tempList[self.levelIndex[depth]] = theFacetList[count]
                self.levelIndex[depth]+=1
                searhStringList.append(theFacetList[count].myFacetName)
                delFacetsList.append(count)
            count+=1
        depth+=1
        for i in theFacetList:
            del i
        for i in searhStringList:
            self.sortFacets(i, len(theFacetList), theFacetList,depth)			

    def getDepth(self,currentFacet):
        self.maxdepth = 0
        self.countChildren(currentFacet, 0)
        return self.maxdepth

    def countChildren(self, currNode,depth=0):
        if depth > self.maxdepth:
            self.maxdepth = depth
        if self.connectionsDictionary.has_key(currNode) == 1:
            depth+=1
            for i in self.connectionsDictionary[currNode]:
                self.countChildren(i, depth)
                self.myFacetViewDepth(i,depth)
        elif self.hiddenConnectionsDictionary.has_key(currNode) == 1:
            depth+=1
            for j in self.hiddenConnectionsDictionary[currNode]:
                self.countChildren(j, depth)
                self.myFacetViewDepth(j,depth)

            
    def myFacetViewDepth(self, currNode, depth):
        for i in self.facetList:
            if i.myFacetName == currNode:
                i.myFacetViewDepth = abs(self.maxdepth-depth)
            
    def organizeConnections(self, cN,  vD, cD=0): #cN: Current Node / vD: View Depth / cD: Current Depth
        if vD == -1:
            vD = self.maxdepth
        del self.removeList[0:]
        for j in self.facetList:
            if j.myFacetName == cN:
                prevvD = j.myFacetViewDepth
                vD+=int(j.myFacetLevel)
                cD+=int(j.myFacetLevel)
                j.myFacetViewDepth = vD
                continue
        #~ print "Current Depth: ", cD, "\nPrev View Depth: ", prevvD , "\nView Depth: ", vD
        if prevvD < vD:
            self.addConn(cN, vD, cD)
            for k in self.facetList:
                if k.myFacetName in self.addList:
                    k.myFacetShow = "True"
            #~ print self.facetLevelsList
        else:
            self.removeConn(cN, vD, cD)
            for i in self.facetList:
                if i.myFacetName in self.removeList:
                    i.myFacetShow = "False"
            #~ print self.facetLevelsList

    def removeConn(self, currNode, viewdepth, currdepth=0):
        if self.connectionsDictionary.has_key(currNode) == 1:
            currdepth+=1
            for i in self.connectionsDictionary[currNode]:
                self.removeConn(i,viewdepth, currdepth)
            if viewdepth <= currdepth-1:
                self.hiddenConnectionsDictionary[currNode] = self.connectionsDictionary[currNode]
                self.removeList += self.connectionsDictionary[currNode]
                #~ print str(currdepth) + " " +str(len(self.connectionsDictionary[currNode]))
                self.facetLevelsList[currdepth]-=len(self.connectionsDictionary[currNode])
                del self.connectionsDictionary[currNode]

    def addConn(self,currNode, viewdepth, currdepth=0):
        if self.connectionsDictionary.has_key(currNode) == 1:
            currdepth+=1
            for i in self.connectionsDictionary[currNode]:
                self.addConn(i,viewdepth,currdepth)
        if self.hiddenConnectionsDictionary.has_key(currNode) == 1:
            currdepth+=1
            for j in self.hiddenConnectionsDictionary[currNode]:
                self.addConn(j,viewdepth,currdepth)
            if viewdepth > currdepth-1:
                self.connectionsDictionary[currNode] = self.hiddenConnectionsDictionary[currNode]
                self.addList += self.hiddenConnectionsDictionary[currNode]
                self.facetLevelsList[currdepth]+=len(self.hiddenConnectionsDictionary[currNode])
                del self.hiddenConnectionsDictionary[currNode]


#---------------------------------------------------------------------------
#~ TheSociety = mySociety() # Create the society
#TheSociety.AddNewFacet("Root", "SOURCEFACET", 0, "noparent")
#TheSociety.AddNewFacet("Child1", "HOSTFACET", 1, "Root")
#TheSociety.AddNewFacet("Child2", "HOSTFACET", 1, "Root")
#TheSociety.AddNewFacet("Child3", "HOSTFACET", 1, "Root")
#TheSociety.AddNewFacet("SubChild1", "NODEFACET", 2, "Child3")
#TheSociety.AddNewFacet("SubChild2", "NODEFACET", 2, "Child1")
#TheSociety.AddNewFacet("SubSubChild1", "AGENTFACET", 3, "SubChild1")
#TheSociety.getFacetList()
#print TheSociety.getFacetList()