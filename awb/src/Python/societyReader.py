# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: societyReader.py,v 1.3 2004-12-06 22:19:04 damoore Exp $
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
import re
import urllib2
from urlparse import urlparse
import random as r
import time
import os, string
import thread
import httplib
from screenScraper import *


#~ htmlText = ''' <html><head><title>Agents at the Root ("<a href="/agents?suffix=.">.</a>")</title></head>
#~ <body><p><h1>Agents at the Root ("<a href="/agents?suffix=.">.</a>")</h1>
#~ <table border="0">
#~ <tr><td align="right">&nbsp;1.&nbsp;</td><td align="right"><a href="/agents?suffix=.comm">.comm</a></td></tr>
#~ <tr><td align="right">&nbsp;2.&nbsp;</td><td align="right"><a href="/$PlannerAgent/list">PlannerAgent</a></td></tr>
#~ <tr><td align="right">&nbsp;3.&nbsp;</td><td align="right"><a href="/$PlannerAgent2/list">PlannerAgent2</a></td></tr>
#~ </table>
#~ <p>
#~ <a href="/agents">Agents on host (fpga:8800)</a><br>
#~ <a href="/agents?suffix=.">Agents at the root (.)</a><br></body></html>
#~ '''

class SocietyReader:
        def __init__(self, url):
                self.url = url

        def readAgents(self):
                try:
                    f = urllib2.urlopen(self.url)
                    htmlText=  f.read() # reads the whole page as a big glob
                    f.close()
                    return self.scrapeHTML(htmlText)
                except urllib2.URLError:
                    return None

        def scrapeHTML(self, htmlText):
                self.agentList = []
                scraper = BeautifulSoup()
                scraper.feed(htmlText)
                #~ print ">>>\n",

                list = scraper.fetch('a', {'href':'/$%'})
                #~ for l in list:
                        #~ print "AREF >>>", l

                #~ print "\n\n Second tests..."
                #~ print 'Fetch List...'
                for s in list:
                        s = str(s)
                        #~ print 's >>>', s
                        start = string.index(s, ">")
                        end = string.rindex(s, "<")
                        t = s[start+1:end]
                        #~ print "AREF...", t
                        self.agentList.append(str(t))
                        #~ alphabet = [
#~ 'Alpha','Beta','Gamma','Delta','Epsilon',
#~ 'Zeta','Eta','Theta','Iota','Kappa',
#~ 'Lambda','Mu','Nu','Xi','Omicron',
#~ 'Pi','Rho','Sigma','Tau','Upsilon',
#~ 'Phi','Chi','Psi','Omega'
#~ ]
                #~ for item in alphabet:
                        #~ self.agentList.append(item)
                return self.agentList

        fyi = '''
        http://192.233.51.210:8800/$PlanAnalyzerAgent/tasks?mode=12&limit=true&formType=3&uid=formSubmit=Search
        '''
        fyi2 = """
        http://localhost:8800/$GameManager/tasks?mode=12
        """ # this is what the "all uniqueObjects" looks like

        def readUniqueObjects(self, host,port):
                self.uniqueObjects = {}
                uniqueObjectsQuery = '/tasks?mode=12&limit=true&formType=3&uid=formSubmit=Search'
                uniqueObjectsQuery = '/tasks?mode=12'

                if len(self.agentList) == None: return
                for agent in self.agentList:
                        wellformedURL = 'http://'+host+':'+port+ '/$' + agent +uniqueObjectsQuery
                        #~ print 'wellformedURL', wellformedURL
                        try:
                            f = urllib2.urlopen(wellformedURL)
                            htmlText=  f.read() # reads the whole page as a big glob
                            f.close()
                            scraper = BeautifulSoup()
                            scraper.feed(htmlText)
                            elements = scraper.fetch('center')
                            #~ print "elements>>>", elements
                            elt = str(elements[0])
                            elt = elt[elt.index('<b>')+3:elt.index('</b>')]
                            self.uniqueObjects[str(agent)] = elt
                        except  urllib2.HTTPError:
                            pass
                            # We are going to ignore anyone who has no tasks servlet ; just forget them
                            #
                # add dummy:
                        #~ self.uniqueObjects['---'] = '---' # not sure why you need to do - bug in DividedShape??
                #~ print 'uniqueObjects',  self.uniqueObjects
                return self.uniqueObjects


        def __str__(self):
                return "Agents >>>" + self.url