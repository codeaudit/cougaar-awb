import jabber
import sys
import sha
import pickle
import string
import httplib
import re
import sys, re, os, string

import thread


from roboUser import RoboUser

keys = {}
myFromID = 'robologger'
MYPORT = 7002
JABBERSERVER = None
def iqCB(con, iq):
    resultIq = jabber.Iq(to=iq.getFrom())
    resultIq.setID(iq.getID())
    resultIq.setFrom(iq.getTo())
    myFromID = iq.getTo()

    query_result = resultIq.setQuery(iq.getQuery())
    type = iq.getType()
    query_ns = iq.getQuery()

    print 'type = ', type, ' ns = ',query_ns
    if query_ns == jabber.NS_REGISTER:
        if type == 'get':
            resultIq.setType('result')
            iq_from = str(iq.getFrom())
            keys[iq_from] = sha.new(iq_from)
	    fields = {
	       'instructions': 'The service will add itself to your roster. You can send a message to the server in future like this:experiment=xxxx user=yyyy@zzzz user=yyyy@zzzz',
	      'key': keys[iq_from].hexdigest()
	      }
            for field in fields.keys():
		print 'key:', field
                field_node = query_result.insertTag(field)
                if fields[field]:
                    field_node.putData(fields[field])
            con.send(resultIq)
	    print 'resultQ:', resultIq
	    print 'sent'
	    
	    
	    
	    
        elif type == 'set':
            client_key_node = iq.getQueryNode().getTag('key')
            if not client_key_node:
                resultIq.setType('error')
                resultIq.setError('no key given!')
                con.send(resultIq)
            else:
                if keys[str(iq.getFrom())].hexdigest() == client_key_node.getData():
                    if iq.getQueryNode().getTag('remove'):
                        del clients[iq.getFrom().getStripped()]
                    else:
                        jid = iq.getFrom().getStripped()
			sub_req = jabber.Presence(iq.getFrom(), type='subscribe')
                        sub_req.setFrom(str(iq.getTo()) + "/registered")
                        con.send(sub_req)

                        resultIq.setType('result')
                        con.send(resultIq)
                else:
                    resultIq.setType('error')
                    resultIq.setError('invalid key', 400)
                    con.send(resultIq)
                del keys[str(iq.getFrom())]
		
		

    elif (query_ns == jabber.NS_AGENT) and (type == 'get'):
        # someone wants information about us
        resultIq.setType('result')

        responses = {
            'name': "RoboUser Service Component",
            # 'url': None,
            'description': "this is the RoboUser Component",
            'transport': "<future>...",
            'register': None, # we can be registered with
            'service': 'test' # nothing really standardized here...
            }

        for response in responses.keys():
            resp_node = query_result.insertTag(response)
            if responses[response]:
                resp_node.putData(responses[response])

        con.send(resultIq)
    else:
        print "don't know how to handle type", type, "for query", query_ns

def presenceCB(con, pres):
    print "presenceCB:", pres
    p = jabber.Presence(to=pres.getFrom())
    p.setFrom(pres.getTo())
    
    type = pres.getType()
    if type != 'unsubscribed':
	type = 'unsubscribe'
            
    if not type:
        type = 'available'

    print(pres.getFrom().getStripped() + " is " + type)

    if type == 'unavailable':
        client.setOnline(0)
        p.setType('unavailable')
        con.send(p)
        
    elif type == 'subscribe':
        p.setType('subscribed')
        con.send(p)
        p.setType('subscribe')
        con.send(p)

    elif type == 'unsubscribe':
        p.setType('unsubscribed')
        con.send(p)
        p.setType('unsubscribe')
        con.send(p)
        
    elif type == 'unsubscribed':
        pass

    elif type == 'probe':
        p.setType('available')
        con.send(p)
        
    elif type == 'available':
        # user is online
        client.setStatus(pres.getStatus())
        client.setShow(pres.getShow())

        p.setType('available')
        con.send(p)



def messageCB(con, msg):
    experimentID = ''
    users = []
    print 'msgCB:', msg

    type = msg.getType()
    if type == None: type = 'normal'
    if type == 'chat' or type == 'normal':
      jid = str(msg.getFrom())
      message = "Message from " + jid + ":" + msg.getBody()
      print message
      expr1 = re.compile(' ')
      expr2 = re.compile('=')
      argList= re.split(expr1, msg.getBody())
      print 'arglist',argList
      for i in argList:
	nVPairs = re.split(expr2, str(i))
	print 'nVPairs',nVPairs
	if str(nVPairs[0]) == 'experiment':
	  experimentID =  str(nVPairs[1]) 
	elif str(nVPairs[0]) == 'user':
	  users.append(str(nVPairs[1]))
	else:
	  print 'je ne compre pas', nVPairs
      
      print 'Users:',users
      m = jabber.Message()
      m.setFrom(msg.getTo())
      m.setTo(msg.getFrom())
      m.setType('chat')
      responseString = 'created robo user==>'+experimentID
      roboUser = RoboUser(server=JABBERSERVER, username=experimentID, password=experimentID, resource=experimentID)
      robots[experimentID] = roboUser
      m.setBody("OK :"+responseString)
      con.send(m) # send message back to the service requester. "It worked"
      roboUser.createRoster(users)
      # start its thread...is this really what I want to do or is it more like invoke a
      # function which is  a part of RoboUser?
      roboUser.start()
    else:
      m.setBody("FAIL:"+responseString)
      con.send(m)

# ###
# start here
# ###
if len(sys.argv) == 1: 
      # looks like the invoker forgot to specify a real host. possible bummer
      # let's set it to 'localhost' but print out the fact.
      JABBERSERVER = 'localhost'
else:
      JABBERSERVER = sys.argv[1]
print 'JABBERSERVER == ', JABBERSERVER

con = jabber.Component(host=JABBERSERVER, debug=0, port=MYPORT, log='log')
robots = {}    
    
    
try:
    con.connect()
except IOError, e:
    print "Couldn't connect: %s" % e
    sys.exit(0)
else:
    print "conn OK"
   
con.process(1)

if con.auth('secret'):
    print "auth OK"
else:
    print "problems with handshake: ", con.lastErr, con.lastErrCode
    sys.exit(1)

con.setMessageHandler(messageCB)
con.setPresenceHandler(presenceCB)
con.setIqHandler(iqCB)

p = jabber.Presence(type='available')


p.setFrom(myFromID+'/registered')

WAITSECONDS = 10
try:
    while(1):
        con.process(WAITSECONDS)
            
except KeyboardInterrupt:
    p = jabber.Presence(type='unavailable')
    p.setFrom(myFromID+'/registered')
    con.disconnect()
