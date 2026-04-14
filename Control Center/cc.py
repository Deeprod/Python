import sys
import subprocess
import os
from colorama import init
from colorama import Fore, Style
init(autoreset=True)

#os.system('mode con: cols=300 lines=600') test
os.system('cls')

from cc_shortcut_class import Shortcut
from cc_clipboard import copy_to_clipboard
from cc_config import *
from cc_awb import *
from cc_app import *
from cc_breakdown_dir import *
        
#############################################
## Main Loop
#############################################

print(Fore.YELLOW + sys.version + Style.RESET_ALL)      
print(sys.executable)

while True: 
    
    print("")
    shortcut_input = input(Fore.GREEN + "Input Shortcut: " + Style.RESET_ALL)
    shortcut_input_split = shortcut_input.split("+")
    
    for shortcut_input in shortcut_input_split:

        if len(shortcut_input) == 0:
            continue
            
        shortcut = Shortcut(shortcut_input)
           
        if shortcut.text == "stm":

            if sys.platform.startswith("win"):
                full_path = r"C:\Users\JonathanVenturi\Documents\Python\Movies"
                cmd = f'cd /d "{full_path}" && py -m streamlit run streamlit_page.py'
                subprocess.Popen(f'start cmd /K "{cmd}"', shell=True)

            else:
                full_path = "/Users/jonathanventuri/Documents/Python/Movies"
                cmd = f'cd "{full_path}" && python3 -m streamlit run streamlit_page.py'

                # Escape quotes for AppleScript
                cmd_escaped = cmd.replace('"', '\\"')

                subprocess.Popen([
                    "osascript",
                    "-e",
                    f'tell application "Terminal" to do script "{cmd_escaped}"'
                ])

            continue
        
        if shortcut.text == "std":
            full_path = r'C:\temp\github\act-python\Jonathan\Dashboard'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run main.py"',shell=True)
            continue
           
        elif "awb/" in shortcut.text or "tools/" in shortcut.text:
            awb_sc(shortcut.text)
        
        elif shortcut.text == "clear":
            os.system('cls')
            
        elif shortcut.text == "exit":
            exit()
                       
        elif shortcut.text == "app":
            sc_app()      
            
        if shortcut.path == "":
            print(text_indent + Fore.RED + shortcut.text + " is not recognized" + Style.RESET_ALL)
            continue
        
        if shortcut.is_breakdown:
            breakdown_dir(shortcut)
            
        elif shortcut.is_clipboard:
            copy_to_clipboard(shortcut.path)
            print(text_indent + "Copied to clipboard: " + shortcut.path)
            
        else:
            open_path(shortcut.path)