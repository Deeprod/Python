from cc_config import *
import colorama
from colorama import init
from colorama import Fore, Back, Style
import os
import sys
from datetime import datetime

def prophet_run_folder_action(foldername):
    #Create an input loop
    while True: 
    
        TopX = len(foldername)
        #Display content of the array
        print("")
        print(text_indent + "Number of runs displayed:")
        for prophet_run in range(0,TopX):
            print(text_indent * 2 + str(prophet_run+1) + ") " + foldername[prophet_run])
            
        print("")
        lpr_input = input(text_indent + Fore.YELLOW + "Input (run, rlall, Xrl, Xsp, Xgb, end, exit): " + Style.RESET_ALL)
        
        #If input end, close the loop and go back to main loop
        if lpr_input == "end":
            break
            
        if lpr_input == "exit":
            exit()

        #If input "run", the list of runs is displayed again (useful when scrolling not allowed)
        if lpr_input == "run":
            for prophet_run in range(0,TopX):
                print(text_indent * 2 + str(prophet_run+1) + ") " + foldername[prophet_run])
        
        if lpr_input == "rlall":
            for prophet_run in range(0,TopX):
                text_bf_error = text_indent * 2 + str(prophet_run+1) + ") " + foldername[prophet_run]
                adj = 90 - len(text_bf_error)
                print(text_bf_error + " " * adj + Back.RED + print_runlog(foldername[prophet_run] + "\\results\\RUN_01\\runlog.run","short") + Style.RESET_ALL)
                
        #If input a number, go directly to the folder location of the relevant run
        top10 = [str(x) for x in range(1,TopX+1)]
        if lpr_input in top10:
            folder_name = foldername[int(lpr_input)-1]
            print(text_indent * 2 + "Opening: " + folder_name)
            try:
                os.startfile(os.path.normpath(folder_name))
            except:
                print("Could not open file: " + os.path.normpath(folder_name))
        
        #If input a number followed by "rl", open the runlog of the relevant run
        top10rl = [str(x) + "rl" for x in range(1,TopX+1)]
        if lpr_input in top10rl:   
            folder_name = foldername[int(lpr_input[:-2])-1] + "\\results\\RUN_01\\runlog.run"
            print(text_indent * 2 + "Opening: " + folder_name)
            print_runlog(folder_name,"full")
        
        #If input a number followed by "sp", open the xml of the relevant run
        top10sp = [str(x) + "sp" for x in range(1,TopX+1)]
        if lpr_input in top10sp:   
            folder_name = foldername[int(lpr_input[:-2])-1] + "\\results\\RUN_01\\ExecutionSummary.xml"
            print(text_indent * 2 + "Opening: " + folder_name)
            
            #Extract errors in the console
            file = open(os.path.normpath(folder_name), "r")
            i = 0
            for line in file:
                if "Accumulations" in line:
                    break
                else:
                    if "SummaryItem name=" in line:
                        i = i + 1
                        out_prod = line[line.find("SummaryItem name=")+18:line.find("SummaryItem name=")+18+6]
                        out_status = line[line.find("status=")+8:line.find("status=")+8+6]
                        out_start = line[line.find("started=")+9:line.find("started=")+9+19]
                        out_finish = line[line.find("finished=")+10:line.find("finished=")+10+19]
                        print(text_indent * 2 + "Error " + str(i) + ": " + out_prod + " / " + out_status + " / " + out_start + " / " + out_finish)

            file.close()                         
        
        #If input a number followed by "gb", open the global table of the relevant run
        top10gb = [str(x) + "gb" for x in range(1,TopX)]
        if lpr_input in top10gb:   
            folder_name = foldername[-int(lpr_input[:-2])] + "\\Tables.zip\\Global.fac"
            print(text_indent * 2 + folder_name)
            
            #Extract global information in the console
            file = open(os.path.normpath(folder_name), "r")
            i = 0
            for line in file:
                if ",CC_" not in line:
                    continue
                else:
                    line_split = line[2:-1].split(",")
                    print(text_indent * 2 + line_split[0] + " " * (30 - len(line_split[0])) + line_split[1])

            file.close()  
            
            
            
#############################################
## Function to print a runlog into the console
#############################################
def print_runlog(foldername,outtype):

    #Extract errors in the console
    file = open(os.path.normpath(foldername), "r")
    i = 0
    for line in file:
        if "|T=ERROR|" in line:
            i = i + 1
            error_text = line[line.find("|T=ERROR|")+11:-1]
            error_text = error_text.replace("Generic Table lookup failure ","")
            error_text = error_text.replace("Sub Product ","SP")
            error_text = error_text.replace("Variable ","")
            error_text = error_text.replace("MPF Line Number ","L")
            error_text = error_text.replace("Time Period ","t")
            error_text = error_text.replace("^0aProduct","")
            error_text = error_text.replace("Model Point ","MP")
            error_text = error_text.replace(". Index: ",": ")
            error_text = error_text.replace(".fac","")
            error_text = error_text.replace("'","")
            error_text = error_text.replace("ERROR PVA009 Value for POL_TERM_Y is negative^0a^09model point ","POL_TERM_Y negative MP")
            error_text = error_text.replace("sub product code","SP")
            
            if "POL_TERM_Y negative" in error_text:
                color_text = Back.GREEN
            else:
                color_text = ""
            
            if outtype == "full":
                print(text_indent * 2 + color_text + str(i) + ": " + error_text + Style.RESET_ALL)
            
    file.close()
    if outtype == "full":
        print(text_indent * 2 + Back.RED + "Number of Errors: " + str(i) + Style.RESET_ALL)
    
    return str(i)
    
    
    


def lpr_sc():

    #After the slash is the max number of runs to check
    max_run = input(text_indent + Fore.YELLOW + "Max runs: " + Style.RESET_ALL)      
    lpr_env = input(text_indent + Fore.YELLOW + "Env: " + Style.RESET_ALL)   
    lpr_ym = input(text_indent + Fore.YELLOW + "Date: " + Style.RESET_ALL)   
    
    if len(lpr_ym) == 4:
        lpr_ym = "20" + lpr_ym
    if lpr_env == "p" or lpr_env == "":
        lpr_env = "PRD1"
    if lpr_env == "d4":
        lpr_env = "DEV4"   
    if max_run == "":
        max_run = 20
    
    root_path_chosen = []
    root_path_chosen.append('P:\\' + lpr_env + '\\' + str(lpr_ym) + '\Output\Master')

    #Create a list of all the .FIN files in the folders specified above
    full_path = []
    for rp in root_path_chosen:
        print(text_indent + "Looking through: " + rp)
        listdir_temp = os.listdir(rp)
        for x in listdir_temp:
            if x[-4:] == ".FIN":
                full_path.append(rp + "/{0}".format(x))
            
    #Sort the list by creation date
    try:
        #if ind != "dr":
        full_path_sort = sorted(full_path,key=os.path.getmtime)
        #else:
        #    full_path_sort = full_path
    except:
        input(text_indent + Fore.RED + "!!! Error with the sort !!!" + + Style.RESET_ALL)
        return True
        
    print(text_indent + "Number of runs found: " + str(len(full_path)))
    if max_run == '':
       print(text_indent + "Only display top " + str(10)) 
       max_run = "10"
    else:
       print(text_indent + "Only display top " + str(max_run))
    
    max_run = int(max_run)
    full_path_sort = full_path_sort[-max_run:] #Keep only the most recent
    
    #if ind != "dr":
    full_path_sort.reverse()

    #Remove the .FIN at the end of each items
    #print([x[:-4] + datetime.fromtimestamp(os.path.getctime(x)).strftime('%Y-%m-%d %H:%M:%S') for x in full_path_sort])
    full_path_sort = [x[:-4] for x in full_path_sort]

    
    prophet_run_folder_action(full_path_sort) 
        
    return True
    
    
   
def pr_sc(Shortcut_Input):

    #Create a list of all the folders in a prophet run folder
    #The format of the shortcut should be 'pr/DEV1/112'
    #You can add a criteria to find (optional) 'pr/DEV1/112/DLR'
    i = 0
    pr_list = []
    
    #This allows multiple find criteria as long as it is separated by "/"
    pr_find = Shortcut_Input[3:].lower().split("/")
    pr_path = "P:\\" + pr_find[0] + '\\' + str(202) + str(pr_find[1]) + '\Output\Master' 
    pr_path = os.path.normpath(pr_path)
    
    try:
        pr_dirs = os.listdir(pr_path)
    except:
        print("Could not open: " + pr_path)
        return True
        
    for pr_dir in pr_dirs:
        if pr_dir.find('.') == -1:
            
            pr_ok = False
            if len(pr_find) == 2:
                pr_ok = True
            else:
                if pr_find[2] in pr_dir.lower():
                    pr_ok = True
                    
            if pr_ok:
                i = i + 1
                pr_list.append(pr_path + '//' + pr_dir)

    prophet_run_folder_action(pr_list)
    
    return True    