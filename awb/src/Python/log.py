import sys
debugToggle = 1

def newLog(fileName):
    pass
def log(*values):
    if debugToggle == 0: return
    print >> sys.stderr, "LOG>", 
    for v in values: print >> sys.stderr,  v,
    print >> sys.stderr, '.'

useage = """    
log('==>', data)
"""