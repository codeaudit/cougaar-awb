import xmlrpclib
import httplib


fyi = '''
1. Open arg[1] with a URLLib call
2. parse the data
2. return a common data structure (TBD) to the ServletDataReceiver.
NOTES: This fcn have be embedded into the societyController
'''

#~ gServerAdr = None
#~ gPagePath = None
# request the page
# example: GetUrl("u129:8800", "agents")
fyi = '''
do some thing to get at the globals
'''
#~ print globals()['gServerAdr'],globals()['gPagePath']
#~ serverAddr = globals()['gServerAdr']
#~ page = globals()['gPagePath']
agentMap = globals()['agents']
agentList = agentMap.keys()
aPeer = xmlrpclib.Server('http://localhost:8888')
data = aPeer.initServerMethods(agentMap)

for i in range(0,5):
        print "iteration:", i, aPeer.getGeneratedData(agentList[i])
globals()['taskCount'] = aPeer.ReceiveData(data)


