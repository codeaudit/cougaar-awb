/*
 * Created on Aug 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

/**
 * @author Dana Moore
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class GameMessage {
	private String[] stateRegister = {
			"ALIVE",
			"DEAD"
	};
	private String state  = null;

	public GameMessage(String state){
	}
	/**
	 * @return Returns the state.
	 */
	public String getState() {
		return state;
	}

}
