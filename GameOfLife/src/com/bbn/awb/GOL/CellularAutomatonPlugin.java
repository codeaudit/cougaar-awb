/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import org.cougaar.core.blackboard.IncrementalSubscription;
import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.service.AgentIdentificationService;
import org.cougaar.util.UnaryPredicate;

/**
 * @author Dana Moore
 * 
 * TODO To change the template for this generated type comment go to Window -
 * Preferences - Java - Code Style - Code Templates
 */
public class CellularAutomatonPlugin extends ComponentPlugin {

	public void load() {
		super.load();


	}

	private IncrementalSubscription gameStatus; // Tasks that I'm interested in

	private UnaryPredicate cellStatusPredicate = new UnaryPredicate() {
		public boolean execute(Object o) {
			System.out.println(agentId + " cellStatusPredicate fired");
			if (o instanceof GameMessage) {
				System.out.println(agentId + ":GameMessage Recieved:"
						+ ((GameMessage) o).getState());
				return true;
			}
			return false;
		}
	};

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.blackboard.BlackboardClientComponent#setupSubscriptions()
	 */
	protected void setupSubscriptions() {
		// TODO Auto-generated method stub
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
		gameStatus = (IncrementalSubscription) getBlackboardService()
				.subscribe(cellStatusPredicate);
		GameMessage g = new GameMessage("ALIVE");
		getBlackboardService().publishAdd(g);

	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see org.cougaar.core.blackboard.BlackboardClientComponent#execute()
	 */
	protected void execute() {


	}

}