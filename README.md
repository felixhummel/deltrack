Deltrack is a simple script that moves the currently playing track to trash.

Increase the quality of your music collection by assigning a global shortcut to this script. :)

Installation
============

Copy `deltrack.py` to $HOME/bin

    mkdir -p $HOME/bin
    wget -O $HOME/bin/deltrack.py https://raw.githubusercontent.com/felixhummel/deltrack/master/deltrack.py
    chmod +x $HOME/bin/deltrack.py

and install the input actions:

- go to System Settings --> Input Actions
- in the lower left: Edit --> Import --> select "input_actions.khotkeys"
- (optional) Edit the shortcut to your choice. Default: "Win+Alt+d" (Win == Meta).
- (optional) Edit the command if you copied `deltrack.py` somewhere else.

Have fun!

Alternative Installation with Launcher
======================================

- right-click the "Application Laucher" (blue K, in the lower left corner)
- select "Menu Editor"
- click "New Item" and give it a name (like "delete current track")
- Command: "python $HOME/bin/deltrack.py" (without quotes)
- untick "Enable launch feedback"
- open the "Advanced" tab (ALT+A)
- click the "Current shortcut key" button and assign the shortcut

Slightly Advanced Config
========================

- line 15 contains a list called "exts".  Add other file extentions here to be deleted along with the song itself.  For example, exts=[] will not utilize this feature at all, while exts[".tqd"] will, if songName.mp3 is our deleted file, also delete songName.tqd.
- There is a similar list called "save".  This contains all extensions to recognize as "songs".  If a directory containing the song you just deleted contains NO files with the file extensions in save[], the entire directory will be deleted.
  This prevents empty directories from being scattered about, and also handles the case where a useless cover art image or playlist is left behind.

Requirements
============

- python >= 2.5
- amarok >= 2.0
- KDE >= 4

Author: Felix Hummel <deltrack@felixhummel.de>

Thanks
======

- Camille Gallet <camillegallet@yahoo.fr> for the infoamarok script
- Oleg K for the dynamic playlists fix
- evll for the input actions hint
