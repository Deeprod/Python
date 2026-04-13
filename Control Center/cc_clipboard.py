import subprocess

#############################################
## Function to copy a text to the clipboard
#############################################
def copy_to_clipboard(txt):

    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)


def check_if_clipboard(shortcut):
    
    if len(shortcut) == 0:
        is_clipboard = False
        shortcut = shortcut
        
    elif shortcut[-2:] == "cc":
        is_clipboard = True
        shortcut = shortcut[:-2]
        
    else:
        is_clipboard = False
        shortcut = shortcut
        
    return is_clipboard, shortcut
