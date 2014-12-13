#!/usr/bin/env python2

import tacui
import config
import sys
import os
import subprocess
import threading
import traceback

ui = tacui.SelectingTacUI()

for command in config.commands:
    ui.add(command, True, config.suggestion_format % command)

def scan_installed():
    scanned = set()
    for folder in os.getenv("PATH").split(":"):
        try:
            for f in os.listdir(folder):
                if f not in config.commands:
                    scanned.add(f)
        except:
            pass
    for f in sorted(scanned):
        ui.add(f, False, config.suggestion_format % f)

def decorate(text):
    if text.startswith(config.expression_prefix):
        text = text[len(config.expression_prefix):]
        try:
            result = eval(text)
        except:
            result = sys.exc_info()[0]
        return config.expression_format % (text, result)
    else:
        return config.input_format % text

def launch():
    command = ui.selected_item
    if command in config.command_aliases:
        command = config.command_aliases[command]
    try:
        subprocess.Popen(command, shell=True)
    except:
        traceback.print_exc()
    ui.exit()

def finish_setup():
    ui.input.decorate = decorate
    ui.input.enter = launch

    scanner = threading.Thread(target=scan_installed)
    scanner.daemon = True
    scanner.start()

ui.on_finish_setup(finish_setup)

ui.open()
