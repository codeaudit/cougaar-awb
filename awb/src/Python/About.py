# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: About.py,v 1.5 2004-12-06 22:22:46 damoore Exp $
#  <copyright>
#  Copyright 2002 BBN Technologies, LLC
#  under sponsorship of the Defense Advanced Research Projects Agency (DARPA).
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the Cougaar Open Source License as published by
#  DARPA on the Cougaar Open Source Website (www.cougaar.org).
#
#  THE COUGAAR SOFTWARE AND ANY DERIVATIVE SUPPLIED BY LICENSOR IS
#  PROVIDED 'AS IS' WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS OR
#  IMPLIED, INCLUDING (BUT NOT LIMITED TO) ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND WITHOUT
#  ANY WARRANTIES AS TO NON-INFRINGEMENT.  IN NO EVENT SHALL COPYRIGHT
#  HOLDER BE LIABLE FOR ANY DIRECT, SPECIAL, INDIRECT OR CONSEQUENTIAL
#  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE OF DATA OR PROFITS,
#  TORTIOUS CONDUCT, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
#  PERFORMANCE OF THE COUGAAR SOFTWARE.
# </copyright>

import sys
import wx
import wx.html as html
import wxPython.lib.wxpTag

#---------------------------------------------------------------------------

class MyAboutBox(wx.Dialog):
    text = '''
<html>
<body bgcolor="#AC76DE">
<center><table bgcolor="#458154" width="100%%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center">
    <h1>CSMARTer 2003</h1>
    Version %s<br>
    </td>
</tr>
</table>

<p>AWB provides a graphical environment for building
and manipulating Cougaar societies.</p>

<p>AWB is brought to you by BBN Technolgies.</p>

<p>
<font size="-1">Please see <i>license.txt</i> for licensing information.</font>
</p>

<p><wxp class="wxButton">
    <param name="label" value="OK">
    <param name="id"    value="wxID_OK">
</wxp></p>
</center>
</body>
</html>
'''
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About CSMARTer',)
        html = html.HtmlWindow(self, -1, size=(420, -1))
        py_version = sys.version.split()[0]
        html.SetPage(self.text % ('1.2'))  # Version number
        btn = html.FindWindowById(wx.ID_OK)
        btn.SetDefault()
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+5, ir.GetHeight()+5) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)

#---------------------------------------------------------------------------






