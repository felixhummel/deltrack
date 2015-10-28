#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# This prgram is Licenced under GPL, see http://www.gnu.org/copyleft/gpl.html
# Author: Felix Hummel <deltrack@felixhummel.de>
# Thanks to Camille Gallet <camillegallet@yahoo.fr> for the infoamarok script,
# from which this script borrowed a lot.
import dbus
import sys
import subprocess
import logging
import os

try:  # Python 3
    import urllib.parse as urlparse
except ImportError:  # Python 2
    from urllib2 import urlparse

save = [".mp3", ".flac", ".wma", ".ogg"]  # Don't delete dir if it contains any of these files.
exts = [".tqd"]  # Other extensions to delete with same base name.

log = logging.getLogger(__name__)


def main():
    try:
        bus = dbus.SessionBus()
    except:
        log.error("Could not connect to dbus.")
        sys.exit(1)
    try:
        player = dbus.Interface(bus.get_object('org.mpris.amarok', '/Player'),
                                dbus_interface='org.freedesktop.MediaPlayer')
        tracklist = dbus.Interface(bus.get_object('org.mpris.amarok', '/TrackList'),
                                   dbus_interface='org.freedesktop.MediaPlayer')
    except:
        log.error("Could not connect to Amarok.")
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
            tracklist.DelTrack(index - 1)
        else:
            tracklist.DelTrack(index)
    else:
        player.Stop()
        tracklist.DelTrack(0)

    path = ''
    for ext in exts:  # Delete each basename+extension.
        loc = ''.join([basename, ext])
        cmdext = ['kioclient', 'move', loc, 'trash:/']
        log.info("Running %s" % ' '.join(cmdext))
        retcodext = subprocess.call(cmdext)
        path = urlparse.urlparse(loc).path
        if retcodext == 0:
            log.info('Successfully trashed "%s"' % path)
        else:
            log.warn('Could not trash"%s"' % path)

    direc = os.path.split(path)[0]  # If the dir is empty let's get rid of it, as well.
    subdir = ''  # We'll set this below, if it exists.
    direc = direc.replace("%20", ' ')  # Replace KDE's sillyness.
    # The following for loops seem a bit ugly, but this seems quicker than using recursion and ending up many levels deep,
    # and the various exists are off-putting, but we want to exit asap if we can.
    for f in os.listdir(direc):
        if os.path.isdir(os.path.join(direc, f)):  # We'll go one level deep, no more, takes time.
            subdir = os.path.join(direc, f)
            subls = os.listdir(subdir)
            if len(subls) > 15:  # We probably don't want to delete this.
                sys.exit(0)
            for s in subls:
                if os.path.isdir(os.path.join(subdir, s)):  # Only one level deep, so stop here.
                    sys.exit(0)
                if os.path.splitext(s)[1] in save:
                    sys.exit(0)
        if os.path.splitext(f)[1] in save:
            sys.exit(0)

    try:  # If we made it this far, nuke the dir/subdir.
        if subdir:
            rmdir = ['kioclient', 'move', subdir, 'trash:/']
            retcodext = subprocess.call(rmdir)
            log.info("Removed empty subdir %s." % subdir)
        rmdir = ['kioclient', 'move', direc, 'trash:/']
        retcodext = subprocess.call(rmdir)
        log.info("Removed empty dir %s." % direc)
    except OSError:
        log.error("Error removing %s, maybe no perms." % direc)

    sys.exit(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
    main()
