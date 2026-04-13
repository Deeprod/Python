def check_if_google_search(shortcut):
    
    path = ""
    
    if len(shortcut) == 0:
        is_google_search = False
        shortcut = shortcut
        
    elif shortcut[:2] == "gg":
        is_google_search = True
        shortcut = shortcut[2:]
        path = r"https://www.google.com/search?q=" + shortcut
        
    else:
        is_google_search = False
        shortcut = shortcut
        
    return is_google_search, shortcut, path
