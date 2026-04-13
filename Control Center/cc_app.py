from cc_config import *

def sc_app():    
    
    new_shortcut = input(text_indent + "--- Enter a new Shortcut: ")
    new_path = input(text_indent + "--- Enter a new Path: ")
    append2file(new_shortcut + "," + new_path, "Shortcut_List.txt")
    print(text_indent + "New Shortcut created")
    
    
#############################################
## Function to append a text to a file
#############################################
def append2file(txt,filename):

    with open(filename, "a") as myfile:

        myfile.write("\n")
        myfile.write(txt)
        
        
        