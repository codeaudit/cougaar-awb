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
public class GameMessage 
implements 
Relay.Source, Relay.Target, UniqueObject { 
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
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Source#getTargets()
	 */
	public Set getTargets() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Source#getContent()
	 */
	public Object getContent() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Source#getTargetFactory()
	 */
	public TargetFactory getTargetFactory() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Source#updateResponse(org.cougaar.core.mts.MessageAddress, java.lang.Object)
	 */
	public int updateResponse(MessageAddress arg0, Object arg1) {
		// TODO Auto-generated method stub
		return 0;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.util.UniqueObject#getUID()
	 */
	public UID getUID() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.util.UniqueObject#setUID(org.cougaar.core.util.UID)
	 */
	public void setUID(UID arg0) {
		// TODO Auto-generated method stub
		
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Target#getSource()
	 */
	public MessageAddress getSource() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Target#getResponse()
	 */
	public Object getResponse() {
		// TODO Auto-generated method stub
		return null;
	}
	/* (non-Javadoc)
	 * @see org.cougaar.core.relay.Relay.Target#updateContent(java.lang.Object, org.cougaar.core.relay.Relay.Token)
	 */
	public int updateContent(Object arg0, Token arg1) {
		// TODO Auto-generated method stub
		return 0;
	}

}
