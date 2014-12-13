#!/usr/bin/env python2

import sys

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
    "hibernate",
    "nautilus",
    "deluge",
    "minecraft"
)

# aliases of some commands in <commands>
command_aliases = {
    "intellij": "~/Applications/IntelliJ/bin/idea.sh",
    "lock": "gnome-screensaver-command -l && xset dpms force off",
    "shutdown": "dbus-send --system --print-reply --dest=org.freedesktop.ConsoleKit /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop",
    "standby": "dbus-send --system --print-reply --dest=org.freedesktop.UPower /org/freedesktop/UPower org.freedesktop.UPower.Suspend",
    "hibernate": "dbus-send --system --print-reply --dest=org.freedesktop.UPower /org/freedesktop/UPower org.freedesktop.UPower.Hibernate",
    "nautilus": "nautilus --no-desktop",
    "minecraft": "java -jar ~/Downloads/jar/MagicLauncher_1.2.5.jar"
}
