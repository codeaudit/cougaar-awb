/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;
//import java.io.Serializable;

//import java.util.Set;
//import java.util.Collections;
//
//import org.cougaar.core.relay.*;
//import org.cougaar.core.relay.Relay.TargetFactory;
//import org.cougaar.core.relay.Relay.Token;
//import org.cougaar.core.mts.MessageAddress;
//import org.cougaar.core.util.*;




/**
 * @author Dana Moore
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class GameMessage  { 
//	private String[] stateRegister = {
//			"GO",       //start next iteration
//			"INIT",     //send initial state
//			"READY",    //ready for next iteration 
//			"QUERY",    //Query a state
//			"RESPONSE", //Respond to QUERY
//			"NEIGHBOR",  //Create a neighbor connection between two cells
//			"NEIGHBOR_ACK"  //Create a neighbor connection between two cells
//			
//	};

	public static final String GO_MESSAGE = "GO";
	public static final String INIT_MESSAGE = "INIT";
	public static final String READY_MESSAGE = "READY";
	public static final String QUERY_MESSAGE = "QUERY";
	public static final String RESPONSE_MESSAGE = "RESPONSE";
	public static final String NEIGHBOR_MESSAGE = "NEIGHBOR";
	public static final String NEIGHBOR_ACK_MESSAGE = "NEIGHBOR_ACK";
	
	private String type  = null;
	private String param = null;
	
	public GameMessage(String type){
		this.type = type;
	}
	
	public GameMessage(String type, String param){
		this.type = type;
		this.param = param;
	}
	
	/**
	 * @return Returns the param.
	 */
	public String getParam() {
		return param;
	}
	/**
	 * @return Returns the type.
	 */
	public String getType() {
		return type;
	}
}
