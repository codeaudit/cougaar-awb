# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: encode_bitmaps.py,v 1.2 2004-12-06 22:22:46 damoore Exp $
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
#





#!/usr/bin/env python
#----------------------------------------------------------------------

"""
This is a way to save the startup time when running img2py on lots of
files...
"""

import sys
from wxPython.tools import img2py


command_lines = [
    "   -u -i -n Mondrian bmp_source/mondrian.ico  images.py",
    "-a -u -n Society     bmp_source/society.bmp   images.py",
    "-a -u -n Host        bmp_source/host.bmp      images.py",
    "-a -u -n Node        bmp_source/node.bmp      images.py",
    "-a -u -n Agent       bmp_source/agent.bmp     images.py",
    "-a -u -n Component   bmp_source/component.bmp images.py",
    "-a -u -n Argument    bmp_source/argument.bmp  images.py",
    "-a -u -n Question    bmp_source/querymark.bmp images.py",
    
    "-a -u -n Background  bmp_source/backgrnd.png  images.py",

    "-a -u -n Test2       bmp_source/test2.bmp     images.py",
    "-a -u -n Smiles -m #FFFFFF bmp_source/smiles2.bmp images.py",

    "-a -u -n GridBG      bmp_source/GridBG.gif    images.py",


    "-a -u -n NoIcon  bmp_source/noicon.png  images.py",

    "-a -u -n WizTest1 bmp_source/wiztest1.bmp images.py",
    "-a -u -n WizTest2 bmp_source/wiztest2.bmp images.py",

    "   -u -c bmp_source/001.png gizmoImages.py",
    "-a -u -c bmp_source/002.png gizmoImages.py",
    "-a -u -c bmp_source/003.png gizmoImages.py",
    "-a -u -c bmp_source/004.png gizmoImages.py",
    "-a -u -c bmp_source/005.png gizmoImages.py",
    "-a -u -c bmp_source/006.png gizmoImages.py",
    "-a -u -c bmp_source/007.png gizmoImages.py",
    "-a -u -c bmp_source/008.png gizmoImages.py",
    "-a -u -c bmp_source/009.png gizmoImages.py",
    "-a -u -c bmp_source/010.png gizmoImages.py",
    "-a -u -c bmp_source/011.png gizmoImages.py",
    "-a -u -c bmp_source/012.png gizmoImages.py",
    "-a -u -c bmp_source/013.png gizmoImages.py",
    "-a -u -c bmp_source/014.png gizmoImages.py",
    "-a -u -c bmp_source/015.png gizmoImages.py",
    "-a -u -c bmp_source/016.png gizmoImages.py",
    "-a -u -c bmp_source/017.png gizmoImages.py",
    "-a -u -c bmp_source/018.png gizmoImages.py",
    "-a -u -c bmp_source/019.png gizmoImages.py",
    "-a -u -c bmp_source/020.png gizmoImages.py",
    "-a -u -c bmp_source/021.png gizmoImages.py",
    "-a -u -c bmp_source/022.png gizmoImages.py",
    "-a -u -c bmp_source/023.png gizmoImages.py",
    "-a -u -c bmp_source/024.png gizmoImages.py",
    "-a -u -c bmp_source/025.png gizmoImages.py",
    "-a -u -c bmp_source/026.png gizmoImages.py",
    "-a -u -c bmp_source/027.png gizmoImages.py",
    "-a -u -c bmp_source/028.png gizmoImages.py",
    "-a -u -c bmp_source/029.png gizmoImages.py",
    "-a -u -c bmp_source/030.png gizmoImages.py",
    "-a -u -c bmp_source/rest.png    gizmoImages.py",
    ]


for line in command_lines:
    args = line.split()
    img2py.main(args)

