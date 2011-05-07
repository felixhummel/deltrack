Deltrack is a simple script that moves the currently playing track to trash.

Increase the quality of your music collection by assigning a global shortcut to this script. :)

Installation
============

Copy `deltrack.py` to $HOME/bin

    mkdir -p $HOME/bin
    cp deltrack.py $HOME/bin

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
