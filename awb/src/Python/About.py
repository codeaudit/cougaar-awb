import sys

from   wxPython.wx       import *
from   wxPython.html     import *
import wxPython.lib.wxpTag

#---------------------------------------------------------------------------

class MyAboutBox(wxDialog):
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

<p>CSMARTer provides a graphical environment for building
and manipulating Cougaar societies.</p>

<p>CSMARTer is brought to you by Dana Moore and
Paul Gardella of BBN Technolgies.</p>

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
        wxDialog.__init__(self, parent, -1, 'About CSMARTer',)
        html = wxHtmlWindow(self, -1, size=(420, -1))
        py_version = sys.version.split()[0]
        html.SetPage(self.text % ('1.2'))  # Version number
        btn = html.FindWindowById(wxID_OK)
        btn.SetDefault()
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+5, ir.GetHeight()+5) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wxBOTH)

#---------------------------------------------------------------------------






