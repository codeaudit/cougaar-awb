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

	private Map cell_ready = new HashMap();    //Keep track of READY/BUSY status
	private Map cell_neighbors = new HashMap(); //Count registered neighbors per node
    private int rows;
	private int neighbor_ack_count = 0;
    
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
				rows = Integer.parseInt(s.substring(s.indexOf("=")+1, s.length()));
			if (s.toLowerCase().indexOf("target") < 0)
				continue;

			String target_name = s
					.substring(s.indexOf("=") + 1, s.indexOf(":"));
			String target_value = s.substring(s.indexOf(":") + 1, s.length());

			cell_ready.put(target_name, new Boolean(false));
			cell_neighbors.put(target_name, new Integer(0));
			
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
			GameMessage query = new GameMessage("INIT", target_value);
			SimpleRelay sr = new SimpleRelayImpl(uid, agentId, target, query);

			blackboard.publishAdd(sr);

		}
		sendNeighborList(); // initial knowledge of who each cell's neighbor is

	}

	private void sendNeighborList(){
		String[][] cells;
		int numCells = cell_ready.size();
		int cols = numCells / rows;
		cells = new String[rows][cols];
		
		Iterator itr = cell_ready.keySet().iterator();
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
                	GameMessage query = new GameMessage("NEIGHBOR", n[k]);
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
		System.out.println ("iteration:"+i+" "+j);
		String[] n = new String[8];
		int prevrow = (i-1+rows) % rows;
		int prevcol = (j-1+cols) % cols;
		int nextrow = (i+1) % rows;
		int nextcol = (j+1) % cols;
		
		n[0] = cells[prevrow][prevcol];
		n[1] = cells[prevrow][j];
		n[2] = cells[prevrow][nextcol];
		n[3] = cells[i][prevcol];
		n[4] = cells[i][nextcol];
		n[5] = cells[nextrow][prevcol];
		n[6] = cells[nextrow][j];
		n[7] = cells[nextrow][nextcol];
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
		for (Enumeration en = cellStatus.getAddedList(); en.hasMoreElements();) {
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
					handleInit();
				else if (msg_type.equals(GameMessage.READY_MESSAGE))
					handleReady(msg_src.toString());
				else if (msg_type.equals(GameMessage.QUERY_MESSAGE))
					handleQuery();
				else if (msg_type.equals(GameMessage.RESPONSE_MESSAGE))
					handleResponse();
				else if (msg_type.equals(GameMessage.NEIGHBOR_MESSAGE))
					handleNeighbor();
				else if (msg_type.equals(GameMessage.NEIGHBOR_ACK_MESSAGE))
					handleNeighborAck(msg_src.toString());
			}
			blackboard.publishRemove(sr);
		}
	}



	/**
	 * 
	 */
	private void handleNeighborAck(String msg_src) {
		// TODO Auto-generated method stub
		int i = ((Integer) cell_neighbors.get(msg_src)).intValue();
		cell_neighbors.put(msg_src, new Integer(i+1));
		if (allNeighborsRegistered() && allCellsReady())
			sendGo();
	}

	/**
	 * 
	 */
	private void sendGo() {
		// TODO Auto-generated method stub
		Iterator itr = cell_ready.keySet().iterator();
		System.out.println("Starting next generation");
		try{
		Thread.sleep(20000); //Sleep a bit so iterations don't go too fast
		}catch (Exception e){}
		while (itr.hasNext())
		{
			String cell_name = (String) itr.next();
			sendMessage("GO", null, cell_name);
			cell_ready.put(cell_name, new Boolean(false));
		}
		
	}


	/**
	 * @return
	 */
	private boolean allCellsReady() {
		// TODO Auto-generated method stub
		Iterator itr = cell_ready.values().iterator();
		while (itr.hasNext())
		{
		 if (!((Boolean) itr.next()).booleanValue())
			return false;
		}
		return true;
	}

	/**
	 * @return
	 */
	private boolean allNeighborsRegistered() {
		// TODO Auto-generated method stub
		Iterator itr = cell_neighbors.values().iterator();
		while (itr.hasNext())
		{
			if (((Integer) itr.next()).intValue() != 8)
				return false;
		}
		return true;
	}

	
	/**
	 * @param msg_param
	 */
	private void handleNeighbor() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "+ GameMessage.NEIGHBOR_MESSAGE+
				"  That shouldn't hapen...");
	}

	/**
	 * @param msg_param
	 * @param string
	 */
	private void handleResponse() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "+ GameMessage.RESPONSE_MESSAGE+
		"  That shouldn't hapen...");
	}

	/**
	 * @param msg_src
	 */
	private void handleQuery() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "+ GameMessage.QUERY_MESSAGE+
		"  That shouldn't hapen...");
	}

	/**
	 * @param msg_src
	 * 
	 */
	private void handleReady(String msg_src) {
		// TODO Auto-generated method stub
		cell_ready.put(msg_src, new Boolean(true));
		if (allNeighborsRegistered() && allCellsReady())
			sendGo();
	}

	/**
	 * @param msg_param
	 */
	private void handleInit() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "+ GameMessage.INIT_MESSAGE+
		"  That shouldn't hapen...");
		
	}

	/**
	 * 
	 */
	private void handleGo() {
		// TODO Auto-generated method stub
		System.out.println(agentId + ":Got a "+ GameMessage.GO_MESSAGE+
		"  That shouldn't hapen...");		
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