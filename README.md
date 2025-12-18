# Simple-Text-Editor

A small text editor with new/save/load functionality, all from a terminal-based interface.

Still thoroughly in the work-in-progress phase.

Written using the Tkinter graphical library for Python.

Features:
---
* Terminal-based navigation with commands
* File opening, editing, and saving
* Command memory via the up- and down-arrow keys
* Colorscheme manipulation, including presets and custom foreground and background commands

List of commands:
---
* LOAD, OPEN, L,                  - Load file by name
* SAVE, S,                        - Save file by name
* DELETE, DESTROY, DEL,           - Delete file by name
* NEW, CLEAR, WIPE,               - Empty text box
* LIST, LS, FILES,                - Show available files
* BGCOLOR, COLOR, BGC, C,         - Change background color
* FGCOLOR, FGC,                   - Change text color
* COLORSCHEME, CS,                - Change colorscheme
* RESET, REBOOT, REFRESH,         - Reboot the application
* EXIT, QUIT, STOP, CLOSE,        - Close the application
* HELP, ?,                        - List available commands

Dependencies:
---
* Python & Tkinter
