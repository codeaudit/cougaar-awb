#!/bin/env python
#----------------------------------------------------------------------------
# Name:         
# Purpose:      
#
# Author:       ISAT (D. Moore)
#
# RCS-ID:       $Id: eventFactory.py,v 1.1 2004-08-06 18:58:08 damoore Exp $
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

from wxPython.wx import *
from wxPython import  events

#import threading 
import sys, thread, traceback
#~ import Queue
import random as r
import time

from csmarter_events import *


#----------------------------------------------------------------------

class EventFactory:
    def __init__(self, parent, log):
        self._parent = parent
        self.keepRunning = 1
        self.log = log
        self._Agent_Names = [
"OSD.GOV",
"HNS.MIL",
"TRANSCOM-20.TRANSCOM.MIL",
"DLAHQ.MIL",
"FORSCOM.MIL",
"OSC.MIL",
"NATO.GOV",
"USEUCOM.MIL",
"AmmoTRANSCOM.TRANSCOM.MIL",
"EuroTRANSCOM.TRANSCOM.MIL",
"ConusTRANSCOM.TRANSCOM.MIL",
"JSRCMDSE.NATO.GOV",
"USAEUR.MIL",
"AmmoSea.TRANSCOM.MIL",
"EuroSea.TRANSCOM.MIL",
"EuroAir.TRANSCOM.MIL",
"ConusAir.TRANSCOM.MIL",
"ConusSea.TRANSCOM.MIL",
"21-TSC-HQ.ARMY.MIL",
"5-CORPS.ARMY.MIL",
"AmmoTheaterGround.TRANSCOM.MIL",
"AmmoConusGround.TRANSCOM.MIL",
"AmmoShipPacker.TRANSCOM.MIL",
"EuroGround.TRANSCOM.MIL",
"EuroShipPacker.TRANSCOM.MIL",
"PlanePackerA.TRANSCOM.MIL",
"PlanePackerB.TRANSCOM.MIL",
"ConusGroundA.TRANSCOM.MIL",
"ConusShipPacker.TRANSCOM.MIL",
"TheaterGroundA.TRANSCOM.MIL",
"TheaterGroundB.TRANSCOM.MIL",
"37-TRANSGP.21-TSC.ARMY.MIL",
"RSA.21-TSC.ARMY.MIL",
"200-MMC.21-TSC.ARMY.MIL",
"AWR-2.21-TSC.ARMY.MIL",
"7-TCGP-TPTDD.21-TSC.ARMY.MIL",
"29-SPTGP.21-TSC.ARMY.MIL",
"MCG1.1-UA.ARMY.MIL",
"1-AD.ARMY.MIL",
"CORPS-ARTY.5-CORPS.ARMY.MIL",
"3-SUPCOM-HQ.5-CORPS.ARMY.MIL",
"CORPS-REAR.5-CORPS.ARMY.MIL",
"28-TCBN.37-TRANSGP.21-TSC.ARMY.MIL",
"6-TCBN.37-TRANSGP.21-TSC.ARMY.MIL",
"191-ORDBN.29-SPTGP.21-TSC.ARMY.MIL",
"51-MAINTBN.29-SPTGP.21-TSC.ARMY.MIL",
"MED-SPT.1-UA.ARMY.MIL",
"MCG.1-CABN.1-UA.ARMY.MIL",
"BTY-HQ.NLOS-BN.1-UA.ARMY.MIL",
"CO-HQ.BIC.1-UA.ARMY.MIL",
"FCS-ICV-0.MCG1.1-UA.ARMY.MIL",
"TACP.1-UA.ARMY.MIL",
"MCG.2-CABN.1-UA.ARMY.MIL",
"UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"MCG2.1-UA.ARMY.MIL",
"CO-HQ.FSB.1-UA.ARMY.MIL",
"DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"MCG.3-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG1.1-UA.ARMY.MIL",
"AVNBDE.1-AD.ARMY.MIL",
"3-BDE.1-AD.ARMY.MIL",
"1-BDE.1-AD.ARMY.MIL",
"DIVARTY.1-AD.ARMY.MIL",
"DISCOM.1-AD.ARMY.MIL",
"2-BDE.1-AD.ARMY.MIL",
"DIV-REAR.1-AD.ARMY.MIL",
"41-FABDE.5-CORPS.ARMY.MIL",
"19-MMC.5-CORPS.ARMY.MIL",
"16-CSG.5-CORPS.ARMY.MIL",
"27-TCBN-MVTCTRL.5-CORPS.ARMY.MIL",
"208-SCCO.5-CORPS.ARMY.MIL",
"7-CSG.5-CORPS.ARMY.MIL",
"30-MEDBDE.5-CORPS.ARMY.MIL",
"11-AVN-RGT.5-CORPS.ARMY.MIL",
"205-MIBDE.5-CORPS.ARMY.MIL",
"130-ENGBDE.5-CORPS.ARMY.MIL",
"69-ADABDE.5-CORPS.ARMY.MIL",
"18-MPBDE.5-CORPS.ARMY.MIL",
"12-AVNBDE.5-CORPS.ARMY.MIL",
"22-SIGBDE.5-CORPS.ARMY.MIL",
"109-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"68-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"66-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"416-POL-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"632-MAINTCO.37-TRANSGP.21-TSC.ARMY.MIL",
"110-POL-SUPPLYCO.37-TRANSGP.21-TSC.ARMY.MIL",
"24-ORDCO.29-SPTGP.21-TSC.ARMY.MIL",
"720-EODDET.29-SPTGP.21-TSC.ARMY.MIL",
"23-ORDCO.29-SPTGP.21-TSC.ARMY.MIL",
"702-EODDET.29-SPTGP.21-TSC.ARMY.MIL",
"18-PERISH-SUBPLT.29-SPTGP.21-TSC.ARMY.MIL",
"343-SUPPLYCO.29-SPTGP.21-TSC.ARMY.MIL",
"512-MAINTCO.29-SPTGP.21-TSC.ARMY.MIL",
"5-MAINTCO.29-SPTGP.21-TSC.ARMY.MIL",
"574-SSCO.29-SPTGP.21-TSC.ARMY.MIL",
"FCS-MV-0.MED-SPT.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.MED-SPT.1-UA.ARMY.MIL",
"MED-PLT-HQ.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.1-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.1-CABN.1-UA.ARMY.MIL",
"CO-HQ-SECTION.1-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.1-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.1-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.1-CABN.1-UA.ARMY.MIL",
"TACP.1-CABN.1-UA.ARMY.MIL",
"BTY-C-HQ.NLOS-BN.1-UA.ARMY.MIL",
"BTY-B-HQ.NLOS-BN.1-UA.ARMY.MIL",
"BTY-A-HQ.NLOS-BN.1-UA.ARMY.MIL",
"SENSOR-PLT-HQ.NLOS-BN.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.BTY-HQ.NLOS-BN.1-UA.ARMY.MIL",
"CIC-CMD-GRP.NLOS-BN.1-UA.ARMY.MIL",
"NLOS-LS-PLT.NLOS-BN.1-UA.ARMY.MIL",
"RANGE-EXT-HQ-SQUAD.BIC.1-UA.ARMY.MIL",
"NETOPS-HQ-SQUAD.BIC.1-UA.ARMY.MIL",
"ISR-INTEG-TEAM.BIC.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.CO-HQ.BIC.1-UA.ARMY.MIL",
"FCS-C2V-0.CO-HQ.BIC.1-UA.ARMY.MIL",
"SIT-AWARE-TEAM.BIC.1-UA.ARMY.MIL",
"FCS-C2V-3.TACP.1-UA.ARMY.MIL",
"FCS-C2V-1.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-3.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-6.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-1.TACP.1-UA.ARMY.MIL",
"FCS-ICV-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-4.TACP.1-UA.ARMY.MIL",
"FCS-C2V-5.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-2.TACP.1-UA.ARMY.MIL",
"FCS-C2V-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-2.TACP.1-UA.ARMY.MIL",
"CO-HQ-SECTION.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.2-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.2-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.2-CABN.1-UA.ARMY.MIL",
"MED-PLT-HQ.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.2-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.2-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.2-CABN.1-UA.ARMY.MIL",
"TACP.2-CABN.1-UA.ARMY.MIL",
"FTTS-U-C2-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-MS-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-MS-1.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FCS-ICV-0.MCG2.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG2.1-UA.ARMY.MIL",
"FTTS-U-C2-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"MED-CO-HQ.FSB.1-UA.ARMY.MIL",
"STAFF-CELL.FSB.1-UA.ARMY.MIL",
"DISTRO-MGT-CELL.FSB.1-UA.ARMY.MIL",
"CIC.FSB.1-UA.ARMY.MIL",
"SUSTAIN-CO-HQ.FSB.1-UA.ARMY.MIL",
"FTTS-MS-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"FCS-C2V-1.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"FTTS-U-C2-0.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"FCS-C2V-0.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"SVC-TRP-HQ.AVN-DET.1-UA.ARMY.MIL",
"FLT-TRP-B-HQ.AVN-DET.1-UA.ARMY.MIL",
"FLT-TRP-A-HQ.AVN-DET.1-UA.ARMY.MIL",
"TACP.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.3-CABN.1-UA.ARMY.MIL",
"MED-PLT-HQ.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.3-CABN.1-UA.ARMY.MIL",
"CO-HQ-SECTION.3-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.3-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.3-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.3-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.3-CABN.1-UA.ARMY.MIL",
"127-DASB.DISCOM.1-AD.ARMY.MIL",
"1-501-AVNBN.AVNBDE.1-AD.ARMY.MIL",
"2-501-AVNBN.AVNBDE.1-AD.ARMY.MIL",
"1-1-CAVSQDN.AVNBDE.1-AD.ARMY.MIL",
"1-41-INFBN.3-BDE.1-AD.ARMY.MIL",
"70-ENGBN.3-BDE.1-AD.ARMY.MIL",
"4-1-FABN.3-BDE.1-AD.ARMY.MIL",
"2-70-ARBN.3-BDE.1-AD.ARMY.MIL",
"1-13-ARBN.3-BDE.1-AD.ARMY.MIL",
"125-FSB.DISCOM.1-AD.ARMY.MIL",
"1-36-INFBN.1-BDE.1-AD.ARMY.MIL",
"2-37-ARBN.1-BDE.1-AD.ARMY.MIL",
"501-FSB.DISCOM.1-AD.ARMY.MIL",
"16-ENGBN.1-BDE.1-AD.ARMY.MIL",
"2-3-FABN.1-BDE.1-AD.ARMY.MIL",
"1-37-ARBN.1-BDE.1-AD.ARMY.MIL",
"25-FABTRY-TGTACQ.DIVARTY.1-AD.ARMY.MIL",
"1-94-FABN.DIVARTY.1-AD.ARMY.MIL",
"123-MSB-HQ.DISCOM.1-AD.ARMY.MIL",
"1-6-INFBN.2-BDE.1-AD.ARMY.MIL",
"4-27-FABN.2-BDE.1-AD.ARMY.MIL",
"2-6-INFBN.2-BDE.1-AD.ARMY.MIL",
"1-35-ARBN.2-BDE.1-AD.ARMY.MIL",
"47-FSB.DISCOM.1-AD.ARMY.MIL",
"40-ENGBN.2-BDE.1-AD.ARMY.MIL",
"501-MIBN-CEWI.1-AD.ARMY.MIL",
"501-MPCO.1-AD.ARMY.MIL",
"1-4-ADABN.1-AD.ARMY.MIL",
"141-SIGBN.1-AD.ARMY.MIL",
"69-CHEMCO.1-AD.ARMY.MIL",
"1-27-FABN.5-CORPS.ARMY.MIL",
"2-4-FABN-MLRS.5-CORPS.ARMY.MIL",
"3-13-FABN-155.5-CORPS.ARMY.MIL",
"485-CSB.16-CSG.5-CORPS.ARMY.MIL",
"106-TCBN.16-CSG.5-CORPS.ARMY.MIL",
"18-MAINTBN.16-CSG.5-CORPS.ARMY.MIL",
"71-MAINTBN.7-CSG.5-CORPS.ARMY.MIL",
"181-TCBN.7-CSG.5-CORPS.ARMY.MIL",
"561-SSBN.7-CSG.5-CORPS.ARMY.MIL",
"125-ORDBN.7-CSG.5-CORPS.ARMY.MIL",
"316-POL-SUPPLYBN.7-CSG.5-CORPS.ARMY.MIL",
"244-ENGBN-CBTHVY.5-CORPS.ARMY.MIL",
"52-ENGBN-CBTHVY.5-CORPS.ARMY.MIL",
"286-ADA-SCCO.5-CORPS.ARMY.MIL",
"OSD.GOV",
"HNS.MIL",
"TRANSCOM-20.TRANSCOM.MIL",
"DLAHQ.MIL",
"FORSCOM.MIL",
"OSC.MIL",
"NATO.GOV",
"USEUCOM.MIL",
"AmmoTRANSCOM.TRANSCOM.MIL",
"EuroTRANSCOM.TRANSCOM.MIL",
"ConusTRANSCOM.TRANSCOM.MIL",
"JSRCMDSE.NATO.GOV",
"USAEUR.MIL",
"AmmoSea.TRANSCOM.MIL",
"EuroSea.TRANSCOM.MIL",
"EuroAir.TRANSCOM.MIL",
"ConusAir.TRANSCOM.MIL",
"ConusSea.TRANSCOM.MIL",
"21-TSC-HQ.ARMY.MIL",
"5-CORPS.ARMY.MIL",
"AmmoTheaterGround.TRANSCOM.MIL",
"AmmoConusGround.TRANSCOM.MIL",
"AmmoShipPacker.TRANSCOM.MIL",
"EuroGround.TRANSCOM.MIL",
"EuroShipPacker.TRANSCOM.MIL",
"PlanePackerA.TRANSCOM.MIL",
"PlanePackerB.TRANSCOM.MIL",
"ConusGroundA.TRANSCOM.MIL",
"ConusShipPacker.TRANSCOM.MIL",
"TheaterGroundA.TRANSCOM.MIL",
"TheaterGroundB.TRANSCOM.MIL",
"37-TRANSGP.21-TSC.ARMY.MIL",
"RSA.21-TSC.ARMY.MIL",
"200-MMC.21-TSC.ARMY.MIL",
"AWR-2.21-TSC.ARMY.MIL",
"7-TCGP-TPTDD.21-TSC.ARMY.MIL",
"29-SPTGP.21-TSC.ARMY.MIL",
"MCG1.1-UA.ARMY.MIL",
"1-AD.ARMY.MIL",
"CORPS-ARTY.5-CORPS.ARMY.MIL",
"3-SUPCOM-HQ.5-CORPS.ARMY.MIL",
"CORPS-REAR.5-CORPS.ARMY.MIL",
"28-TCBN.37-TRANSGP.21-TSC.ARMY.MIL",
"6-TCBN.37-TRANSGP.21-TSC.ARMY.MIL",
"191-ORDBN.29-SPTGP.21-TSC.ARMY.MIL",
"51-MAINTBN.29-SPTGP.21-TSC.ARMY.MIL",
"MED-SPT.1-UA.ARMY.MIL",
"MCG.1-CABN.1-UA.ARMY.MIL",
"BTY-HQ.NLOS-BN.1-UA.ARMY.MIL",
"CO-HQ.BIC.1-UA.ARMY.MIL",
"FCS-ICV-0.MCG1.1-UA.ARMY.MIL",
"TACP.1-UA.ARMY.MIL",
"MCG.2-CABN.1-UA.ARMY.MIL",
"UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"MCG2.1-UA.ARMY.MIL",
"CO-HQ.FSB.1-UA.ARMY.MIL",
"DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"MCG.3-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG1.1-UA.ARMY.MIL",
"AVNBDE.1-AD.ARMY.MIL",
"3-BDE.1-AD.ARMY.MIL",
"1-BDE.1-AD.ARMY.MIL",
"DIVARTY.1-AD.ARMY.MIL",
"DISCOM.1-AD.ARMY.MIL",
"2-BDE.1-AD.ARMY.MIL",
"DIV-REAR.1-AD.ARMY.MIL",
"41-FABDE.5-CORPS.ARMY.MIL",
"19-MMC.5-CORPS.ARMY.MIL",
"16-CSG.5-CORPS.ARMY.MIL",
"27-TCBN-MVTCTRL.5-CORPS.ARMY.MIL",
"208-SCCO.5-CORPS.ARMY.MIL",
"7-CSG.5-CORPS.ARMY.MIL",
"30-MEDBDE.5-CORPS.ARMY.MIL",
"11-AVN-RGT.5-CORPS.ARMY.MIL",
"205-MIBDE.5-CORPS.ARMY.MIL",
"130-ENGBDE.5-CORPS.ARMY.MIL",
"69-ADABDE.5-CORPS.ARMY.MIL",
"18-MPBDE.5-CORPS.ARMY.MIL",
"12-AVNBDE.5-CORPS.ARMY.MIL",
"22-SIGBDE.5-CORPS.ARMY.MIL",
"109-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"68-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"66-MDM-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"416-POL-TRKCO.37-TRANSGP.21-TSC.ARMY.MIL",
"632-MAINTCO.37-TRANSGP.21-TSC.ARMY.MIL",
"110-POL-SUPPLYCO.37-TRANSGP.21-TSC.ARMY.MIL",
"24-ORDCO.29-SPTGP.21-TSC.ARMY.MIL",
"720-EODDET.29-SPTGP.21-TSC.ARMY.MIL",
"23-ORDCO.29-SPTGP.21-TSC.ARMY.MIL",
"702-EODDET.29-SPTGP.21-TSC.ARMY.MIL",
"18-PERISH-SUBPLT.29-SPTGP.21-TSC.ARMY.MIL",
"343-SUPPLYCO.29-SPTGP.21-TSC.ARMY.MIL",
"512-MAINTCO.29-SPTGP.21-TSC.ARMY.MIL",
"5-MAINTCO.29-SPTGP.21-TSC.ARMY.MIL",
"574-SSCO.29-SPTGP.21-TSC.ARMY.MIL",
"FCS-MV-0.MED-SPT.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.MED-SPT.1-UA.ARMY.MIL",
"MED-PLT-HQ.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.1-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.1-CABN.1-UA.ARMY.MIL",
"CO-HQ-SECTION.1-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.1-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.1-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.1-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.1-CABN.1-UA.ARMY.MIL",
"TACP.1-CABN.1-UA.ARMY.MIL",
"BTY-C-HQ.NLOS-BN.1-UA.ARMY.MIL",
"BTY-B-HQ.NLOS-BN.1-UA.ARMY.MIL",
"BTY-A-HQ.NLOS-BN.1-UA.ARMY.MIL",
"SENSOR-PLT-HQ.NLOS-BN.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.BTY-HQ.NLOS-BN.1-UA.ARMY.MIL",
"CIC-CMD-GRP.NLOS-BN.1-UA.ARMY.MIL",
"NLOS-LS-PLT.NLOS-BN.1-UA.ARMY.MIL",
"RANGE-EXT-HQ-SQUAD.BIC.1-UA.ARMY.MIL",
"NETOPS-HQ-SQUAD.BIC.1-UA.ARMY.MIL",
"ISR-INTEG-TEAM.BIC.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.CO-HQ.BIC.1-UA.ARMY.MIL",
"FCS-C2V-0.CO-HQ.BIC.1-UA.ARMY.MIL",
"SIT-AWARE-TEAM.BIC.1-UA.ARMY.MIL",
"FCS-C2V-3.TACP.1-UA.ARMY.MIL",
"FCS-C2V-1.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-3.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-6.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-1.TACP.1-UA.ARMY.MIL",
"FCS-ICV-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-4.TACP.1-UA.ARMY.MIL",
"FCS-C2V-5.TACP.1-UA.ARMY.MIL",
"FTTS-U-C2-2.TACP.1-UA.ARMY.MIL",
"FCS-C2V-0.TACP.1-UA.ARMY.MIL",
"FCS-C2V-2.TACP.1-UA.ARMY.MIL",
"CO-HQ-SECTION.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.2-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.2-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.2-CABN.1-UA.ARMY.MIL",
"MED-PLT-HQ.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.2-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.2-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.2-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.2-CABN.1-UA.ARMY.MIL",
"TACP.2-CABN.1-UA.ARMY.MIL",
"FTTS-U-C2-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-MS-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FTTS-MS-1.UA-CO-HQ-SECTION.1-UA.ARMY.MIL",
"FCS-ICV-0.MCG2.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG2.1-UA.ARMY.MIL",
"FTTS-U-C2-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"FTTS-U-SPT-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"MED-CO-HQ.FSB.1-UA.ARMY.MIL",
"STAFF-CELL.FSB.1-UA.ARMY.MIL",
"DISTRO-MGT-CELL.FSB.1-UA.ARMY.MIL",
"CIC.FSB.1-UA.ARMY.MIL",
"SUSTAIN-CO-HQ.FSB.1-UA.ARMY.MIL",
"FTTS-MS-0.CO-HQ.FSB.1-UA.ARMY.MIL",
"FCS-C2V-1.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"FTTS-U-C2-0.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"FCS-C2V-0.DET-HQ.AVN-DET.1-UA.ARMY.MIL",
"SVC-TRP-HQ.AVN-DET.1-UA.ARMY.MIL",
"FLT-TRP-B-HQ.AVN-DET.1-UA.ARMY.MIL",
"FLT-TRP-A-HQ.AVN-DET.1-UA.ARMY.MIL",
"TACP.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-B.3-CABN.1-UA.ARMY.MIL",
"MED-PLT-HQ.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-B.3-CABN.1-UA.ARMY.MIL",
"CO-HQ-SECTION.3-CABN.1-UA.ARMY.MIL",
"BTY-HQ.MORTAR-BTY.3-CABN.1-UA.ARMY.MIL",
"SUPPORT-SECTION.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.MCSCO-A.3-CABN.1-UA.ARMY.MIL",
"CO-HQ.INFCO-A.3-CABN.1-UA.ARMY.MIL",
"FCS-C2V-0.MCG.3-CABN.1-UA.ARMY.MIL",
"DET-HQ.RECON-DET.3-CABN.1-UA.ARMY.MIL",
"127-DASB.DISCOM.1-AD.ARMY.MIL",
"1-501-AVNBN.AVNBDE.1-AD.ARMY.MIL",
"2-501-AVNBN.AVNBDE.1-AD.ARMY.MIL",
"1-1-CAVSQDN.AVNBDE.1-AD.ARMY.MIL",
"1-41-INFBN.3-BDE.1-AD.ARMY.MIL",
"70-ENGBN.3-BDE.1-AD.ARMY.MIL",
"4-1-FABN.3-BDE.1-AD.ARMY.MIL",
"2-70-ARBN.3-BDE.1-AD.ARMY.MIL",
"1-13-ARBN.3-BDE.1-AD.ARMY.MIL",
"125-FSB.DISCOM.1-AD.ARMY.MIL",
"1-36-INFBN.1-BDE.1-AD.ARMY.MIL",
"2-37-ARBN.1-BDE.1-AD.ARMY.MIL",
"501-FSB.DISCOM.1-AD.ARMY.MIL",
"16-ENGBN.1-BDE.1-AD.ARMY.MIL",
"2-3-FABN.1-BDE.1-AD.ARMY.MIL",
"1-37-ARBN.1-BDE.1-AD.ARMY.MIL",
"25-FABTRY-TGTACQ.DIVARTY.1-AD.ARMY.MIL",
"1-94-FABN.DIVARTY.1-AD.ARMY.MIL",
"123-MSB-HQ.DISCOM.1-AD.ARMY.MIL",
"1-6-INFBN.2-BDE.1-AD.ARMY.MIL",
"4-27-FABN.2-BDE.1-AD.ARMY.MIL",
"2-6-INFBN.2-BDE.1-AD.ARMY.MIL",
"1-35-ARBN.2-BDE.1-AD.ARMY.MIL",
"47-FSB.DISCOM.1-AD.ARMY.MIL",
"40-ENGBN.2-BDE.1-AD.ARMY.MIL",
"501-MIBN-CEWI.1-AD.ARMY.MIL",
"501-MPCO.1-AD.ARMY.MIL",
"1-4-ADABN.1-AD.ARMY.MIL",
"141-SIGBN.1-AD.ARMY.MIL",
"69-CHEMCO.1-AD.ARMY.MIL",
"1-27-FABN.5-CORPS.ARMY.MIL",
"2-4-FABN-MLRS.5-CORPS.ARMY.MIL",
"3-13-FABN-155.5-CORPS.ARMY.MIL",
"485-CSB.16-CSG.5-CORPS.ARMY.MIL",
"106-TCBN.16-CSG.5-CORPS.ARMY.MIL",
"18-MAINTBN.16-CSG.5-CORPS.ARMY.MIL",
"71-MAINTBN.7-CSG.5-CORPS.ARMY.MIL",
"181-TCBN.7-CSG.5-CORPS.ARMY.MIL",
"561-SSBN.7-CSG.5-CORPS.ARMY.MIL",
"125-ORDBN.7-CSG.5-CORPS.ARMY.MIL",
"316-POL-SUPPLYBN.7-CSG.5-CORPS.ARMY.MIL",
"244-ENGBN-CBTHVY.5-CORPS.ARMY.MIL",
"52-ENGBN-CBTHVY.5-CORPS.ARMY.MIL",
"286-ADA-SCCO.5-CORPS.ARMY.MIL"
        ]
        self._parent = parent
        r.seed(len(self._Agent_Names))

    def Start(self):
        self.keepGoing = self.running = true
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.keepGoing = false
      #~ self.log.WriteText("Thread done...\n")
      
    def IsRunning(self):
        return self.running
    
    def Run(self):
      self.log.WriteText( "Thread starting...\n")
      iterations = 0
      while self.keepGoing:
        evt = None
        string = self._Agent_Names[r.randint(0, len(self._Agent_Names))]
        time.sleep(1)
        #~ print "EVENTFACTORY is sending", string
        evt = SocietyControllerEvent(string)
        wxPostEvent(self._parent, evt)
        iterations += 1
        if iterations >= 300 : self.keepGoing = false  #  ?
      self.running = false
      
      
if __name__ == '__main__':
     x = EventFactory(None, None)
     x.Start()
     print "done!"
     