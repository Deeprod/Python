from cc_config import *
import colorama
from colorama import init
from colorama import Fore, Back, Style
import os
import sys

def check_if_breakdown(shortcut):
    
    if len(shortcut) == 0:
        is_breakdown_path = False
        shortcut = shortcut
        text_find = ""
        
    elif "." in shortcut:
        is_breakdown_path = True
        shortcut_split = shortcut.split(".")
        shortcut = shortcut_split[0]
        text_find = shortcut_split[1]
        
    else:
        is_breakdown_path = False
        shortcut = shortcut
        text_find = ""
        
    return is_breakdown_path, shortcut, text_find


def breakdown_dir(shortcut):
    
    file_output = []
    count = 0
    for root, dirs, files in os.walk(shortcut.path):
        for file in files:
            if ".lnk" in file or ".ini" in file:
                continue
            
            if shortcut.text_find != "":
                if not shortcut.text_find in file:
                    continue

            count = count + 1
            print(text_indent + "File " + str(count) + ": " + file + " (" + str(count) + ")")
            file_output.append(root + '\\' + file)

        break

    if count > 1:
        input_console = input(text_indent + Fore.YELLOW + "Input: " + Style.RESET_ALL)
        
        if(input_console == ""):
            return True
        
        if input_console == "exit":
            exit()
            
        if(input_console.isdigit()):
            path = os.path.normpath(file_output[int(input_console)-1])
            open_path(path)
        
    elif count == 1:
        path = os.path.normpath(file_output[0])
        open_path(path)
        
    return True