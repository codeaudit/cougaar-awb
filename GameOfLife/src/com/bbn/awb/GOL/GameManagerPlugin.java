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

import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.service.AgentIdentificationService;
import org.cougaar.core.service.UIDService;

/**
 * @author Dana Moore
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class GameManagerPlugin extends ComponentPlugin {
	UIDService uidService;
	private Map props;
	public GameManagerPlugin(){
		}
	/* (non-Javadoc)
	 * @see org.cougaar.core.plugin.ComponentPlugin#setupSubscriptions()
	 */
	protected void setupSubscriptions() {
		// TODO Auto-generated method stub
		
	}

	/* (non-Javadoc)
	 * @see org.cougaar.core.plugin.ComponentPlugin#execute()
	 */
	protected void execute() {
		// TODO Auto-generated method stub
		
	}
	public void load() {
	    super.load();



	    // get agent id
	    AgentIdentificationService agentIdService = 
	      (AgentIdentificationService) 
	      getServiceBroker().getService(
	          this, AgentIdentificationService.class, null);
	    if (agentIdService == null) {
	      throw new RuntimeException(
	          "Unable to obtain agent-id service");
	    }
	    agentId = agentIdService.getMessageAddress();
	    getServiceBroker().releaseService(
	        this, AgentIdentificationService.class, agentIdService);
	    System.out.println("GameManagerPlugin:AgentIdentificationService>>>:"+agentIdService.getName());
	    if (agentId == null) {
	      throw new RuntimeException(
	          "Agent id is null");
	    }

	    // get UID service
	    uidService = (UIDService) 
	      getServiceBroker().getService(
	          this, UIDService.class, null);
	    System.out.println("GameManagerPluginUIDService:"+uidService);
	    if (uidService == null) {
	      throw new RuntimeException(
	          "Unable to obtain agent-id service");
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
	        value = s.substring(sep+1);
	      }
	      props.put(name, value);
	    }


	  }

	  public void unload() {
	    if (uidService != null) {
	      getServiceBroker().releaseService(
	          this, UIDService.class, uidService);
	      uidService = null;
	    }
	  }

}
