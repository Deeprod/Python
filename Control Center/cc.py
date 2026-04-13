import sys
import subprocess
sys.path.append("C:\\Users\\Jonathan.Venturi\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\site-packages")

import os
from colorama import init
from colorama import Fore, Back, Style
init(autoreset=True)

#os.system('mode con: cols=300 lines=600') test
os.system('cls')

from cc_shortcut_class import Shortcut
from cc_clipboard import copy_to_clipboard
from cc_config import *
from cc_lpr_pr import *
from cc_awb import *
from cc_app import *
from cc_breakdown_dir import *
        
#############################################
## Main Loop
#############################################

print(Fore.YELLOW + sys.version  + Style.RESET_ALL)      
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
            full_path = r'C:\temp\github\act-python\Jonathan\Movies'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run streamlit_page.py"',shell=True)
            continue
        
        if shortcut.text == "std":
            full_path = r'C:\temp\github\act-python\Jonathan\Dashboard'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run main.py"',shell=True)
            continue
        
        if shortcut.text == "steas":
            full_path = r'C:\temp\github\act-python\EAS'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run main.py"',shell=True)
            continue
        
        if shortcut.text == "stai":
            full_path = r'C:\temp\github\act-python\Jonathan\Toolkit Ai'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run main.py"',shell=True)
            continue
        
        if shortcut.text == "stair":
            full_path = r'C:\temp\github\act-python\Jonathan\Toolkit Ai'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run response.py"',shell=True)
            continue
        
        if shortcut.text == "stair1":
            full_path = r'C:\temp\github\act-python\Jonathan\Toolkit Ai'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run response_GPT5_v1.py"',shell=True)
            continue     
        
        if shortcut.text == "stair2":
            full_path = r'C:\temp\github\act-python\Jonathan\Toolkit Ai'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run response_GPT5_v2.py"',shell=True)
            continue
        
        if shortcut.text == "stair3":
            full_path = r'C:\temp\github\act-python\Jonathan\Toolkit Ai'
            #Open a new terminal and run a streamlit session
            subprocess.Popen(f'start cmd /K "cd /d {full_path} && py -m streamlit run response_GPT5_v3.py"',shell=True)
            continue
        
        elif "pr/" in shortcut.text:
            pr_sc(shortcut.text)
           
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