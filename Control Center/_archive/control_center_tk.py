import subprocess
import os
import tkinter
import importlib

from hub import *
from cal import *

#import pyodbc
#os.system('mode con: cols=30 lines=5')


#############################################
## Function to convert a shortcut to a path
#############################################
def sc2path(sc):
    path = ""
    SC_Array = []
    file = open(r"shortcut/Shortcut_List.txt", "r")

    for line in file:
        SC_Array.append(line.split(","))
    file.close()

    for Shortcut in SC_Array:

        if Shortcut[0][:3] == "XXX":

            for x in range(1, 12):

                if Shortcut[0].replace("XXX",str(x)) == sc:

                    if x < 10:
                        xx = "0" + str(x)
                    else:
                        xx = str(x)

                    path = Shortcut[1].replace("\n","").replace("XXX",xx)
                    break
                       
        elif sc == Shortcut[0]:
            path = Shortcut[1].replace("\n","")
            break
            
    return path


#############################################
## Function to append a text to a file
#############################################

def append2file(txt,filename):

    with open(filename, "a") as myfile:

        myfile.write("\n")
        myfile.write(txt)

 
#############################################
## Function to copy a text to the clipboard
#############################################

def copy2clip(txt):

    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def shortcut(txt):

    entry.delete(0, END)
    
    Shortcut_Input_User = txt
    Shortcut_Input_Split = Shortcut_Input_User.split("+")

    for Shortcut_Input in Shortcut_Input_Split:

        path = ""
        prw_ext = ""
        clipboard = False

        if Shortcut_Input == "clear":
        
            os.system('cls')
            continue

        if Shortcut_Input == "sqltest":

            print("bla")
            #print("TTTEEEESSSSTTTTT")
            #cnxn_str = ("Driver={SQL Server Native Client 11.0};Server=MELAIPWBAT01,45600;Database=VALDATA;Trusted_Connection=yes;")
            #cnxn = pyodbc.connect(cnxn_str)
            #print("YAY!")
            #continue
                      
        if Shortcut_Input == "user":
        
            username = input("Enter a Username:")
            name = subprocess.check_output('net user ' + username + ' /domain | FIND /I "Full Name"', shell=True)
            full_name = name.replace(b"Full Name", b"").strip()
            print(full_name)
            continue
        
        if Shortcut_Input == "rub":
            importlib.reload(sys.modules['hub'])
            build_hub()
            Shortcut_Input = "hub"

        if Shortcut_Input == "ral":
            importlib.reload(sys.modules['cal'])
            build_cal()
            Shortcut_Input = "hub"
            
        if Shortcut_Input == "exit":
        
            exit()
                       
        if Shortcut_Input == "app":

            new_shortcut = input("--- Enter a new Shortcut: ")
            new_path = input("--- Enter a new Path: ")
            append2file(new_shortcut + "," + new_path,"Shortcut_List.txt")
            print("New Shortcut created")
            continue
            
        if Shortcut_Input == "del.proj":

            directory = input("Enter a directory:")
            
            for filename in os.listdir(directory):
                
                if filename.endswith(".proj"):
                
                    os.remove(directory + "\\" + filename)
                    print(directory + "\\" + filename)

            continue
            
        if Shortcut_Input[-2:] == "cc":
        
            clipboard = True
            Shortcut_Input = Shortcut_Input[:-2]
            
        if Shortcut_Input[-3:] == "prw":
        
            Shortcut_Input = Shortcut_Input[:-3]
            prw_ext = r"/Prophet.prw"
                        
        if Shortcut_Input[:1] == "w" and len(Shortcut_Input) == 5:

            path = r"\\"
            path = path + "" + Shortcut_Input[-4:]
            
        if Shortcut_Input[:2] == "gg":

            path = r"https://www.google.com/search?q=" + Shortcut_Input[2:]
            
        if path == "":

            path = sc2path(Shortcut_Input)
            
        if path != "" and clipboard == False:

            path = os.path.normpath(path)

            try:
                os.startfile(path + prw_ext)
                #os.system('cls')
            except:
                print("!!!! " + path + prw_ext + " is not valid !!!!")
                                       
        elif path != "" and clipboard == True:

            copy2clip(path + prw_ext)
            print(path + prw_ext + " copied to clipboard")
            
        else:

            print(Shortcut_Input + " is not recognized")
                
                
                
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#############################################
## Start of the program
#############################################

from tkinter import *    
master = Tk()

# Create this method before you create the entry
def return_entry(en):
    """Gets and prints the content of the entry"""
    content = entry.get()
    print(content) 
    shortcut(content)

entry = Entry(master)
entry.grid(row=0, column=1)

button = Button(master, text="Sure!")
button.grid(row=0, column=2)
#button.grid_remove()

# Connect the entry with the return button
entry.bind('<Return>', return_entry) 

mainloop()







            
            
            
            
