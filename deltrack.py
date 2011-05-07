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
from pprint import pprint

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

index = tracklist.GetCurrentTrack() # to remove track from playlist
md = player.GetMetadata()
location = md['location'] # track's url (to send track to trash)
player.Next()
# handle dynamic playlists. Thanks go to Oleg K (ICQ: 367607160)
new_index = tracklist.GetCurrentTrack()
if new_index == index:
    tracklist.DelTrack(index-1)
else:
    tracklist.DelTrack(index)

retcode = subprocess.call(['kioclient', 'move', location, 'trash:/'])

pathname = urllib2.url2pathname(location)
path = urllib2.urlparse.urlparse(pathname).path
if retcode == 0:
    print 'Successfully trashed "%s"'%path
    sys.exit(0)
else:
    print 'Could not trash "%s"'%path
    sys.exit(1)
