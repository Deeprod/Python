import os
import subprocess
import sys
from colorama import *

text_indent = r'   '

def open_path(path):
    path = os.path.normpath(path)
    try:
        # Windows
        if sys.platform.startswith("win"):
            os.startfile(path)  
            
        # macOS
        else:
            subprocess.run(["open", path], check=True)  

    except:
        print(text_indent + Fore.RED + "Failed to open: " + path + Style.RESET_ALL)