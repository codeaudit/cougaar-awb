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
import org.cougaar.util.UnaryPredicate;

import com.bbn.awb.GOL.CellStatusPredicate;

/**
 * @author Dana Moore
 * 
 * TODO To change the template for this generated type comment go to Window -
 * Preferences - Java - Code Style - Code Templates
 */
public class CellularAutomatonPlugin extends ComponentPlugin {
	UIDService uidService;

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
		System.out.println(agentId+":UIDService:" + uidService);
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

		String target_name = "GameManager";
		MessageAddress target = MessageAddress.getMessageAddress(target_name);
		if (agentId.equals(target)) {
			System.out.println(agentId+":sending to myself..." + agentId);
			return;
		}
		UID uid = uidService.nextUID();
		GameMessage query = new GameMessage("ALIVE");
		SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);
		blackboard.publishAdd(sr);

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
		      System.out.println("observe added "+sr);
		   
		      if (agentId.equals(sr.getTarget())) {
		        // send back reply
		        sr.setReply("echo-"+sr.getQuery());
		        System.out.println("Reply "+sr);		        
		        blackboard.publishChange(sr);
		      } else {
		      	System.out.println("ignore relays we sent");
		      }
		    }

		    // observe changed relays
		    for (Enumeration en = gameStatus.getChangedList(); en.hasMoreElements();) {
		      SimpleRelay sr = (SimpleRelay) en.nextElement();
		      System.out.println("observe changed "+sr);
		      
		      if (agentId.equals(sr.getSource())) {
		        // got back answer
		        System.out.println(agentId+":Received "+sr);
		        // remove query both locally and at the remote target
		        // this is optional, but it's a good idea to clean up and
		        // free some memory.
		        blackboard.publishRemove(sr);
		      } else {
		        System.out.println(agentId+"ignore our own reply");
		      }
		    }
		      // removed relays
		      for (Enumeration en = gameStatus.getRemovedList(); en.hasMoreElements();) {
		        SimpleRelay sr = (SimpleRelay) en.nextElement();
		        System.out.println(agentId+" :observe removed "+sr);
		      }
	}

}