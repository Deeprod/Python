import pandas as pd
from datetime import datetime

def convert_minutes_to_hours(minutes):
    hours = minutes // 60
    mins = str(minutes % 60).zfill(2)
    return f"{hours}h{mins}"

def display_list(list, list2 = None):

    if(list is None):
        return    
    
    count = 0
    for index, item in enumerate(list):
        if not pd.isna(item):
            count +=1
            
            if(list2 is None):
                print(f"{count}) {item}")
            else:
                print(f"{count}) {item} [{list2[index]}]")
            
def average(lst):
    return sum(lst) / len(lst) if lst else 0  # Avoid division by zero

def jk_color_theme(jk):
    if jk <= 5:
        return ":red[5]"
    if jk == 6:
        return ":orange[6]"
    if jk == 7:
        return ":blue[7]"
    if jk == 8:
        return ":green[8]"
    if jk == 9:
        return ":violet[9]"
    
def days_compared_to(date_DDMMYYYY):
    if date_DDMMYYYY == '?':
        return '?'
    date_obj = datetime.strptime(date_DDMMYYYY, "%d/%m/%Y")
    return (datetime.today() - date_obj).days

def DDMMYYYY_to_MMYY(date_string):
    date_obj = datetime.strptime(date_string, "%d/%m/%Y")
    return date_obj.strftime("%m-%Y")
