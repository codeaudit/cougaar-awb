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

//import org.cougaar.util.UnaryPredicate;

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

	private Map targets = new HashMap();
    private int rows;
	
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

		// send initial relays with initial cell states
		for (Iterator iter = getParameters().iterator(); iter.hasNext();) {
			String s = (String) iter.next();
			if (s.toLowerCase().indexOf("rows") >= 0)
				rows = Integer.parseInt(s.substring(s.indexOf("="), s.length()));
			if (s.toLowerCase().indexOf("target") < 0)
				continue;

			String target_name = s
					.substring(s.indexOf("=") + 1, s.indexOf(":"));
			String target_value = s.substring(s.indexOf(":") + 1, s.length());

			targets.put(target_name, target_value);
			System.out.println(agentId + " :target_name" + target_name
					+ " target_value " + target_value);
			MessageAddress target = MessageAddress
					.getMessageAddress(target_name);
			if (agentId.equals(target)) {
				System.out
						.println(agentId + " :sending to myself..." + agentId);
				return;
				//	        continue;
			}
			UID uid = uidService.nextUID();
			GameMessage query = new GameMessage(target_value);
			SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);

			blackboard.publishAdd(sr);

		}

	}

	private void sendNeighborList(){
		String[][] cells;
		int numCells = targets.size();
		int cols = numCells / rows;
		cells = new String[rows][cols];
		
		Iterator itr = targets.keySet().iterator();
		int i = 0;
		int j = 0;
		while (itr.hasNext()){
			cells[i][j] = (String) itr.next();
			i++;
			if (i == rows){
				i = 0;
				j++;
			}
		}
		
		for(i = 0; i < rows; i++){
			for(j = 0; j < cols; j++){
				String[] n = neighborList(i, j, cells, cols);
				MessageAddress target = MessageAddress.getMessageAddress(cells[i][j]);
                for(int k = 0; k < n.length; k++){
                	UID uid = uidService.nextUID();
                	GameMessage query = new GameMessage("Neighbor:"+n[k]);
                	SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);
                	blackboard.publishAdd(sr);
                }
			}
		}
	}
	
		

	/**
	 * @param i
	 * @param j
	 * @param cells
	 * @param cols
	 * @return
	 */
	private String[] neighborList(int i, int j, String[][] cells, int cols) {
		// TODO Auto-generated method stub
		String[] n = new String[8];
		n[0] = cells[(i-1)%rows][(j-1)%cols];
		n[0] = cells[(i-1)%rows][j];
		n[0] = cells[(i-1)%rows][(j+1)%cols];
		n[0] = cells[i][(j-1)%cols];
		n[0] = cells[i][(j+1)%cols];
		n[0] = cells[(i+1)%rows][(j-1)%cols];
		n[0] = cells[(i+1)%rows][j];
		n[0] = cells[(i+1)%rows][(j+1)%cols];
		return n;
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
			//System.out.println(agentId+":observe added " + sr);

			if (agentId.equals(sr.getTarget())) {
				// send back reply
				sr.setReply("echo-" + sr.getQuery());
				//				System.out.println(agentId+":REPLY " + sr);
				blackboard.publishChange(sr);
			} else {
				//				System.out.println(agentId+":ignoring relays we sent");
			}
		}

		// observe changed relays
		for (Enumeration en = cellStatus.getChangedList(); en.hasMoreElements();) {

			SimpleRelay sr = (SimpleRelay) en.nextElement();
			//System.out.println(agentId.toString().toUpperCase()+":observe
			// changed " + sr);

			if (agentId.equals(sr.getSource())) {
				// got back answer
				// printMessageData("~~~ ", sr);
				// printMessage(agentId.toString().toUpperCase(), sr);
				// remove query both locally and at the remote target.
				// this is optional, but it's a good idea to clean up and
				// free some memory.
				blackboard.publishRemove(sr);
			} else {
				//			System.out.println(agentId.toString().toUpperCase()+":RECIEVED
				// FROM " + sr.getSource()+" TO "+sr.getTarget()+"
				// getQuery:::"+sr.getQuery());
				printMessageData("^^^ ", sr);
				printMessage(agentId.toString().toUpperCase(), sr);
				//			System.out.println(agentId+":ignore our reply");
			}
		}

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
		System.out.println(agentId + ":UIDService:" + uidService);
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
			//			System.out.println(agentId + ":"+ name + "=" + value);
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