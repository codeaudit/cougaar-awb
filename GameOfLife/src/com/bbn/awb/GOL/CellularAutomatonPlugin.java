/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.util.Collection;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.Vector;

import org.cougaar.core.blackboard.IncrementalSubscription;
import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.core.relay.SimpleRelayImpl;
import org.cougaar.core.service.AgentIdentificationService;
import org.cougaar.core.service.UIDService;
import org.cougaar.core.util.UID;
//import org.cougaar.util.UnaryPredicate;

import com.bbn.awb.GOL.CellStatusPredicate;

/**
 * @author Dana Moore
 * 
 * TODO To change the template for this generated type comment go to Window -
 * Preferences - Java - Code Style - Code Templates
 */
public class CellularAutomatonPlugin extends ComponentPlugin {
	UIDService uidService;

	private Vector neighbors = new Vector();
    private Vector neighbor_status = new Vector();
	
	private String myState = new String();

	private IncrementalSubscription gameStatus; // Tasks that I'm interested in

	public static final String STATUS_ALIVE = "ALIVE";
	public static final String STATUS_DEAD = "DEAD";
	

	public void load() {
		super.load();
		// get agent id
		AgentIdentificationService agentIdService = (AgentIdentificationService) getServiceBroker()
				.getService(this, AgentIdentificationService.class, null);
		if (agentIdService == null) {
			throw new RuntimeException("Unable to obtain agent-id service");
		}
		agentId = agentIdService.getMessageAddress();
		String agentIdString = agentIdService.getName();
		getServiceBroker().releaseService(this,
				AgentIdentificationService.class, agentIdService);
		System.out.println(agentId + " <<<AgentIdentification");
		if (agentId == null) {
			throw new RuntimeException("Agent id is null");
		}
		// get UID service
		uidService = (UIDService) getServiceBroker().getService(this,
				UIDService.class, null);
		System.out.println(agentId + ":UIDService:" + uidService);
		if (uidService == null) {
			throw new RuntimeException("Unable to obtain Uid service");
		}

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.blackboard.BlackboardClientComponent#setupSubscriptions()
	 */
	protected void setupSubscriptions() {

		// create relay subscription
		gameStatus = (IncrementalSubscription) blackboard
				.subscribe(new CellStatusPredicate(agentId));

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.blackboard.BlackboardClientComponent#execute()
	 */
	protected void execute() {
		if (!gameStatus.hasChanged()) {
			// usually never happens, since the only reason to execute
			// is a subscription change
			return;
		}

		// observe added relays
		for (Enumeration en = gameStatus.getAddedList(); en.hasMoreElements();) {
			SimpleRelay sr = (SimpleRelay) en.nextElement();
			String msg_type = ((GameMessage) sr.getQuery()).getType();
			String msg_param = ((GameMessage) sr.getQuery()).getParam();
			MessageAddress msg_src = sr.getSource();

			if (!agentId.equals(msg_src)) { //Ignore messages from self
				printMessageData("^^^ ", sr);
				printMessage(agentId.toString().toUpperCase(), sr);
				if (msg_type.equals(GameMessage.GO_MESSAGE))
					handleGo();
				else if (msg_type.equals(GameMessage.INIT_MESSAGE))
					handleInit(msg_param);
				else if (msg_type.equals(GameMessage.READY_MESSAGE))
					handleReady();
				else if (msg_type.equals(GameMessage.QUERY_MESSAGE))
					handleQuery(msg_src);
				else if (msg_type.equals(GameMessage.RESPONSE_MESSAGE))
					handleResponse(msg_param, msg_src.toString());
				else if (msg_type.equals(GameMessage.NEIGHBOR_MESSAGE))
					handleNeighbor(msg_param);
				else if (msg_type.equals(GameMessage.NEIGHBOR_ACK_MESSAGE))
					handleNeighborAck();
			}
			//blackboard.publishRemove(sr);
		}
	}

	/**
	 *  Cells shouldn't recieve NEIGHBOR_ACK messages
	 */
	private void handleNeighborAck() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "
				+ GameMessage.NEIGHBOR_ACK_MESSAGE
				+ "  That shouldn't hapen...");
	}

	/**
	 * @param msg_param
	 */
	private void handleNeighbor(String msg_param) {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Creating neighbor connection to "
				+ msg_param);
		neighbors.add(msg_param);
		sendMessage(GameMessage.NEIGHBOR_ACK_MESSAGE,
				msg_param /* here, taken to mean my neighbor */, 
				"GameManager");
	}

	/**
	 * @param msg_param
	 * @param msg_src
	 */
	private void handleResponse(String msg_param, String msg_src) {
		// TODO Auto-generated method stub
		System.out.println("Got response " + msg_param + " from " + msg_src);
        //Source doesn't mattter. We only care about the number of living neighbors
		neighbor_status.add(msg_param); 
	    if (neighbor_status.size() == neighbors.size()){
	    	setState(calc_state());
	    	sendMessage(GameMessage.READY_MESSAGE, null, "GameManager");
	    }	
	}

	/**
	 * @param msg_src
	 */
	private void handleQuery(MessageAddress msg_src) {
		// TODO Auto-generated method stub
		sendMessage(GameMessage.RESPONSE_MESSAGE, myState, msg_src);
	}

	/**
	 * Cells shouldn't recieve ready messages.  
	 */
	private void handleReady() {
		// TODO Auto-generated method stub
		System.out.println(agentId
				+ ":Got a READY message.  That shouldn't hapen...");
	}

	/**
	 * @param msg_param
	 */
	private void handleInit(String msg_param) {
		// TODO Auto-generated method stub
		setState(msg_param);
		sendMessage(GameMessage.READY_MESSAGE, null, "GameManager");		
	}

	/**
	 *  
	 */
	private void handleGo() {
		// TODO Auto-generated method stub
		System.out.println(agentId.toString() + " starting next iteration");
        Iterator itr = neighbors.iterator();
        neighbor_status = new Vector();
        while (itr.hasNext())
        	sendMessage(GameMessage.QUERY_MESSAGE, null, (String) itr.next());
        //We've sent out our qeuries now wait for them to come back        
	}

	/**
	 * Rules for GOL:
	 * With 3 living neighbors dead cell comes alive
	 * With 2 or 3 living neighbors living cell stays alive
	 * Else die/remain dead
	 * @return State for this iteratrion
	 */
	private String calc_state() {
		// TODO Auto-generated method stub
		int num_alive = 0;
		Iterator itr = neighbor_status.iterator();
		while (itr.hasNext()){
			if (((String)itr.next()).equals("ALIVE"))
				num_alive++;
		}
		if (num_alive == 3)
			return "ALIVE";
		if (num_alive == 2)
			return myState;
		
		return "DEAD";
	}

	/**
	 * @param string
	 */
	private void setState(String state) {
		myState = state;
		
		//Remove old state from blackboard and add new state
		//possibly create ASSERT message toput own state on blackboard
		//Currently using RESPONSE
	  	Collection status_collection = blackboard.query(new CellStatusPredicate(agentId));
	  	Iterator itr = status_collection.iterator();
	  	while (itr.hasNext())
	  	{
			SimpleRelay sr = (SimpleRelay) itr.next();
			String msg_type = ((GameMessage) sr.getQuery()).getType();
			String msg_param = ((GameMessage) sr.getQuery()).getParam();
			MessageAddress msg_src = sr.getSource();
			//Only care about Responses.  They indicate state.
			
			if (msg_src.equals(agentId) && 
					msg_type.equals(GameMessage.RESPONSE_MESSAGE))
			{
				System.out.println(agentId+": Removing old state from blackboard: "+msg_param);				
				blackboard.publishRemove(sr);
			}
	  	}
		sendMessage(GameMessage.RESPONSE_MESSAGE, state, agentId.toString());		
	}
	
	/**
	 * @param msg
	 * @param param
	 * @param target
	 */
	private void sendMessage(String type, String param, MessageAddress target) {
		if (agentId.equals(target)) {
			System.out.println(agentId + ":sending to myself..." + agentId);
			return;
		}
		UID uid = uidService.nextUID();
		GameMessage query = new GameMessage(type, param);
		SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);
		blackboard.publishAdd(sr);	
	}
	
	/**
	 * Overloading to accept target as a string
	 * @param msg
	 * @param param
	 * @param target_name
	 */
	private void sendMessage(String type, String param, String target_name) {
		// TODO Auto-generated method stub
		MessageAddress target = MessageAddress.getMessageAddress(target_name);
		sendMessage(type, param, target);
	}



	private void printMessageData(String extra, SimpleRelay sr) {
		System.out.println(extra + agentId.toString().toUpperCase()
				+ " :DST-> " + sr.getTarget() + " :SRC-> " + sr.getSource());
	}

	/**
	 * @param sr
	 */
	private void printMessage(String me, SimpleRelay sr) {
		StringBuffer sB = new StringBuffer();
		sB.append("\t");
		if (sr.getQuery() != null && sr.getQuery() instanceof GameMessage) {
			sB.append("Query Message->>>").append(
					((GameMessage) sr.getQuery()).getType());
		}

		if (sr.getReply() != null && sr.getReply() instanceof GameMessage) {
			sB.append(" Query Reply->>>").append(
					((GameMessage) sr.getReply()).getType());
		}

		System.out.println(sB.toString());
	}

}