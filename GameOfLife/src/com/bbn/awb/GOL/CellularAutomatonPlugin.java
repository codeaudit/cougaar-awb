/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.util.Enumeration;

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
			if (!agentId.equals(sr.getSource())) {
				printMessageData("^^^ ", sr);
				printMessage(agentId.toString().toUpperCase(), sr);
				if (sr.getSource().toAddress().equals("GameManager")) {
					System.out.println("\t\tgot message from GameManager");
				}
				setState(((GameMessage) sr.getQuery()).getState());
				calculateState();
				returnStateToGameManager(((GameMessage) sr.getQuery()).getState());
			}
			blackboard.publishRemove(sr);
		}		
	}

	/**
	 * @param state
	 */
	private void setState(String state) {
		// TODO Auto-generated method stub
		myState = state;
	}

	/**
	 * 
	 */
	private void returnStateToGameManager(String state) {
		String target_name = "GameManager";
				MessageAddress target =
		 MessageAddress.getMessageAddress(target_name);
				if (agentId.equals(target)) {
					System.out.println(agentId + ":sending to myself..." + agentId);
					return;
				}
				UID uid = uidService.nextUID();
				GameMessage query = new GameMessage(state);
				SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);
				blackboard.publishAdd(sr);

		
	}

	/**
	 * make conversaations with adjacent cells.
	 * calculate my state based on number of received responses
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
					((GameMessage) sr.getQuery()).getState());
		}

		if (sr.getReply() != null && sr.getReply() instanceof GameMessage) {
			sB.append(" Query Reply->>>").append(
					((GameMessage) sr.getReply()).getState());
		}

		System.out.println(sB.toString());
	}

}