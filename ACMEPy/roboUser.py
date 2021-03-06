#!/usr/bin/env python2
import socket
from select import select
from string import split,strip,join
import sys,os
import threading
import jabber
import xmlrpclib

class RoboUser(threading.Thread):
  
  True = 1
  False = 0

  
  def __init__(self, server=None, rpc=None, username=None, password=None, resource=None):
    threading.Thread.__init__(self)
    print "RoboUser: Register a New Robot: ",server, username, password, resource
    if server == None or username == None or password == None or resource == None:
      print "RoboUser: bad robot!"
      sys.exit(0)
    self.DELAY = 10
    self.observations = []
    con = jabber.Client(host=server, debug=False, log=sys.stderr)
    self.con = con
    con.setMessageHandler(self.messageCB)
    con.setPresenceHandler(self.presenceCB)
    con.setIqHandler(self.iqCB)
    con.setDisconnectHandler(self.disconnectedCB)
    
    self.server = server
    self.username = username
    self.password = password
    self.resource = resource
    self.rpc = rpc

    try:
      self.con.connect()
    except IOError, e:
      print "RoboUser: Couldn't connect: %s" % e
      sys.exit(0)
    else:
      print "RoboUser: Connected"
    self.con.process(1)
    reg = self.con.getRegInfo()
    print 'RoboUser: reginfo', reg
    # Set up a jabber account
    self.con.setRegInfo('username', username)
    self.con.setRegInfo('password', password)
    self.con.setRegInfo('resource', resource)
    self.con.sendRegInfo()
    print "RoboUser: sent registration info"
    self.con.process(1)
    
    if con.auth(self.username, self.password, self.resource):
	print "RoboUser: Logged in as %s to server %s" % (self.username, self.server)
    else:
	print "RoboUser: error -> ", con.lastErr, con.lastErrCode
	sys.exit(0)

    print "Requesting Roster Info"
    self.roster = con.requestRoster()
    con.sendInitPresence()
    print "RoboUser created"
    self.createConference()

  def createConference(self):
    """
    Use the newer Multi-User Conference spec (vs the older groupchat spec)
    Multi-step process; not totally sure of sequence (i.e., whether something gets received between these)
    1). First, send presence to the room (to see if it exists):
    <presence to="X2180@conference.localhost" id="3"> <priority>0</priority> </presence>
    2). Next send an IQ to the conference:
    <iq to="X2180@conference.localhost" id="conf_1" type="set">
    <query xmlns="jabber:iq:conference">
    <nick>X_2180</nick>
    <name>X_2180</name>
    </query>
    </iq>
    3). Finally, send a presence to the room:
    <presence to="X2180@conference.localhost" id="4">
    <status>Normal attention</status>
    <priority>0</priority>
    </presence>
    
    """
    # first message:
    roomName = "X"+str(self.username)
    pres = jabber.Presence(to=roomName+'@conference.'+str(self.server))
    self.con.send(pres)
    # second message  
    confSetUpIq = jabber.Iq(to=roomName+'@conference.'+str(self.server))
    confSetUpIq.setType('set')
    confSetUpIq.setID('COM_'+str(self.username))
    query = confSetUpIq.setQuery("jabber:iq:conference")
    node = query.insertTag('nick')
    node.putData("X_"+roomName)
    node = query.insertTag('name')
    node.putData("X"+roomName)
    self.con.send(confSetUpIq)
    print "confSetUpIq", confSetUpIq
    # final message
    pres = jabber.Presence(to=roomName+'@conference.'+str(self.server))
    
    self.con.send(pres)
    
  def createRoster(self, users):
    print "robo user: users:", users
    self.con.sendInitPresence()
    self.roster = self.con.requestRoster()
    for user in users:
      self.sendSubscriptionMessage(user)
      self.sendWelcomeMessage(user)

  def  sendSubscriptionMessage(self, user):
    pres = jabber.Presence(to=str(user))
    pres.setID("JCOM"+str(user))
    pres.setType('subscribe')
    pres.setStatus('Normal Subscription Request')
    self.con.send(pres)
    
  def sendWelcomeMessage(self,user):
    m = jabber.Message()
    m.setFrom(self.username)
    m.setTo(user)
    m.setType('chat')
    responseString = 'join me in conference X'+str(self.username)
    m.setBody(responseString)
    self.con.send(m) # send message back to the service requester. "It worked"

    
  def usage(self):
      print "%s is a python jabber client to log group chats" % sys.argv[0]
      sys.exit(0)
 

  def messageCB(self, con, msg):
    """Called when a message is recieved"""
    print "robo user: messageCB", str(msg)
    if msg.getType() == 'groupchat':
      self.observations.append(str(msg.getBody()))

      if msg.getBody() == 'RECORD':
	self.polarisServer = xmlrpclib.Server(self.rpc)
	observationString = str(self.username)+" Observation:\r\n"
	for observation in self.observations:
	  observationString =observationString + observation +'\r\n'
	print "POSTING: "+ observationString
	self.polarisServer.remote.addObservation(int(self.username), str(self.username), observationString)
    
  def presenceCB(self, con, prs):
    """Called when a presence is recieved
    expect something like: RECV: <presence to='y@localhost' type='subscribed' from='x@localhost'/>
    """
    print "RoboUser: presenceCB",str(prs)  
    if prs.getType() == 'subscribed':
      print 'got subscribed message'
      # respond to subscriber:
      # SENT: <presence to="x@localhost" type="subscribed"/>
      pres = jabber.Presence(to=str(prs.getFrom()))
      pres.setID("JCOM"+str(self.username))
      pres.setType('subscribed')
      pres.setStatus('Normal Subscription Response')
      self.con.send(pres)

  def run(self):
    
    while 1:
      #~ print "RoboUser: process. Delay =", self.DELAY
      self.con.process(self.DELAY)

  def setDELAY(self, delay):
    self.DELAY = delay
  def getDELAY(self):
    return self.DELAY
    
  def iqCB(self, con,iq):
    print "RoboUser: recieved InfoQuery", str(iq) 
    print "RoboUser: returning."
    return 1
  def disconnectedCB(self, con):
      print "ERROR: network disconect"
      sys.exit(1)

# ## 
# simple test driver vvvvvvvvvv
# ##
if __name__ == '__main__':
 
  if len(sys.argv) == 5:
    r = RoboUser(server=sys.argv[1],username=sys.argv[2],password=sys.argv[3],resource=sys.argv[4] )
    users = ['y@localhost']
    r.createRoster(users)
    r.start()
  else:
    r.usage()
    sys.exit(0)
  print "RoboUser: processing incoming connections"
  #~ while 1:
    #~ pass
    
