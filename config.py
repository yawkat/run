#!/usr/bin/env python2

import sys

# width of the launcher box
width = 400
# height of each launcher entry
line_height = 18

if len(sys.argv) > 1:
    screen_width = int(sys.argv[1])
else:
    screen_width = 1600
# location of the launcher
x = screen_width - width
y = 18
# background color
bg = "#002b36"
# background color of the selected suggestion
bg_highlight = "#586e75"
# text color
fg = "#fdf6e3"
# text color
fg_application = "#93a1a1"
# text font
font = "\"Source Code Pro\" 8 bold"

# format used for command display (first line)
input_format = "> %s"
# prefix for expressions (Typing '<expression_prefix><expression>' will be parsed as an expression)
expression_prefix = "#"
# expression display format
expression_format = "# %s = %s"
# display format for command suggestions (two spaces to pad with '> ')
suggestion_format = "  %s"

# available commands
commands = (
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
    "shutdown",
    "standby",
    "nautilus",
    "deluge",
    "minecraft"
)

# aliases of some commands in <commands>
command_aliases = {
    "rhythmbox": "rhythmbox --rhythmdb-file ~/SSD/Music/rhythmbox/db --playlists-file ~/SSD/Music/rhythmbox/playlists",
    "intellij": "~/Applications/IntelliJ/bin/idea.sh",
    "lock": "gnome-screensaver-command -l",
    "shutdown": "dbus-send --system --print-reply --dest=org.freedesktop.ConsoleKit /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop",
    "standby": "dbus-send --system --print-reply --dest=org.freedesktop.UPower /org/freedesktop/UPower org.freedesktop.UPower.Suspend",
    "nautilus": "nautilus --no-desktop",
    "minecraft": "java -jar ~/Downloads/jar/MagicLauncher_1.2.5.jar"
}
