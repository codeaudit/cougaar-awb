/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.util.Enumeration;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.cougaar.core.blackboard.IncrementalSubscription;
import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.core.relay.SimpleRelayImpl;
import org.cougaar.core.service.AgentIdentificationService;
import org.cougaar.core.service.UIDService;
import org.cougaar.core.util.UID;
import org.cougaar.util.UnaryPredicate;

/**
 * @author Dana Moore
 * 
 * TODO To change the template for this generated type comment go to Window -
 * Preferences - Java - Code Style - Code Templates
 */
public class GameManagerPlugin extends ComponentPlugin {
	UIDService uidService;

	private boolean initDone = false;

	private Map props;

	private IncrementalSubscription cellStatus; // Tasks that I'm interested in

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.plugin.ComponentPlugin#setupSubscriptions()
	 */
	protected void setupSubscriptions() {

		// TODO Auto-generated method stub

		GameMessage g = new GameMessage("GO");
		getBlackboardService().publishAdd(g);
		// create relay subscription
		cellStatus = (IncrementalSubscription) blackboard
				.subscribe(new CellStatusPredicate(agentId));

		// send relays
		//	    for (Iterator iter = getParameters().iterator(); iter.hasNext();) {
		//	      String s = (String) iter.next();
		//	      if (!s.startsWith("target=")) {
		//	        continue;
		//	      }
		//	      String target_name = s.substring("target=".length());
		String target_name = "Cell00";
		MessageAddress target = MessageAddress.getMessageAddress(target_name);
		if (agentId.equals(target)) {
			System.out.println(agentId+" :sending to myself..." + agentId);
			return;
			//	        continue;
		}
		UID uid = uidService.nextUID();
		GameMessage query = new GameMessage("GO");
		SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);

		blackboard.publishAdd(sr);
		//	    }
		// end added code
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.plugin.ComponentPlugin#execute()
	 */
	protected void execute() {
		if (!cellStatus.hasChanged()) {
			// usually never happens, since the only reason to execute
			// is a subscription change
			return;
		}

		// observe added relays
		for (Enumeration en = cellStatus.getAddedList(); en.hasMoreElements();) {
			SimpleRelay sr = (SimpleRelay) en.nextElement();
			System.out.println(agentId+":observe added " + sr);

			if (agentId.equals(sr.getTarget())) {
				// send back reply
				sr.setReply("echo-" + sr.getQuery());
				System.out.println(agentId+":REPLY " + sr);
				blackboard.publishChange(sr);
			} else {
				System.out.println(agentId+":ignoring relays we sent");
			}
		}

		// observe changed relays
		for (Enumeration en = cellStatus.getChangedList(); en.hasMoreElements();) {
			SimpleRelay sr = (SimpleRelay) en.nextElement();
			System.out.println(agentId+":observe changed " + sr);
			
			if (agentId.equals(sr.getSource())) {
				// got back answer
				System.out.println(agentId+":RECIEVED " + sr);
				
				// remove query both locally and at the remote target.
				//
				// this is optional, but it's a good idea to clean up and
				// free some memory.
				blackboard.publishRemove(sr);
			} else {
				System.out.println(agentId+":ignore our reply");
			}
		}


	}

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
		System.out.println(agentId + " <<< AgentIdentification");
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

		// get parameters
		List params = (List) getParameters();
		props = new HashMap();
		for (int i = 0; i < params.size(); i++) {
			String s = (String) params.get(i);
			String name = null;
			String value = null;
			int sep = s.indexOf('=');
			if (sep >= 0) {
				name = s.substring(0, sep);
				value = s.substring(sep + 1);
			}
			System.out.println(agentId + ":"+ name + "=" + value);
			props.put(name, value);
		}

	}

	public void unload() {
		if (uidService != null) {
			getServiceBroker().releaseService(this, UIDService.class,
					uidService);
			uidService = null;
		}
	}

}