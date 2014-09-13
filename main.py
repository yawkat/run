#!/usr/bin/env python2

import Tkinter as tk
import sys
import subprocess
import traceback

from config import *

# current entered command
command = ""
# Label objects for suggestions
suggestion_labels = {}
# index of the current suggestion in config.commands
selected_suggestion = 0

def key(evt):
    global command, selected_suggestion
    if evt.keycode is 9: # escape
        exit()
    elif evt.keycode is 22: # backspace
        command = command[0:-1] # remove last char
        update_ui()
    elif evt.keycode is 36: # enter
        if command != "":
            try:
                cmd = command
                # use suggestion if there is one
                if selected_suggestion >= 0 and selected_suggestion < len(commands):
                    cmd = commands[selected_suggestion]
                    if cmd in command_aliases:
                        cmd = command_aliases[cmd]
                print "Running '%s'..." % cmd
                # run
                subprocess.Popen(cmd, shell=True)
            except:
                traceback.print_exc()
        exit()
    elif evt.keycode is 111: # up
        # previous suggestion
        if selected_suggestion > 0:
            selected_suggestion -= 1
            update_ui()
    elif evt.keycode is 116: # down
        # next suggestion
        if selected_suggestion < len(commands) and selected_suggestion is not -1:
            selected_suggestion += 1
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
    global command_var, suggestion_labels, selected_suggestion

    # suggestions
    suggest = set(filter(lambda l: l.startswith(command), commands))

    if len(suggest) is 0 and command[0].startswith(expression_prefix):
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
    frame.master.geometry("%sx%s+%s+%s" % (width, line_height * (1 + len(suggest)), x, y))

    # make labels for new suggestions we didn't have labels for before
    for suggestion in suggest:
        if not suggestion in suggestion_labels:
            label = tk.Label(frame, text=(suggestion_format % suggestion), anchor="nw", justify="left", fg=fg, bg=bg, font=font)
            suggestion_labels[suggestion] = label

    # limit suggested to < len and >= 0, or -1 if no suggestions
    # also moves suggestion focus if the selected suggestion disappeared
    actual_selected = selected_suggestion
    if len(suggest) > 0:
        if actual_selected is -1:
            actual_selected = 0
        # try to find a suggestion above the removed one first if one was removed
        while actual_selected > 0 and not commands[actual_selected] in suggest:
            actual_selected -= 1
        # try below too
        if not commands[actual_selected] in suggest:
            actual_selected = selected_suggestion
            while actual_selected < len(commands) - 1 and not commands[actual_selected] in suggest:
                actual_selected += 1
    else:
        # no suggestions
        actual_selected = -1
    selected_suggestion = actual_selected

    # display and pack suggestion labels
    i = 0
    for k in commands:
        if not k in suggestion_labels:
            continue
        label = suggestion_labels[k]
        if k in suggest:
            # suggestion shown
            label.pack(fill="both")
            if i is selected_suggestion:
                label.config(background=bg_highlight)
            else:
                label.config(background=bg)
        else:
            # not shown
            label.pack_forget()
        i += 1

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

update_ui()

# force focus on the frame
frame.after(0, lambda: frame.master.focus_force())
frame.focus_set()

# main
frame.mainloop()
