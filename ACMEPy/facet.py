#facet.py
#
# Name:         
# Purpose:      
#
# Author:       ISAT (D. Moore/M. Barger/P. Gardella)
#
# RCS-ID:       $Id: facet.py,v 1.6 2003-07-28 12:24:58 pgardella Exp $
#
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
from __future__ import generators
import types

class Facet:
  def __init__(self, aFacet, rule='BASE'):
    # Note that we can construct a Facet by passing in either a Dictionary or a String,
    # but we store them all in a dictionary
    if type(aFacet) == types.DictionaryType:
      self.facets = aFacet
    elif type(aFacet) == types.StringType:
      self.facets = self.to_dictionary(aFacet)
    else:
      print "ERROR: Facet input type is", type(aFacet)  
    self.rule = rule
    self.parent = None
    
  def __str__(self):
    retval = ""
    for fp in self.each_facet_pair():
      retval += fp + "\n"
    return retval

  def set_rule(self, newRule):
        self.rule = str(newRule)

  def set_attribute(self, attribute, value):
    # both args must be strings
    if attribute.lower() == 'value':
      dic = self.to_dictionary(value)
      self.facets.update(dic)
    elif attribute.lower() == 'rule':
      self.rule = value
    else:
      raise Exception, "Attempting to set unknown Facet attribute: " + attribute.lower()

  # #
  # Adds a key/value pair to the Dictionary 'facets'
  #
  # key:: [Object] to be used as the key
  # value:: [Object] to be used as the value
  #
  def add_facet_element(self, key, value):
    self.facets[key] = value
  
  ##
  # Iteratively returns each key/value pair in this Facet instance as a 
  # String in "key=value" format.
  #
  def each_facet_pair(self):
    for key in self.facets.keys():
      yield (key + "=" + self.facets[key])
  
  def has_key(self, key):
    return self.facets.has_key(key)
  
  def get(self, key):
    return self.facets[key]
  
  ##
  # If the 'key' argument is not provided, this entire Facet 
  # obj deletes itself from its parent.  If a key is provided,
  # this method removes a single key=value entry from the 
  # dictionary contained in this Facet.  If removal of this 
  # entry leaves the dictionary empty, then this method
  # calls itself without a 'key' argument, thus causing this
  # Facet to be deleted from its parent.
  #
  # keyValueString:: [String] in "key=value" format
  #
  def delete_entity(self, key=None):
    if key is None:
      self.parent.delete_facet(self)  # deletes entire dictionary from parent instance
    else:
      del self.facets[key]  # just deletes a single key/value pair
      if len(self.facets) == 0:   # if the last (or only) key/value pair was just deleted
        del self.facets
        self.delete_entity()  # delete self from parent
  
  ##
  # Returns True if the dictionary contained in this Facet obj contains
  # the specified entry; else, returns False
  #
  # keyValueString:: [String] in "key=value" format
  #
  def contains_entry(self, keyValueString):
    key, value = self.split_entry(keyValueString)
    return self.has_key(key)
  
  ##
  # Removes a single key=value entry from the dictionary
  # contained in this Facet.  If removal of this entry
  # leaves the dictionary empty, then this method
  # causing this Facet to be deleted from its parent.
  # Provides identical functionality as delete_entity(key),
  # but allows for a key-value string argument.
  #
  # keyValueString:: [String] the entry to be removed, in "key=value" format
  #
  def remove_entry(self, keyValueString):
    key, value = self.split_entry(keyValueString)
    self.delete_entity(key)
  
  ##
  # Adds a single key=value entry to the dictionary contained
  # in this Facet.
  #
  # keyValueString:: [String] the entry to be added, in "key=value" format
  #
  def add_entry(self, keyValueString):
    entry = self.to_dictionary(keyValueString)  # chg string into dictionary
    self.facets.update(entry)  # add new entry into self.facets
  
  ##
  # Replaces one entry in the dictionary contained in this Facet
  # with another.
  #
  # oldEntry:: [String] the existing entry to be replaced, in "key=value" format
  # newEntry:: [String] the new entry to be added, in "key=value" format
  #
  def replace_entry(self, oldEntry, newEntry):
    key, value = self.split_entry(oldEntry)  # extract key from oldEntry
    del self.facets[key]  # delete the old entry
    self.add_entry(newEntry)
  
  ##
  # Returns a two-tuple containing the (key, value) from the input string
  #
  # keyValueString:: [String] in "key=value" format
  #
  def split_entry(self, keyValueString):
    entryList = keyValueString.split('=')
    return entryList[0], entryList[1]
  
  def clone(self):
    newDict = {}
    for key in self.facets.keys():
      newDict[key] = self.facets[key]
    return Facet(newDict)
  
  ##
  # Returns a Dictionary obj containing a single key/value pair
  #
  # aString:: [String] in "key=value" format
  #
  def to_dictionary(self, aString):
    dicList = aString.split("=")
    #strip off single quotes, if any
    if dicList[1].startswith("'"):
      dicList[1] = dicList[1][1:]
    if dicList[1].endswith("'"):
      dicList[1] = dicList[1][:-1]
    return {dicList[0]: dicList[1]}
  
  def to_xml(self, numIndents=0):
    xml = ""
    indent = numIndents * 2 * ' '
    if len(self.facets) > 0:
      #~ xml = "    <facet"
      xml = indent + "<facet"
      for key in self.facets.keys():
        xml = xml + " " + key + "='" + self.facets[key] + "'"
      xml = xml + "/>\n"
    return xml
  
  def to_python(self):
    script = ""
    if len(self.facets) > 0:
      script = "facetDict = {}\n"
      for key in self.facets.keys():
        script = script + "facetDict[" + key + "] = " + self.facets[key] + "\n"
      script = "facet = Facet(facetDict)\n"
      script = script + self.parent.name + ".add_facet(facet)\n"
    return script
  
  def to_ruby(self, numTabs):
    script = ""
    indent = "  " * numTabs
    for key in self.facets.keys():
      script = script + indent + "facet[:" + key + "]='" + self.facets[key] + "'\n"
    return script

def unitTest():
  facetDict = {}
  facetDict["a"] = "b"
  facetDict["c"] = "d"
  f = Facet(facetDict)  
  print f
  
if __name__ == '__main__':
  unitTest()
\