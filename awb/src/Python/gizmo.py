# Name:
# Purpose:
#
# Author:       D. Moore
#
# RCS-ID:       $Id: gizmo.py,v 1.3 2004-12-06 22:22:46 damoore Exp $
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

import threading, os
##os.putenv('LANG', 'C') # for running on GTK2
#from wxPython.wx import *
import wx
# ------------------------------------------------------------------------------

wxEVT_UPDATE_GIZMO = wx.NewEventType()
EVT_UPDATE_GIZMO = wx.PyEventBinder (wxEVT_UPDATE_GIZMO,1)

class UpdateGizmoEvent(wx.PyEvent):
    def __init__(self):
        wx.PyEvent.__init__(self)
        self.SetEventType(wxEVT_UPDATE_GIZMO)

# ------------------------------------------------------------------------------

class Gizmo(wx.Panel):
    """
    The first argument is either the name of a file that will be split into frames
    (a composite image) or a list of  strings of image names that will be treated
    as individual frames.  If a single (composite) image is given, then additional
    information must be provided: the number of frames in the image and the width
    of each frame.  The first frame is treated as the "at rest" frame (it is not
    shown during animation, but only when GIZMO.Rest() is called.
    A second, single image may be optionally specified to overlay on top of the
    animation. A label may also be specified to show on top of the animation.
    """
    def __init__(self, parent, id,
                 bitmap,          # single (composite) bitmap or list of bitmaps
                 pos = (554,316),	  #wx.DefaultPosition,
                 size = wx.DefaultSize,
                 frameDelay = 0.1,# time between frames
                 frames = 0,      # number of frames (only necessary for composite image)
                 frameWidth = 0,  # width of each frame (only necessary for composite image)
                 label = None,    # optional text to be displayed
                 overlay = None,  # optional image to overlay on animation
                 reverse = 0,     # reverse direction at end of animation
                 style = 0,       # window style
                 name = "gizmo"):
        wx.Panel.__init__(self, parent, id, pos, size, style, name)
        self.name = name
        self.label = label
        _seqTypes = (type([]), type(()))

        # set size, guessing if necessary
        width, height = size
        if width == -1:
            if type(bitmap) in _seqTypes:
                width = bitmap[0].GetWidth()
            else:
                if frameWidth:
                    width = frameWidth
        if height == -1:
            if type(bitmap) in _seqTypes:
                height = bitmap[0].GetHeight()
            else:
                height = bitmap.GetHeight()
        self.width, self.height = width, height

        # double check it
        assert width != -1 and height != -1, "Unable to guess size"

        if label:
            extentX, extentY = self.GetTextExtent(label)
            self.labelX = (width - extentX)/2
            self.labelY = (height - extentY)/2
        self.frameDelay = frameDelay
        self.current = 0
        self.direction = 1
        self.autoReverse = reverse
        self.overlay = overlay
        if overlay is not None:
            self.overlay = overlay
            self.overlayX = (width - self.overlay.GetWidth()) / 2
            self.overlayY = (height - self.overlay.GetHeight()) / 2
        self.showOverlay = overlay is not None
        self.showLabel = label is not None

        # do we have a sequence of images?
        if type(bitmap) in _seqTypes:
            self.submaps = bitmap
            self.frames = len(self.submaps)
        # or a composite image that needs to be split?
        else:
	    self.frames = frames
            self.submaps = []
            for chunk in range(frames):
                rect = (chunk * frameWidth, 0, width, height)
                self.submaps.append(bitmap.GetSubBitmap(rect))

        # self.sequence can be changed, but it's not recommended doing it
        # while the gizmo is running.  self.sequence[0] should always
        # refer to whatever frame is to be shown when 'resting' and be sure
        # that no item in self.sequence >= self.frames or < 0!!!
        self.sequence = range(self.frames)

        self.SetClientSize((width, height))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(EVT_UPDATE_GIZMO, self.Rotate)
        wx.EVT_WINDOW_DESTROY(self, self.OnDestroyWindow)

        self.event = threading.Event()
        self.event.set() # we start out in the "resting" state


    def __del__(self):
        # make sure it's stopped, since EVT_WINDOW_DESTROY may not be sent
        # on all platforms
        self.Stop()


    def OnDestroyWindow(self, event):
        # this is currently broken due to a bug in wxWindows... hopefully
        # it'll be fixed soon.  Meanwhile be sure to explicitly call Stop()
        # before the gizmo is destroyed.
        self.Stop()
        event.Skip()


    def Draw(self, dc):
        dc.DrawBitmap(self.submaps[self.sequence[self.current]], 0, 0, True)
        if self.overlay and self.showOverlay:
            dc.DrawBitmap(self.overlay, self.overlayX, self.overlayY, True)
        if self.label and self.showLabel:
            dc.DrawText(self.label, self.labelX, self.labelY)
            dc.SetTextForeground(wx.WHITE)
            dc.DrawText(self.label, self.labelX-1, self.labelY-1)


    def OnPaint(self, event):
        self.Draw(wx.PaintDC(self))
        event.Skip()


    def UpdateThread(self):
        try:
            while hasattr(self, 'event') and not self.event.isSet():
                wx.PostEvent(self, UpdateGizmoEvent())
                self.event.wait(self.frameDelay)
        except wx.PyDeadObjectError: # BUG: we were destroyed
            print "Got wx.PyDeadObjectError"  # prg debug
            self.Rest()
            #~ return
        except Exception, args:
          import traceback
          traceback.print_exc()
          self.Rest()


    def Rotate(self, event):
        if self.event.isSet():
            return
        self.current += self.direction
        if self.current >= len(self.sequence):
            if self.autoReverse:
                self.Reverse()
                self.current = len(self.sequence) - 1
            else:
                self.current = 1
        if self.current < 1:
            if self.autoReverse:
                self.Reverse()
                self.current = 1
            else:
                self.current = len(self.sequence) - 1
        self.Draw(wx.ClientDC(self))


    # --------- public methods ---------
    def SetFont(self, font):
        """Set the font for the label"""
        wx.Panel.SetFont(self, font)
        self.SetLabel(self.label)
        self.Draw(wx.ClientDC(self))


    def Rest(self):
        """Stop the animation and return to frame 0"""
        self.Stop()
        self.current = 0
        self.Draw(wx.ClientDC(self))


    def Reverse(self):
        """Change the direction of the animation"""
        self.direction = -self.direction


    def Running(self):
        """Returns True if the animation is running"""
        return not self.event.isSet()


    def Start(self):
        """Start the animation"""
        if not self.Running():
            self.event.clear()
            thread = threading.Thread(target = self.UpdateThread,
                                      name = "%s-thread" % self.name)
            thread.start()


    def Stop(self):
        """Stop the animation"""
        if self.event.isSet():
            return
        self.event.set()


    def SetFrameDelay(self, frameDelay = 0.05):
        """Delay between each frame"""
        self.frameDelay = frameDelay


    def ToggleOverlay(self, state = None):
        """Toggle the overlay image"""
        if state is None:
            self.showOverlay = not self.showOverlay
        else:
            self.showOverlay = state
        self.Draw(wx.ClientDC(self))


    def ToggleLabel(self, state = None):
        """Toggle the label"""
        if state is None:
            self.showLabel = not self.showLabel
        else:
            self.showLabel = state
        self.Draw(wx.ClientDC(self))


    def SetLabel(self, label):
        """Change the text of the label"""
        self.label = label
        if label:
            extentX, extentY = self.GetTextExtent(label)
            self.labelX = (self.width - extentX)/2
            self.labelY = (self.height - extentY)/2
        self.Draw(wx.ClientDC(self))



# ------------------------------------------------------------------------------

