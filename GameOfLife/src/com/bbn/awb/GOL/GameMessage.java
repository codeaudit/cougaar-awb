/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;
import java.io.Serializable;

import java.util.Set;
import java.util.Collections;

import org.cougaar.core.relay.*;
import org.cougaar.core.relay.Relay.TargetFactory;
import org.cougaar.core.relay.Relay.Token;
import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.util.*;




/**
 * @author Dana Moore
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class GameMessage  { 
	private String[] stateRegister = {
			"GO",
			"ALIVE",
			"DEAD"
	};
	private String state  = null;

	public GameMessage(String state){
		this.state = state;
	}
	/**
	 * @return Returns the state.
	 */
	public String getState() {
		return state;
	}

}
