CSMARTer '03 Installation and Users' Manual

Version 1.2
November 7, 2003


Part I.  OVERVIEW

CSMARTer ’03 presents the following features to the user in a graphical 
interface:

·  Creation (from scratch) of Cougaar societies and associated attributes,
   such as facets, parameters, class, priority, insertion point, etc.
·  Display of Cougaar societies read from pre-existing XML files;
·  Viewing and editing of Cougaar societies, including drag-and-drop editing;
·  Finding and sorting Cougaar society entities
·  Extensive facility for adding, deleting, displaying, editing, copying, and 
   pasting facets;
·  Saving of Cougaar societies as XML files;
·  Creation, display, and editing of society transformation rules in Python
   or Ruby;
·  Society transformation using Python or Ruby rules;
·  Layout of Cougaar agents from an agent list onto a set of hosts using 
   several different allocation methodologies:
   o	Manual (drag-and-drop)
   o	Automatic
      - Even distribution
      - Distribution by specified number of agents per host
	- Distribution by facet
      - Distribution of agents with their associated nodes to a new set of 
        hosts


Part II.  INSTALLATION

1.  CSMARTer uses the following third party software: 

	Python    The Python language interpreter
	wxPython  Libraries for creating a graphical user interface in Python
	4Suite    Python XML Parser

Assistance in finding and installing these applications, where necessary, is 
provided below.


2.  Getting and installing CSMARTer:

	a.  CSMARTer zip file (Windows only):  The best way to get CSMARTer is
to download the CSMARTer zip file ("CSMARTer.zip") from Docushare (under 
UltraLog -> Software Downloads).  Unzip this file into the subdirectory of 
your choice and the installation is complete.  Note that no Python, 
wxPython, or 4Suite installation is required.

	b.  CSMARTer Installer (Windows only):  The next best way to get 
CSMARTer is to download the installer (CSMARTer-1.2.win32.exe) from Docushare 
(under UltraLog -> Software Downloads).  After downloading, double-click on 
the installer file and it will install itself into your Python directory in 
the Lib/site-packages subdirectory.  Note, however, that this option requires
a pre-existing installation of Python, wxPython, and 4Suite (see paragraph 
2.e, below).

	c.  CSMARTer .tar file (Linux only):  Download the file
CSMARTer-1.2-linux.tar.gz from Docushare (under UltraLog -> Software 
Downloads) into the directory of your choice.  Ensure this directory is in
your PYTHONPATH environment variable.  Unpack the tarball.  Note that this 
option requires an existing installation of Python, wxPython, and 4Suite 
(see paragraph 2.f, below).


	d.  CSMARTer code (Windows or Linux):  If you need to have the latest 
CSMARTer source code, download the CVS repository from the TIC by entering:

	cvs -d :ext:yourname@cvs.ultralog.net:/cvs/commons/isat co csmart

If you don't have cvs access, contact Tom Copeland (tom@infoether.com).
When checkout is complete, the CSMARTer application will be located at 
csmart/src/python.  It contains the CSMARTer and ACMEPy directories.  Note 
that this option requires an existing installation of Python, wxPython, 
and 4Suite (see paragraph 2.e or 2.f, below).

The remainder of these instructions will use the term "CSMARTER_INSTALL_PATH" 
to point to the directory to which you installed or unzipped the application 
(i.e., the directory containing the CSMARTer subdirectory).

	e.  Installing the prerequisite software (Windows):

		(1) Download and install the latest version of Python from:

	   		www.python.org (latest version as of this writing is 2.3).

		(2) Download and install the latest version of wxPython from:
 
	   		http://www.wxpython.org/download.php (latest version as of 
         		this writing is 2.4.2.4).

		(3) Download and install the Python XML parser from: 

	   		http://4suite.org/docs/howto/Windows.xml
	
	   	Click the link to:

	   		ftp://ftp.4suite.org/pub/4Suite/ 
	
	   	Then download:

	   		4Suite-1.0a3.win32-py2.3.exe 

	   	by double-clicking on it.  Note that the file to download may 
	   	change as new versions of Python and 4Suite are released.
	
		(4) Set PATH to include the python executable.

		(5) If running directly from CVS checked out code, set a 
	   	PYTHONPATH environment variable to include the python 
		site-packages directory and the csmart\src\python directory.  For 
		example, if Python is installed in C:\python23 and 
		CSMARTER_INSTALL_PATH points to the csmart directory (checked out 
		from the cvs repository at the TIC as explained above), then 
		PYTHONPATH=
	   	C:\python23\site-packages;CSMARTER_INSTALL_PATH\src\python


	f.  Installing the prerequisite software (Linux):


		(1) Red Hat Linux 8 ships with version 2.2.1 or 2.2.2 of Python, 
                but download and installation of the latest version of Python 
                is recommended.  Go to:

	   		www.python.org (latest version as of this writing is 2.3.2).

                (Before installing a new version of Python, if you want to 
		    preserve the original distribution version, move the python
		    executable "python" from /usr/bin to /usr/lib/python2.x.)

		    The RPM binaries for Python 2.3.x only work with Red Hat 9, 
                so if you are running Red Hat 9, download the RPM and install.
                If you are running an earlier version of Red Hat, you will 
                have to download the source and build it yourself.  To do 
                this, download the Python source tarball for the latest 
                version (the .tgz or .tar.bz2 file) to your home directory,
                unpack it, then run the following commands to compile and
                install:

			./configure --prefix=/usr
			make
			make install

                This will install the Python executable to your /usr/bin
		    directory and the rest of Python to your /usr/lib/python2.3 
                directory. 

		(2) Download and install the latest version of wxPython from:
 
	   		http://www.wxpython.org/download.php 

		    (latest version as of this writing is 2.4.2.4).  Click on the 
		    link for wxPythonGTK under "For Python 2.3".  Download the 
		    binary RPM to your home directory, log in as root, and install 
		    the RPM with:

			rpm -i [RPM filename]

		    This will install wxPython into your 
		    /usr/lib/python2.3/site-packages directory.

		(3) Download and install the Python XML parser from: 

	   		http://4suite.org/docs/howto/UNIX.xml
	
	   	    Click the link to:

	   		ftp://ftp.4suite.org/pub/4Suite/ 
	
	   	    Then download:

	   		4Suite-1.0a3.tar.gz

	   	    by double-clicking on it.  Note that the file to download 
	   	    may change as new versions of Python and 4Suite are released.  
 	   	    Follow the installation instructions provided on the 4Suite 
		    web page.  This will install 4Suite in your 
		    /usr/lib/python2.3/site-packages directory.
	
		(4) Ensure PATH is set to include the Python executable (should 
		    already include /usr/bin).

		(5) Set an environment variable PYTHONPATH to include the python 
		    site-packages directory and your CSMARTER_INSTALL_PATH. 
		    For example, if Python is installed in /usr/lib/python2.3, 
		    then set PYTHONPATH=
	   	    /usr/lib/python2.3/site-packages:CSMARTER_INSTALL_PATH


Part III.  STARTING CSMARTER

1.	a.  If CSMARTer was obtained via the CSMARTer.zip file (Part II, 
paragraph 2.a), execute cs03.exe to start CSMARTer.  

	b.  If CSMARTer was obtained via the installer (Part II, paragraph 
2.b), Windows users can start CSMARTer by running the batch file, 
CSMARTer.bat, located in (Python dir)\Lib\site-packages\CSMARTer.  

	c.  Linux users who downloaded the .tar file should change directory 
to CSMARTER_INSTALL_PATH/CSMARTer and launch the program by entering:

	python CS03.py

	d.  Users running from the CSMARTer source code checked out from CVS 
can start CSMARTer either by running the CSMARTer.bat file at 
CSMARTER_INSTALL_PATH/CSMARTer (Windows only) or by changing directory to 
their CSMARTER_INSTALL_PATH/CSMARTer and entering:

	python CS03.py


Part IV.  USING CSMARTER

1.  Functionality Description

The CSMARTer application window contains four tabbed panes: Overview, Rules, 
Society Editor, and Agent Laydown.

	a.  Overview

	The Overview tabbed pane presents a page of text that simply provides 
an overview of each of the other tabbed panes.  It is not intended to be a 
complete Help facility.  Users should view this pane for a quick overview of 
CSMARTer.

	b.  Rules

	The Rules tabbed pane allows the user to create, view, edit, and apply 
society transformation rules.  The rules can be written in either Python or 
Ruby.  Python rule files should be named with the file extension ".rul", 
while Ruby rules should use the extension "rule".  

		(1)  Creating a new rule

		Click the "Create New Rule" button.  Begin typing the rule in the 
editor window.  Start the rule by including a comment that describes the 
purpose of the rule.  CSMARTer reads the first sentence of this comment (or 
the first line if it contains no periods) as a description of the rule, and 
places this description in the "Rule Description" text box when the rule is 
next opened in the Rules pane.  Save the rule when done.
KNOWN BUG: Once the rule has been saved, it will appear in the Rulebook pane.
There is no way to get it out of the Rulebook pane without closing CSMARTer.
WORKAROUND: Just ignore it.  If you need to use it to transform a society,
just use it as usual.  If you open the rulebook into which the rule was 
saved, the new rule will appear twice in the Rulebook pane.  This causes no
problem beyond simple annoyance since use of either instance of the rule
will give the proper result.

		(2)  Opening an existing rule

		A "rulebook" is simply a directory containing rules.  To open an 
existing rule, click the "Open RuleBook" button and navigate to the directory
containing the rule(s) you wish to open.  Select it, then click "OK".  The 
rule files contained in that rulebook will appear in the CheckListBox in the 
Rules pane.  To open the rule in the editor window, simply click on the rule 
name in the CheckListBox.  Once a rule is opened, it can be replaced in the 
editor window with a different rule by clicking on that new rule's name in 
the CheckListBox.

Multiple Rulebooks can be open concurrently.  To close an open Rulebook, 
select View -> Close Rulebook from the menu bar.

		(3)  Saving a rule

		To save a rule, simply click the "Save Rule" button at the bottom 
of the Rules pane, or select File -> Save Rule or File -> Save Rule As... 
from the menu bar.

		(4)  Editing a rule

		Once a rule is opened in the Rules pane, it can be edited with 
most standard text editing commands.  

		(5)  Applying a rule

		To apply a rule to a society (i.e., to transform the society), 
open the rulebook(s) containing the rule(s) to be applied.  Ensure the 
society to be transformed has been opened (i.e., the society's name is 
visible in the "Current Society" text box at the top of the Rules tabbed 
pane), then check the checkboxes next to each rule to be applied (any number 
of rules may be checked), then click the "Apply Rules" button.  If the 
society to be transformed is not yet opened, open it by clicking the "Open 
Society" button at the bottom of the Rules pane.  When the society is open, 
its name will appear in the Current Society text box.  Then you may click on 
the "Apply Rules" button.  An alternative method of opening the society is to 
click on the Society Editor tab and open the society in that tabbed pane, 
where it can be reviewed prior to transformation, then return to the Rules 
pane.  

The completion of the transformation can be determined by watching the log 
messages that appear in the log pane at the bottom of the CSMARTer window.  
Once the transformation is complete, its effect can be seen by switching to 
the Society Editor pane.  Added or changed society entities will be 
highlighted in cyan.

		(6)  Undoing a rule transformation
	
		When a society, has been transformed by the application of one or
more rules, this transformation can be backed out by pressing the "Undo 
Transform" button.  The society will revert to the state it was in prior to 
the application of the rule(s).  It is important to note that ALL changes 
made to the society after the application of the rule(s) will be lost.  A
warning dialog box pops up when the "Undo Transform" button is pressed to 
ensure the user is aware of, and approves of, the effect of backing out the 
rule.

		(7)  Deleting or renaming a rule

		Rules can be deleted by selecting the rule in the Rulebook 
window, then clicking on Edit -> Delete Rule in the menu bar.  Similarly,
rules can be renamed by selecting the rule in the Rulebook window, then
clicking on Edit -> Rename Rule in the menu bar.  


	c.  Society Editor

	The Society Editor allows a user to create, view, and/or edit a 
complete society.  Main society entities (society, hosts, nodes, agents, 
components, and arguments) are displayed in a hierarchical tree format.  

		(1)  Creating a society

		To create a society from scratch, right click in the blank 
Society Editor window and select Create Society from the popup menu.  Enter 
a name into the dialog box for the society being created and press <Enter>.  
The society will appear as the root node of the society tree.  Right-clicking 
on this society tree item produces a popup menu from which the user can add a 
host, delete the society, or rename the society.  To add a host, choose the 
Add A Host menu item.  Another dialog box appears that permits the user to 
create a host by entering the host name.  When the host is added, it can be 
right-clicked to add a node or perform other operations.  A similar process 
can be followed to add agents, components, and arguments.

		(2)  Viewing/Editing a society

		Pre-existing societies can be displayed by reading them in from 
an XML file.  Click the Open Society button and select the desired XML file 
from the File Chooser.  If the society fails to display, check the log pane 
for error messages.  If the XML file contains an error, CSMARTer will issue a
Parse Error and the log message will indicate the nature of the problem.  An
alternate way to open a society in the Society Editor is available if the
society of interest is already open in the Agent Laydown tabbed pane: click 
the "Get HNA Map" button and the same society opened in the HNA Map (right 
side) window of the Agent Laydown pane is opened in the Society Editor.  
However, whereas society entities below the agent level are not shown in the
Agent Laydown pane (even when they exist), these entities ARE shown in the
Society Editor.

When the society is initially displayed, it is visible only down to the host
level.  To view entities below that, click on the plus sign ("+") next to the 
host of interest to view that host's children, or select View on the menu bar
then Show Entire Society, Show All Nodes, Show All Agents, or Show All 
Components to expand the society tree to the desired level.  The View menu 
can also be used to collapse the society tree to the desired level.  

When a society has been transformed by applying rules, the society entities
affected by the rule appear highlighted in cyan.  To aid in finding these
highlighted entities, press the "Next Highlight" button.  The tree display
will expand and scroll to the next highlighted entity not already visible.
Successive clicks of the "Next Highlight" button will reveal additional
highlighted items until all are visible.  At this point, the "Next 
Highlight" button will be disabled.  To remove the highlighting from an item,
simply click on it.
KNOWN BUG: Once society items are changed by a rule and highlighted, 
each subsequent application of rules will cause the highlighting to reappear 
on the original items.
WORKAROUND: Save the society, close it, and reopen it.  Highlighting will be
gone.

To reduce clutter, only the main society entities are displayed in the 
society tree; related information (such as facets, class, parameters, 
priority, insertion point) are available by right-clicking on the entity of 
interest and selecting View/Edit Info from the popup menu.  These associated 
data can also be edited by right-clicking on the data item to be edited and 
selecting the desired function from the popup menu.  Right-clicking on an 
item in the View/Edit Info tree display gives the user the opportunity to 
delete or edit the item and to add another sibling (if the data element can 
have multiple values).  Right-clicking on a parent item also allows the user 
to add a child item (unless it only takes a single value and that value is 
already present).  
IMPORTANT NOTE: If selecting View/Edit Info from a society entity's right-
click popup menu does not produce the View/Edit Info display, there is 
probably a previously displayed View/Edit Info window that has not been 
closed.  ONLY ONE VIEW/EDIT INFO WINDOW CAN BE OPEN AT A TIME.

When a society is opened in the Society Editor, CSMARTer automatically 
creates a node agent for each node and attaches it to that node.  Components 
associated with the node are attached as children of the node agent FOR
DISPLAY ONLY; when the society is saved, the node agent does not appear in 
the XML file, while the components appear as child elements of the node in 
the XML file.

An open society may be edited by right-clicking on an item of interest and
selecting the desired function from the popup menu.  Entities can be added,
deleted, or renamed in this manner.

Entities can be moved and/or copied by dragging and dropping.  This operation
also supports reordering of child entities.

Other operations available in the Edit menu in the menu bar include:
	
	Sort: Select a society entity, then click on Edit -> Sort to sort the
		child items under the selected entity alphabetically.

	Find/Find Next: Enter a string of text and any society entity name 
		containing this string will be made visible and highlighted in 
		blue.

	Change Nameserver: The society nameserver appears as a parameter on 
		each node.  This function changes the host that is to act as the 
		nameserver.  Note that the default nameserver is the first host
		listed in the society.
		KNOWN BUG: If, after changing the nameserver, the society is 
		saved then reopened, the new nameserver is forgotten.
		WORKAROUND: Change the nameserver each time the society file
		is opened.

		(3)  Closing/Saving a society

		When the user is through with a society, it may be either closed
or saved.  To close, click the Close Society button.  If the society has 
changed, the user will be prompted to save it; otherwise, the society tree
display will be cleared.  To save the society, click the Save Society button
to save the society as an XML file with the same name as the file originally
opened (overwriting the original file), or select File -> Save Society As to
save it as a separate file with a new name.  The functionality of the Save
Society button is duplicated by the File -> Save Society menu item.


	d.  Agent Laydown

	The purpose of the Agent Laydown tabbed pane is to allow agents to be
distributed from a list of agents to individual nodes and hosts.  This pane 
is more complicated than the others, but also provides more functionality.  
The concept of operations is that a one-host, one-node society with many 
agents (an "agent list") is opened in the left window while a society with 
multiple hosts (and possibly nodes, but no agents) is opened in the right 
window.  The user then maps agents to nodes, resulting in a "Host-Node-Agent 
(HNA) Map".  This mapping may be done automatically by CSMARTer or manually 
by the user through drag and drop.  The major features of the Agent Laydown 
pane are described below.

		(1) Create/Open an Agent List

		An agent list may be created from scratch by right-clicking 
inside a blank Agent List window and selecting Create Society.  The process 
is identical to that described in section c (Society Editor).  To open an 
existing agent list society, click the Open Agent List button on the left 
side and select an XML file to open from the File Chooser.

		(2) Create/Open an HNA Map

		There are several ways to obtain an HNA Map society.  First is to
create it manually by right clicking in an empty HNA Map window and selecting
Create Society, then manually creating the necessary hosts by right clicking
on the society item and selecting Create Host from the popup menu.  Second is
to click the Open HNA Map button and open an existing society XML file.  
Finally, a new society can be created quickly by clicking the Build HNA Map 
button in the center (between the two windows), which produces the Create New
HNA Map dialog box.  Enter a society name (optional; CSMARTer will create a 
default name if this text box is left blank), then enter the number of hosts 
to create.  The host names are constructed by CSMARTer by concatenating the
string in the Prefix text box with a sequence string.  Specify the starting
value of the sequence string in the Sequence Begins At text box; when 
CSMARTer creates the designated number of hosts, it will use this starting 
value in the name of the first host, then increment the the sequence value by 
one for each subsequent host.  The starting value may be either one or more 
numbers or one or more letters.  Repeat this process for node creation.  If 
creation of only hosts is desired, check the "Do not create nodes" checkbox.  
Conversely, if only nodes are desired, check the "Do not create hosts" 
checkbox.  CSMARTer will provide a default arrangement of the nodes on the 
available hosts, and will create a default host if nodes but no hosts are 
created.  As an example of the flexibility of this process, the user can 
create 20 hosts, then 10 nodes with one prefix, then repeat the process by 
checking "Do not create hosts" and creating 10 more nodes with a different 
prefix (and starting sequence value, if desired).  CSMARTer will place the 
first ten nodes on the first ten hosts, and the second ten nodes on the 
second ten hosts.

		(3)  Distribute agents

		Agents from the agent list can be distributed to the HNA Map (the
"mapped society") either manually by drag and drop or automatically by 
CSMARTer.  The manual method is self-explanatory and will not be discussed
further.  There are currently three automatic distribution methods: 
(1) distributing agents evenly across the hosts in the mapped society;
(2) by specifying the number of agents to be mapped to each host; and
(3) by distributing agents or nodes based on facets.  The selection of one of 
these three options is made by selecting one of the radio buttons in the 
center of the Agent Laydown pane.  

If "Distribute evenly" is selected, the agents are distributed evenly among
the hosts in the HNA Map.  If a host contains multiple nodes, the agents are
also distributed evenly across the nodes within that host, but the number of
agents allocated to that host is not affected by the number of nodes on the
host.

If "Specify number per host" is selected, an initial number of agents per 
host must be specified (though CSMARTer provides a suggested default value).
Also, the number of nodes to place on each host is selectable (default is 1).
(default is 1).  If more than one node is specified per host, then the agents 
allocated to that host are evenly distributed across the nodes.  If the agent 
list already contains nodes, checking the "Include Nodes from Agent List" 
checkbox will bring the nodes (with their agents) from the agent list to the 
HNA Map, distributing them evenly across the available hosts.  To maintain 
the same node-to-host mapping, select the "Maintain same distribution" radio 
button.  

If the "Distribute by facet" radio button is selected, the user can 
distribute agents either (1) selected from the Agent List or (2) agents 
specified by the type and value of one or more of their facets.  The 
destination to which these agents will be distributed can be specified 
either by specific host or node name or by a set of host or node facets.  
If the "Include Nodes from Agent List" checkbox is checked, then nodes can be 
distributed rather than agents.  When multiple facets are chosen as selection 
criteria, the user can designate whether the facets are to be combined using 
"AND" boolean logic or "OR" logic.

When all the option selections are made, click the Distribute Agents 
button (it will be labelled "Distribute Nodes" if the "Include Nodes from 
Agent List" checkbox is checked).  Note that when distribution of nodes is 
included, any facets present on the hosts in the agent list are automatically 
transferred to the hosts in the HNA Map.  To prevent this facet transfer, 
check the "Ignore Host Facets" checkbox.  If the "Distribute by facet" radio
button was selected, clicking the "Distribute Agents" (or "Distribute Nodes")
button opens a dialog box that permits the user to make the selections 
necessary to perform the operations described in the previous paragraph.  
Once the distribution is complete, if the result is unsatisfactory, the 
operation may be reversed by clicking on Edit -> Undo in the menu bar.

Additional functionality related to agent distribution includes:

			(a)  Exclude Node/Agent from distro: Occasionally, it may 
be desirable to distribute all agents and/or nodes in the agent list except 
for certain nodes and/or agents.  Similarly, it may not be desirable to 
distribute nodes and/or agents to every host and/or node in the HNA Map.  For 
example, if a certain host in the HNA Map has already had nodes and agents 
allocated to it manually (via drag and drop) and the user desires to complete 
the remainder of the distribution using CSMARTer's automatic distribution 
feature without allocating still more nodes/agents to that host, it can be 
excluded from receiving additional nodes/agents.  This is accomplished by 
right clicking on the entity to be excluded (nodes or agents in the agent 
list, hosts or nodes in the HNA Map), and selecting 
"Exclude [host | node | agent] from distro" from the popup menu.  Excluded
hosts, nodes, or agents are highlighted in red.

			(b)  Once a distribution has been made, individual entities
can be "unassigned" without undoing the entire distribution by right clicking
on the entity to unassign and selecting "Unassign" from the popup menu.  This
operation removes the entity from the HNA Map and returns it to the agent
list.  If an entity is unassigned but there is no open society in the agent
list window, a "temp society" is automatically created as a harness to hold 
the unassigned entity.

		(4)  Working with facets

		Several capabilities are provided for working with facets.  They 
are available by right-clicking on a society, host, node, or agent tree item
and selecting the desired function from the popup menu.  Show and Hide 
functions affect all entities of the same type as the selected entity.  Other
functions affect only the selected entity.

Facet functions available on all entities:
	
	Show Specified Facets: Brings up a dialog box allowing the user to
specify one or more existing facet types (with or without specific values)
to display in the tree itself, immediately following the entity name.
	Show All Facets: Displays all available facets in the tree itself,
immediately following the entity name.  Facets appear in key=value format.
	Hide All Facets (only available when facets are shown): Removes the 
facets from the tree display (does not disassociate the facet from the 
entity).
	View/Edit Facets: Brings up a dialog box showing the facets on the 
selected entity.  Allows users to add, delete, edit, or copy facets.  Right 
clicking on an existing facet produces a popup menu containing add, delete, 
and copy options.  Left-clicking a selected facet allows editing.  If there 
are noexisting facets shown in the dialog box, right-clicking on the column 
header bar of the dialog box produces a popup menu allowing the user to add 
a facet.
	Add Facets: A more flexible way of adding facets than that provided by
the Edit Facets function.  Provides a dialog box with dropdown boxes 
containing likely facet types and values.  Also permits adding the specified
facet to the selected entity only or to all entities of the same type as the
selected entity.  
	Delete Facets: A more flexible way of deleting facets than that 
provided by the Edit Facets function.  Provides a dialog box with dropdown 
boxes containing the existing facets on the selected entity.  Also permits 
deleting the specified facet from the selected entity only or from all 
entities of the same type as the selected entity (where that facet exists).

Facet functions available on Hosts and Nodes only:
	
	Copy Facets: Copies all facets on the selected entity and stores them 
on a clipboard, destroying the previous clipboard contents.
	Paste Facets: Pastes the facets on the clipboard into the selected 
entity.  Pasting does not remove the facets from the clipboard.

Facet functions available on Hosts only:

	Show Enclave Facet: Displays the value of the enclave facet in the tree
itself, immediately following the host name.  This display appears for every
host.
	Show Service Facet: Displays the value of the service facet in the tree
itself, immediately following the host name.  This display appears for every
host.

Facet functions available on Nodes only:

	Show Role Facet: Displays the value of the role facet in the tree
itself, immediately following the node name.  This display appears for every
node.

		(5)  Viewing Summary Statistics on the Society

		The right-click popup menu for the Society and for Hosts con-
tains a "View Society Summary" menu item.  Selecting this item produces a
dialog box containing the following information about the HNA Map society:

	- Society Name
	- Number of hosts, nodes, and agents
	- List of hosts with the number of nodes on each of those hosts

		(6)  Deleting Society Entities

		The right-click popup menu for each entity contains a "Delete" 
menu item.  If the selected entity is the Society or an Agent, delete 
destroys the entity.  If the selected entity is the Society, the XML file is 
also deleted from the disk.  Warning dialog boxes provide an opportunity to 
cancel the operation.  If the selected entity is a Host or Node, the entity 
itself is destroyed, but its children (if any) are moved to the Agent List 
window.

		(7)  Finding and Sorting

		Other operations available in the Edit menu in the menu bar 
include:
	
	Sort: Select a society entity, then click on Edit -> Sort to sort the
		child items alphabetically under the selected entity.

	Find/Find Next: Enter a string of text and any society entity name 
		containing this string will be made visible and highlighted in 
		blue.

		(8)  Saving an Agent List

		The society displayed in the Agent List window CANNOT BE SAVED.  
It is intended as merely a "holding area" for agents (and sometimes nodes).
Societies that a user desires to save should be created and/or edited in the
HNA Map window.

		(9)  Saving an HNA Map 

The society displayed in the HNA Map can be saved my clicking the Save HNA 
Map button above the HNA Map window.  This button is a "Save As" button the
first time the mapped society is saved in that it always gives the user a 
File Chooser dialog box and requires the input of a file name for the saved 
file.  This is to prevent a user from inadvertently overwriting a society 
XML file with a partially-complete society.  Subsequent saves after the 
first, however, are traditional in that the society is saved to the same 
file to which it was previously saved.  A "Save As" of the HNA Map can be 
forced at any time by selecting the File -> Save HNA Map As item in the menu 
bar.


3.  Logging

CSMARTer has an automatic logging facility that logs to the file 
CSMARTer\CSMARTer.log.  Currently, logging is restricted to: 
	a. notice of a rule application, and
	b. the number of society entities that were modified by the rule. 
If a need arises for logging of other events and/or errors, contact the 
CSMARTer developer or enter a bug.







