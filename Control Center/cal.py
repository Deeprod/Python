import os
import re
import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None)
import csv

from numpy import genfromtxt

def build_cal():
    
    def bg(txt):
        if txt == "orange":
            return"#fef0db;"
        elif txt == "red":    
            return "rgba(253, 197, 208, 0.7);"

    root_folder = r"C:\Users\Jonathan\Google Drive\Python\Control Center\hub"

    bf_mth = 1
    in_mth = 2
    af_mth = 3

    month_end = [9999,31,28,31,30,31,30,31,31,30,31,30,31]
    last_month_end = [9999,31,31,28,31,30,31,30,31,31,30,31,30]
    month_name = ["99999", "January","February","March","April","May","June","July","August","September","October","November","December"]

    month_start = {2020: [9999,0,0,0,0,0,0,0,0,0,0,26,30],
                   2021: [9999,28,1,1,29,26,31,28,26,30,27,1,29]}

    content = pd.read_csv("hub\\csv\\master_calendar.csv")
    print(content)
    
    for year in [2020,2021]:

        for month in [1,2,3,4,5,6,7,8,9,10,11,12]:

            d = month_start[year][month]
            
            row = 0 
            day_div = []
            grid_map = []
            
            status = bf_mth

            while True:
            
                row = row + 1
                
                for i in range(7):
                    
                    if (d > last_month_end[month] or d == 1)  and status == bf_mth:
                        d = 1
                        status = in_mth
                        
                    if d > month_end[month] and status == in_mth:
                        d = 1
                        status = af_mth
                        
                    day_div_string = """<div class="day""" + (" disabled" if status != in_mth else "") + """\">""" + str(d) + """</div>"""
                    day_div.append(day_div_string)

                    if status == in_mth:
                        grid_map.append([row+1,i+1])

                    d = d + 1

                if status == af_mth:
                    break
                    
            #print(grid_map)

            page = """
            <head>
                <link rel="stylesheet" href="..\css\style.css">"""

            page = page + """
            </head>
            <body>
            <div class="header">
                """ + month_name[month] + """ """ + str(year) + """
            </div>
            <div class="calendar-container mt-75">

                <div class="calendar">
                    <span class="day-name">Mon</span>
                    <span class="day-name">Tue</span>
                    <span class="day-name">Wed</span>
                    <span class="day-name">Thu</span>
                    <span class="day-name">Fri</span>
                    <span class="day-name">Sat</span>
                    <span class="day-name">Sun</span>"""

                            
            for i in day_div:
                page = page + i

            overlap_day = [0] * 31
            
            for idx in content.index:
            
                color = content['color'][idx]
                title = content['title'][idx].replace('"', "")
                subtext = content['subtext'][idx].replace('"', "")
                day = content['day'][idx]
                
                page = page + """		
                    <section class="task task_""" + str(idx) + """ " >
                        <div style="cursor: pointer;"
                             onClick = "document.getElementById('TextBoxTitle').innerHTML = '""" + title + """';
                                        document.getElementById('TextBoxBody' ).innerHTML = '""" + subtext + """';">""" + title + """
                        </div>
                    </section>
                             
                    <style>
                        .task_""" + str(idx) + """
                        {
                            border-left-color: """ + color + """;
                            color: """ + color + """;
                            background: """ + bg(color) + """;
                            grid-column: """ + str(grid_map[day][1]) + """ / span 1;
                            grid-row: """ + str(grid_map[day][0]) + """;
                            align-self: start;
                            margin-top: """ + str(50 + overlap_day[day]*50) + """px; 
                            box-shadow: 0 10px 14px rgba(71, 134, 255, 0.15);
                            border-radius: 5px;
                            
                            overflow:hidden;
                        }
                        .task_""" + str(idx) + """:hover 
                        { 
                            opacity:0.8;
                        }
                    </style>"""
                    
                
                overlap_day[day] = overlap_day[day] + 1
            
            page = page + """
                    </div>
                </div>
                
                <div class="calendar-container mt-15">
                    <div id="TextBoxTitle" class="calendar-box-title">  dfgdfgdfgdfgdfgdfgdfgdfgdf  </div>
                    <div id="TextBoxBody" class="calendar-box-txt">  dfgdfgdfgdfsdsdfdsfgdfgdfgdfgdfgdf  </div>
                </div>
                        
            </body>
            """

            #Create an HTML file for the full doc menu
            file = open(root_folder + "\\html\calendar_" + str(year) + "_" + str(month) + ".html","w") 
            file.write(page) 
            file.close()

