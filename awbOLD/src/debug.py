import sys

def DBG(name, value=None): 
    if not value: print >> sys.stderr,"DBG:", name
    else:print >> sys.stderr,"DBG:", name, value

#~ if __name__ == '__main__':
    #~ import sys,os
    #~ DBG("spam", value="hello world!")
    #~ DBG("green eggs",value=42)
    #~ DBG("terminator",value=101.1)
    #~ DBG("no value")