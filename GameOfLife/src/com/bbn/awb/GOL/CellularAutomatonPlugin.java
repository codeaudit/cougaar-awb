/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.util.Enumeration;
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

	Vector neighbors = new Vector();

	private String myState = new String();

	private IncrementalSubscription gameStatus; // Tasks that I'm interested in

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

			if (!agentId.equals(msg_src)) { //Ignore messages to self
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
			blackboard.publishRemove(sr);
		}
	}

	/**
	 *  
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
	}

	/**
	 * @param msg_src
	 */
	private void handleQuery(MessageAddress msg_src) {
		// TODO Auto-generated method stub
		sendMessage("RESPONSE", myState, msg_src.toString());
	}

	/**
	 *  
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
		myState = msg_param;
		sendMessage("READY", null, "GameManager");
	}

	/**
	 *  
	 */
	private void handleGo() {
		// TODO Auto-generated method stub
		System.out.println(agentId.toString() + " starting next iteration");

	}

	/**
	 * @param msg
	 * @param target_name
	 */
	private void sendMessage(String type, String param, String target_name) {
		// TODO Auto-generated method stub
		MessageAddress target = MessageAddress.getMessageAddress(target_name);
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
	 * @param state
	 */
	private void setState(String state) {
		// TODO Auto-generated method stub
		myState = state;
	}

	/**
	 * make conversaations with adjacent cells. calculate my state based on
	 * number of received responses
	 *  
	 */
	private void calculateState() {
		// TODO Auto-generated method stub

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