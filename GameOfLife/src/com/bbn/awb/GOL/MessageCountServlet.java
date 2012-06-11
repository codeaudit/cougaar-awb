/*
 * Created on Sep 30, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;

import javax.servlet.ServletException;
import javax.servlet.http.*;

//import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.core.servlet.SimpleServletSupport;


/**
 * @author jnilsson
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class MessageCountServlet extends HttpServlet {
	private SimpleServletSupport support;
	
	public void setSimpleServletSupport(SimpleServletSupport support)
	{
	  this.support = support;
	}

	public void doGet(
	    HttpServletRequest request,
	    HttpServletResponse response) throws IOException, ServletException
	{
	  execute(request, response);
	}

	public void doPost(
	     HttpServletRequest request,
	     HttpServletResponse response) throws IOException, ServletException
	{
	  execute(request, response);
	}

	private void execute(
	       HttpServletRequest request,
	       HttpServletResponse response) throws IOException, ServletException
	{
	  	PrintWriter out = response.getWriter();
	  	out.println("<html>");
	  	out.println("<table>");
		HashMap messageCount = calcMessageCount();
		Iterator itr = messageCount.keySet().iterator();
		while (itr.hasNext())
		{
			String target = (String) itr.next();
			Integer count = (Integer) messageCount.get(target);
			out.println("<tr><td>"+target+"</td><td>"+count.toString()+"</td></tr>");			
		}
	  	out.println("</table>");
	  	out.println("</html>");
	}
	
	private HashMap calcMessageCount()
	{
	  	Collection messageCollection = 
	  		support.queryBlackboard(new CellStatusPredicate(support.getAgentIdentifier()));
	  	HashMap messageCount = new HashMap();
	  	Iterator itr = messageCollection.iterator();
	  	while (itr.hasNext())
	  	{
	  		SimpleRelay sr = (SimpleRelay) itr.next();
	  		String msg_src = sr.getSource().toString();
	  		String msg_dest = sr.getTarget().toString();
	  		String agent;
	  		if (msg_src.equals(support.getAgentIdentifier().toString()))
	  			agent = msg_dest;
			else
				agent = msg_src;
	  		if (messageCount.keySet().contains(agent))
			{
	  			int count = ((Integer) messageCount.get(agent)).intValue();
	  			count++;
	  			messageCount.put(agent, new Integer(count));
			}
	  		else
	  		{
	  			messageCount.put(agent, new Integer(1));
	  		}	
	  	}	  	
	  	return messageCount;

	}
}
