import types
class zork:
  def __init__(self, arg):
    self.whatever = arg
    self.string = None
    if isinstance(arg, types.StringType):
      self.string = arg

  def aMethod(self, x):
    a = 'duuuuuh'
    print a
    return "Hello"+ str(x)
  def printWhatever(self):
    print "Whatever is == ", self.whatever

a = 'foo'
b = 'bar'
c = a + b
print "A is "+a+" B is "+b+" C is "+ c
z = zork(12)
zz = zork("string thing")
zzz = zork(43.132123)


print z.aMethod(" World.")

z.printWhatever()
zz.printWhatever()
zzz.printWhatever()

print z.string
print zz.string
print zzz.string