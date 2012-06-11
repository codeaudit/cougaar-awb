/*
 * Created on Sep 24, 2004
 *
 * TODO To change the template for this generated file go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
package com.bbn.awb.GOL;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.cougaar.core.mts.MessageAddress;
import org.cougaar.core.relay.SimpleRelay;
import org.cougaar.core.servlet.SimpleServletSupport;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.Collection;
import java.util.Iterator;


/**
 * @author jnilsson
 *
 * TODO To change the template for this generated type comment go to
 * Window - Preferences - Java - Code Style - Code Templates
 */
public class CellStatusServlet extends HttpServlet {
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
	  	Collection status_collection =  
	  		support.queryBlackboard(new CellStatusPredicate(support.getAgentIdentifier()));
	  	String state = "Undetermined";
	  	Iterator itr = status_collection.iterator();
	  	while (itr.hasNext())
	  	{
			SimpleRelay sr = (SimpleRelay) itr.next();
			String msg_type = ((GameMessage) sr.getQuery()).getType();
			String msg_param = ((GameMessage) sr.getQuery()).getParam();
			MessageAddress msg_src = sr.getSource();
			//Only care about Response messages from self.  They indicate state.
			if (msg_src.equals(support.getAgentIdentifier()) && 
					msg_type.equals(GameMessage.RESPONSE_MESSAGE)) 
				state = msg_param;			
	  	}
	  	out.println("Cell : "+support.getAgentIdentifier().toString()+"<BR>");
	  	out.println("State: "+state+"<BR>");
	  	out.println("</html>");
	  }
}
