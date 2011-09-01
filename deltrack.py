#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# This prgram is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: Felix Hummel <deltrack@felixhummel.de>
# Thanks to Camille Gallet <camillegallet@yahoo.fr> for the infoamarok script,
# from which this script borrowed a lot.
import dbus
import sys
import subprocess
import urllib2
import os
from pprint import pprint

exts = [".tqd"] # Other extensions to delete with same base name.

try:
    bus = dbus.SessionBus()
except:
    print "Could not connect to dbus."
    sys.exit(1)
try:
    player = dbus.Interface(bus.get_object('org.mpris.amarok', '/Player'),
              dbus_interface='org.freedesktop.MediaPlayer')
    tracklist = dbus.Interface(bus.get_object('org.mpris.amarok', '/TrackList'),
              dbus_interface='org.freedesktop.MediaPlayer')
except:
    print "Could not connect to Amarok."
    sys.exit(1)

index = tracklist.GetCurrentTrack()  # to remove track from playlist
md = player.GetMetadata()
location = md['location']  # track's url (to send track to trash)

baselist = os.path.splitext(location)
basename = baselist[0]
basext = baselist[1]
exts.append(basext)

is_last_track = tracklist.GetLength() == 1
if not is_last_track:
    player.Next()
    # handle dynamic playlists. Thanks go to Oleg K (ICQ: 367607160)
    new_index = tracklist.GetCurrentTrack()
    if new_index == index:
        tracklist.DelTrack(index-1)
    else:
        tracklist.DelTrack(index)
else:
    player.Stop()
    tracklist.DelTrack(0)

for ext in exts: #Delete each basename+extension.
    loc = ''.join([basename,ext])
    cmdext = ['kioclient', 'move', loc, 'trash:/']
    print "Running %s"%' '.join(cmdext)
    retcodext = subprocess.call(cmdext)
    path = urllib2.urlparse.urlparse(loc).path
    if retcodext == 0:    
        print 'Successfully trashed "%s"'%path
    else:
        print 'Could not trash"%s"'%path

sys.exit(0)
