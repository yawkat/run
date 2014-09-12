#!/usr/bin/env python2

import Tkinter as tk
import sys
import subprocess
import traceback

from config import *

command = ""
suggestion_labels = {}
selected_suggestion = 0

def key(evt):
    global command, selected_suggestion
    if evt.keycode is 9: # escape
        exit()
    elif evt.keycode is 22: # backspace
        command = command[0:-1]
        update_ui()
    elif evt.keycode is 36: # enter
        if command != "":
            try:
                cmd = command
                if selected_suggestion >= 0 and selected_suggestion < len(commands):
                    cmd = commands[selected_suggestion]
                    if cmd in command_aliases:
                        cmd = command_aliases[cmd]
                print "Running '%s'..." % cmd
                subprocess.Popen(cmd, shell=True)
            except:
                traceback.print_exc()
        exit()
    elif evt.keycode is 111: # up
        if selected_suggestion > 0:
            selected_suggestion -= 1
            update_ui()
    elif evt.keycode is 116: # down
        if selected_suggestion < len(commands) and selected_suggestion is not -1:
            selected_suggestion += 1
            update_ui()
    else:
        command += evt.char
        update_ui()

def exit(evt=None):
    sys.exit()

def update_ui():
    global frame
    frame.after(0, update_ui_now)

def update_ui_now():
    global command_var, suggestion_labels, selected_suggestion

    suggest = set(filter(lambda l: l.startswith(command), commands))

    if len(suggest) is 0 and command[0].startswith(expression_prefix):
        expression = command[len(expression_prefix):]
        result = "ERROR"
        try:
            result = eval(expression)
        except:
            result = sys.exc_info()[0]
        command_var.set(expression_format % (expression, result))
    else:
        command_var.set(input_format % command)

    frame.master.geometry("%sx%s+%s+%s" % (width, line_height * (1 + len(suggest)), x, y))

    for suggestion in suggest:
        if not suggestion in suggestion_labels:
            label = tk.Label(frame, text=(suggestion_format % suggestion), anchor="nw", justify="left", fg=fg, bg=bg, font=font)
            suggestion_labels[suggestion] = label

    actual_selected = selected_suggestion
    if len(suggest) > 0:
        if actual_selected is -1:
            actual_selected = 0
        while actual_selected > 0 and not commands[actual_selected] in suggest:
            actual_selected -= 1
        if not commands[actual_selected] in suggest:
            actual_selected = selected_suggestion
            while actual_selected < len(commands) - 1 and not commands[actual_selected] in suggest:
                actual_selected += 1
    else:
        actual_selected = -1
    selected_suggestion = actual_selected

    i = 0
    for k in commands:
        if not k in suggestion_labels:
            continue
        label = suggestion_labels[k]
        if k in suggest:
            label.pack(fill="both")
            if i is selected_suggestion:
                label.config(background=bg_highlight)
            else:
                label.config(background=bg)
        else:
            label.pack_forget()
        i += 1

frame = tk.Frame(bg=bg)
frame.master.attributes("-type", "dock")
frame.master.attributes("-topmost", "true")
frame.bind("<Key>", key)
frame.bind("<FocusOut>", exit)

frame.grid()

command_var = tk.StringVar()
command_label = tk.Label(frame, textvariable=command_var, anchor="nw", justify="left", fg=fg, bg=bg, font=font, width=width)
command_label.pack(fill="x")

update_ui()

frame.after(0, lambda: frame.master.focus_force())
frame.focus_set()
frame.mainloop()
