
REM ----------------------------------------------------------------------------
REM Name:
REM Purpose:
REM
REM Author:       ISAT (D. Moore)
REM
REM RCS-ID:       $Id: AWB.bat,v 1.2 2004-12-06 22:22:46 damoore Exp $
REM  <copyright>
REM  Copyright 2002 BBN Technologies, LLC
REM  under sponsorship of the Defense Advanced Research Projects Agency (DARPA).
REM
REM  This program is free software; you can redistribute it and/or modify
REM  it under the terms of the Cougaar Open Source License as published by
REM  DARPA on the Cougaar Open Source Website (www.cougaar.org).
REM
REM  THE COUGAAR SOFTWARE AND ANY DERIVATIVE SUPPLIED BY LICENSOR IS
REM  PROVIDED 'AS IS' WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS OR
REM  IMPLIED, INCLUDING (BUT NOT LIMITED TO) ALL IMPLIED WARRANTIES OF
REM  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND WITHOUT
REM  ANY WARRANTIES AS TO NON-INFRINGEMENT.  IN NO EVENT SHALL COPYRIGHT
REM  HOLDER BE LIABLE FOR ANY DIRECT, SPECIAL, INDIRECT OR CONSEQUENTIAL
REM  DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE OF DATA OR PROFITS,
REM  TORTIOUS CONDUCT, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
REM  PERFORMANCE OF THE COUGAAR SOFTWARE.
REM </copyright>
REM 


@echo off
REM AWB.bat

REM Set the initial tabbed pane to be displayed
REM 0 is the Overview pane
REM 1 is the Rule Editor
REM 2 is the Society Editor
REM 3 is the Agent Laydown
set INITIAL_PANE="3"

python AWB.py %INITIAL_PANE%
