/*
 * Created on Sep 3, 2004
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
//import java.util.Collection;
import java.util.Enumeration;
import java.util.Iterator;

import org.cougaar.core.blackboard.IncrementalSubscription;
//import org.cougaar.core.blackboard.Subscription;
import org.cougaar.core.component.ServiceBroker;
import org.cougaar.core.logging.LoggingServiceWithPrefix;
import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.plugin.ComponentPlugin;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.core.relay.SimpleRelaySource;
import org.cougaar.core.service.LoggingService;
import org.cougaar.core.service.UIDService;
import org.cougaar.core.util.UID;
import org.cougaar.util.UnaryPredicate;

/**
 * Example SimpleRelay client, which both sends relays and replies
 * to them.
 * <p>
 * To use, add this component to an agent and specify a target,
 * for example in "AgentA" with a target of "AgentB":<pre>
 *   &lt;component
 *       name='org.cougaar.core.relay.SimpleRelayExample(target=AgentB)'
 *       class='org.cougaar.core.relay.SimpleRelayExample'
 *       priority='COMPONENT'
 *       insertionpoint='Node.AgentManager.Agent.PluginManager.Plugin'&gt;
 *     &lt;argument&gt;target=AgentB&gt;/argument&gt;
 *   &lt;/component&gt;
 * </pre>
 * In the target agent add the component without a target argument:<pre>
 *   &lt;component
 *       name='org.cougaar.core.relay.SimpleRelayExample(target=AgentB)'
 *       class='org.cougaar.core.relay.SimpleRelayExample'
 *       priority='COMPONENT'
 *       insertionpoint='Node.AgentManager.Agent.PluginManager.Plugin'/&gt;
 * </pre>
 * You should see output similar to the following, which excludes
 * logging timestamps and other details:<pre>
 *   .. AgentA: Sending (.. query=ping reply=null)
 *   .. AgentB: Reply (.. query=ping reply=echo-ping)
 *   .. AgentA: Received (.. query=ping reply=echo-ping)
 * </pre>
 * <p>
 * It would be straight-forward to extend this example to a more
 * general remote procedure call (<u>RPC</u>) utility:  the query
 * specifies a String "method" name and Object[] parameters, and
 * the reply is either a Throwable or a non-error value, plus a
 * wrapper if the non-error value is null or a Throwable.  As in
 * RMI, the parameters and return value must be Serializable and
 * treated as immutable.
 */
public class SimpleRelayExample extends ComponentPlugin {

  private LoggingService log;
  private UIDService uids;

  private IncrementalSubscription sub;

  public void load() {
    super.load();

    // get services
    ServiceBroker sb = getServiceBroker();
    log = (LoggingService)
      sb.getService(this, LoggingService.class, null);
    uids = (UIDService)
      sb.getService(this, UIDService.class, null);

    // prefix all logging calls with our agent name
    log = LoggingServiceWithPrefix.add(log, agentId+": ");

    if (log.isDebugEnabled()) {
      log.debug("loaded");
    }
  }

  protected void setupSubscriptions() {
    if (log.isDebugEnabled()) {
      log.debug("setupSubscriptions");
    }

    // create relay subscription
    sub = (IncrementalSubscription)
      blackboard.subscribe(new MyPred(agentId));

    // send relays
    for (Iterator iter = getParameters().iterator(); iter.hasNext();) {
      String s = (String) iter.next();
      if (!s.startsWith("target=")) {
        continue;
      }
      String target_name = s.substring("target=".length());
      MessageAddress target =
        MessageAddress.getMessageAddress(target_name);
      if (agentId.equals(target)) {
        if (log.isWarnEnabled()) {
          log.warn("Ignoring target that matches self: "+target);
        }
        continue;
      }
      UID uid = uids.nextUID();
      Object query = "ping";
      SimpleRelay sr = new SimpleRelaySource(
          uid, agentId, target, query);
      if (log.isShoutEnabled()) {
        log.shout("Sending "+sr);
      }
      blackboard.publishAdd(sr);
    }
  }

  protected void execute() {
    if (log.isDebugEnabled()) {
      log.debug("execute");
    }

    if (!sub.hasChanged()) {
      // usually never happens, since the only reason to execute
      // is a subscription change
      return;
    }

    // observe added relays
    for (Enumeration en = sub.getAddedList(); en.hasMoreElements();) {
      SimpleRelay sr = (SimpleRelay) en.nextElement();
      if (log.isDebugEnabled()) {
        log.debug("observe added "+sr);
      }
      if (agentId.equals(sr.getTarget())) {
        // send back reply
        sr.setReply("echo-"+sr.getQuery());
        if (log.isShoutEnabled()) {
          log.shout("Reply "+sr);
        }
        blackboard.publishChange(sr);
      } else {
        // ignore relays we sent
      }
    }

    // observe changed relays
    for (Enumeration en = sub.getChangedList(); en.hasMoreElements();) {
      SimpleRelay sr = (SimpleRelay) en.nextElement();
      if (log.isDebugEnabled()) {
        log.debug("observe changed "+sr);
      }
      if (agentId.equals(sr.getSource())) {
        // got back answer
        if (log.isShoutEnabled()) {
          log.shout("Received "+sr);
        }
        // remove query both locally and at the remote target.
        //
        // this is optional, but it's a good idea to clean up and
        // free some memory.
        blackboard.publishRemove(sr);
      } else {
        // ignore our reply
      }
    }

    if (log.isDebugEnabled()) {
      // removed relays
      for (Enumeration en = sub.getRemovedList(); en.hasMoreElements();) {
        SimpleRelay sr = (SimpleRelay) en.nextElement();
        log.debug("observe removed "+sr);
      }
    }
  }

  /**
   * My subscription predicate, which matches SimpleRelays where my
   * local address matches either the source or target.
   */
  private static class MyPred implements UnaryPredicate {
    private final MessageAddress agentId;
    public MyPred(MessageAddress agentId) {
      this.agentId = agentId;
    }
    public boolean execute(Object o) {
      if (o instanceof SimpleRelay) {
        SimpleRelay sr = (SimpleRelay) o;
        return
          (agentId.equals(sr.getSource()) ||
           agentId.equals(sr.getTarget()));
      }
      return false;
    }
  }
}
