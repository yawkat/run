#!/usr/bin/env python2

import Tkinter as tk
import os
import sys
import subprocess
import traceback
import threading

from config import *

# current entered command
command = ""
# Label objects for suggestions
suggestion_labels = []
# current suggestion in config.commands
selected_suggestion = None
selected_suggestion_index = -1
suggestions = ()

TYP_CUSTOM = 0
TYP_APPLICATION = 1

class Command():
    def __init__(self, name, typ=TYP_CUSTOM, command=None):
        if command is None:
            command = name
        self.name = name
        self.command = command
        self.typ = typ

command_objects = list(map(lambda x: Command(x, command=command_aliases.get(x, x)), commands))

def scan_installed():
    command_names = set(map(lambda c: c.name, command_objects))
    scanned = {}
    for folder in os.getenv("PATH").split(":"):
        try:
            for f in os.listdir(folder):
                if f not in command_names:
                    command_names.add(f)
                    scanned[f] = Command(f, typ=TYP_APPLICATION)
        except:
            pass
    for f in sorted(scanned):
        command_objects.append(scanned[f])

scanner = threading.Thread(target=scan_installed)
scanner.daemon = True
scanner.start()

def key(evt):
    global command, selected_suggestion, selected_suggestion_index, suggestions
    if evt.keycode is 9: # escape
        exit()
    elif evt.keycode is 22: # backspace
        command = command[0:-1] # remove last char
        update_ui()
    elif evt.keycode is 36: # enter
        try:
            cmd = command
            # use suggestion if there is one
            if selected_suggestion is not None:
                cmd = selected_suggestion.command
            print "Running '%s'..." % cmd
            # run
            subprocess.Popen(cmd, shell=True)
        except:
            traceback.print_exc()
        exit()
    elif evt.keycode is 111: # up
        # previous suggestion
        if len(suggestions) is not 0:
            selected_suggestion_index -= 1
            while selected_suggestion_index < 0:
                selected_suggestion_index += len(suggestions)
            selected_suggestion = suggestions[selected_suggestion_index]
            update_ui()
    elif evt.keycode is 116: # down
        # next suggestion
        if len(suggestions) is not 0:
            selected_suggestion_index += 1
            while selected_suggestion_index >= len(suggestions):
                selected_suggestion_index -= len(suggestions)
            selected_suggestion = None
            update_ui()
    else:
        command += evt.char
        update_ui()

def exit(evt=None): # optional evt arg so we can use it directly for the unfocus listener
    sys.exit()

def update_ui():
    global frame
    # run on ui thread
    frame.after(0, update_ui_now)

def update_ui_now():
    global command_var, suggestion_labels, selected_suggestion, selected_suggestion_index, suggestions

    # suggestions
    suggestions = list(filter(lambda l: l.name.startswith(command), command_objects))[:len(suggestion_labels)]

    if len(suggestions) is 0 and command[0].startswith(expression_prefix):
        # parse expression
        expression = command[len(expression_prefix):]
        result = "ERROR"
        try:
            result = eval(expression)
        except:
            result = sys.exc_info()[0]
        # display expression and result
        command_var.set(expression_format % (expression, result))
    else:
        # display command input
        command_var.set(input_format % command)

    # resize for suggestions
    frame.master.geometry("%sx%s+%s+%s" % (width, line_height * (1 + len(suggestions)), x, y))

    # limit suggested to < len and >= 0, or -1 if no suggestions
    # also moves suggestion focus if the selected suggestion disappeared

    try:
        selected_suggestion_index = suggestions.index(selected_suggestion)
    except ValueError:
        if selected_suggestion_index < 0:
            if len(suggestions) is 0:
                selected_suggestion_index = -1
            else:
                selected_suggestion_index = 0
        else:
            selected_suggestion_index = min(len(suggestions) - 1, selected_suggestion_index)

    if selected_suggestion_index >= 0:
        selected_suggestion = suggestions[selected_suggestion_index]
    else:
        selected_suggestion = None

    # display and pack suggestion labels
    for i in range(len(suggestions)):
        suggestion = suggestions[i]
        label = suggestion_labels[i]
        label[1].set(suggestion_format % suggestion.name)
        # suggestion shown
        label[0].pack(fill="both")
        if suggestion == selected_suggestion:
            label[0].config(background=bg_highlight)
        else:
            label[0].config(background=bg)
        if suggestion.typ == TYP_CUSTOM:
            label[0].config(foreground=fg)
        else:
            label[0].config(foreground=fg_application)

frame = tk.Frame(bg=bg)
# xlib hacks to float above WM
frame.master.attributes("-type", "dock")
frame.master.attributes("-topmost", "true")
frame.bind("<Key>", key)
frame.bind("<FocusOut>", exit) # hide on unfocus

frame.grid()

command_var = tk.StringVar()
command_label = tk.Label(frame, textvariable=command_var, anchor="nw", justify="left", fg=fg, bg=bg, font=font, width=width)
command_label.pack(fill="x")

for _ in range(20):
    v = tk.StringVar()
    label = tk.Label(frame, textvariable=v, anchor="nw", justify="left", fg=fg, bg=bg, font=font, width=width)
    suggestion_labels.append((label, v))

update_ui()

# force focus on the frame
frame.after(0, lambda: frame.master.focus_force())
frame.focus_set()

# main
frame.mainloop()
