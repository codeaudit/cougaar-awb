from screenScraper import *



# ~~~~~~
# quickie tester:
text = ''' <html><head><title>Agents at the Root ("<a href="/agents?suffix=.">.</a>")</title></head>
<body><p><h1>Agents at the Root ("<a href="/agents?suffix=.">.</a>")</h1>
<table border="0">
<tr><td align="right">&nbsp;1.&nbsp;</td><td align="right"><a href="/agents?suffix=.comm">.comm</a></td></tr>
<tr><td align="right">&nbsp;2.&nbsp;</td><td align="right"><a href="/$PlannerAgent/list">PlannerAgent</a></td></tr>
<tr><td align="right">&nbsp;3.&nbsp;</td><td align="right"><a href="/$PlannerAgent2/list">PlannerAgent2</a></td></tr>
</table>
<p>
<a href="/agents">Agents on host (fpga:8800)</a><br>
<a href="/agents?suffix=.">Agents at the root (.)</a><br></body></html>
'''
soup = BeautifulSoup()
soup.feed(text)
print "trs>>>\n",
#~ list = soup("a")
#~ for l in list:
        #~ print "AREF...", l
print "\n\n Second tests..."
list = soup.fetch('a', {'href':'/$%'})
print 'Fetch List...'
for l in list:
        print "AREF...", l


#~ soup = BeautifulSoup()
#~ soup.feed('''<a href="http://foo.com/">bla</a>''')
#~ print soup.fetch('a', {'href': 'http://foo.com/'})
#~ print soup.fetch('a', {'href': 'http://%'})
#~ print soup.fetch('a', {'href': '%.com/'})
#~ print soup.fetch('a', {'href': '%o.c%'})
