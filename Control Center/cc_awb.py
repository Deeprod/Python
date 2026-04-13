from cc_config import *
import colorama
from colorama import init
from colorama import Fore, Back, Style
import os
import sys


def awb_sc(Shortcut_Input):

    if "awb/" in Shortcut_Input:
        location = r'M:\Acturial\Current\Actuarial Systems Team\Prophet\AWB\\'
        text_find = Shortcut_Input[4:]
        text_find2 = "Assumption_Workbook"
    elif "tools/" in Shortcut_Input:
        location = r'M:\Acturial\Current\Actuarial Systems Team\Tools\\'
        text_find = Shortcut_Input[6:]
        text_find2 = ""
        
    print(text_indent + "Text to find: " + str(text_find))
    
    file_output = []
    awb_count = 0
    for root, dirs, files in os.walk(location):
        if "Archive" in root or "Checks" in root or "_archive" in root or "MPF Sample" in root:
            continue
        else:
            for file in files:
                if text_find in file and text_find2 in file:
                    awb_count = awb_count + 1
                    print(text_indent + "File " + str(awb_count) + ": " + root + '\\' + file + " (" + str(awb_count) + ")")
                    file_output.append(root + '\\' + file)

    awb_input = input(text_indent + Fore.YELLOW + "Input: " + Style.RESET_ALL)
    
    if(awb_input == ""):
        return True

    try:
        os.startfile(os.path.normpath(file_output[int(awb_input)-1]))
    except:
        print("File open failed")
        
    return True