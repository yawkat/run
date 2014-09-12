#!/usr/bin/env python2

width = 400
line_height = 18
x = 1600 - width
y = 18
bg = "#073642"
bg_highlight = "#586e75"
fg = "#fdf6e3"
font = "\"Source Code Pro\" 8 bold"

input_format = "> %s"
expression_prefix = "#"
expression_format = "# %s = %s"
suggestion_format = "  %s"

commands = [
    "firefox",
    "xfce4-terminal",
    "rhythmbox",
    "thunderbird",
    "quasselclient",
    "subl",
    "intellij",
    "gimp",
    "inkscape",
    "lock",
    "shutdown"
]

command_aliases = {
    "rhythmbox": "rhythmbox --rhythmdb-file ~/SSD/Music/rhythmbox/db --playlists-file ~/SSD/Music/rhythmbox/playlists",
    "intellij": "~/Applications/IntelliJ/bin/idea.sh",
    "lock": "gnome-screensaver-command -l",
    "shutdown": "dbus-send --system --print-reply --dest=org.freedesktop.ConsoleKit /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop"
}
