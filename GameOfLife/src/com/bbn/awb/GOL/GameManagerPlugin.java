/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cougaar.core.blackboard.IncrementalSubscription;
import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.service.AgentIdentificationService;
import org.cougaar.core.service.UIDService;
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

	private UnaryPredicate cellStatusPredicate = new UnaryPredicate() {
		public boolean execute(Object o) {
			System.out.println(agentId + " cellStatusPredicate fired");

			if (o instanceof GameMessage) {
				System.out.println(agentId + ":GameMessage Recieved:"
						+ ((GameMessage) o).getState());
			}
			return true;
		}
	};

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.plugin.ComponentPlugin#setupSubscriptions()
	 */
	protected void setupSubscriptions() {
		// TODO Auto-generated method stub

			GameMessage g = new GameMessage("GO");
			getBlackboardService().publishAdd(g);


		cellStatus = (IncrementalSubscription) getBlackboardService()
				.subscribe(cellStatusPredicate);
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.plugin.ComponentPlugin#execute()
	 */
	protected void execute() {
		// loops forever ...
	
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
		System.out.println(agentId
				+ " <<< AgentIdentification");
		if (agentId == null) {
			throw new RuntimeException("Agent id is null");
		}

		// get UID service
		uidService = (UIDService) getServiceBroker().getService(this,
				UIDService.class, null);
		System.out.println("GameManagerPlugin:UIDService:" + uidService);
		if (uidService == null) {
			throw new RuntimeException("Unable to obtain agent-id service");
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
			System.out.println("GameManagerPlugin:" + name + "=" + value);
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