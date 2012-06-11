/*
 * Created on Sep 3, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.util.UnaryPredicate;

/**
 * @author Dana Moore
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public final class CellStatusPredicate implements UnaryPredicate {
  private final MessageAddress agentId;
  public CellStatusPredicate(MessageAddress agentId) {
    this.agentId = agentId;
  }
  public boolean execute(Object o) {
    if (o instanceof SimpleRelay) {
      SimpleRelay sr = (SimpleRelay) o;
//      System.out.println("MESSAGE FROM <<< "+sr.getSource()+" TO >>> "+sr.getTarget()+"...\n\t((("+sr.getReply()+")))");
      return
        (agentId.equals(sr.getSource()) ||
         agentId.equals(sr.getTarget()));
    }
    return false;
  }
}	