#zoomView:
#given a societymodel, draws it at the chosen level of zoom granularity
import sys
import re

import wx

DEFAULT_ZOOMLEVEL = 1

viewLevelData = [
{"BOXWIDTH":   10,"BOXHEIGHT":  20, "FONTSIZE":8, "PIXELLEVEL":2},
{"BOXWIDTH":   20,"BOXHEIGHT": 25, "FONTSIZE":12, "PIXELLEVEL":3},
{"BOXWIDTH":   90,"BOXHEIGHT": 35, "FONTSIZE":16, "PIXELLEVEL":4},
{"BOXWIDTH": 140,"BOXHEIGHT": 40, "FONTSIZE":20, "PIXELLEVEL":5},
]

ZEROLEVEL = 0
MAXWIDTH = 8000
MAXHEIGHT= 1000
BOXWIDTH = 50
BOXHEIGHT = 30
WIDTHSPACING = 20
HEIGHTSPACING = 150

CURRENTLEVEL = DEFAULT_ZOOMLEVEL

def setLevel(level=1): 
        global CURRENTLEVEL
        if level < 0: level = 0
        if level > 3: level = 3
        CURRENTLEVEL = level
        
def getLevel(): return CURRENTLEVEL
