import os
import re
import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None)

def page_start(scr):

    scr_style = ""
    if scr == "scroll-bar-no":
        scr_style = """<link href="..\css\style-scroll-bar.css" rel="stylesheet">"""
    
    return """ 
            <!doctype html> 
            <html lang="en"> 

            <head> 
                <meta charset="utf-8" /> 
                <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
                <link href="..\css\style.css" rel="stylesheet">""" + scr_style + """<link href="..\fontawesome\css\all.css" rel="stylesheet">
            </head> 
                
            <body>
            """

def page_end():
    return """
    <script src="../fontawesome/js/all.js"></script>
</body>
</html>
"""

def capsule_start():
    return """<div id="Capsule">"""

def capsule_menu_start():
    return """<div id="Capsule_Menu">"""

def capsule_end():
    return """</div>"""

def category_start():
    return """ <ul class="menu inset mb-1"> """

def menu_item(nb,ref,txt):
    return """
        <li>
            <a href=\"""" + ref + """\" target="right_frame" class="item">
                <div class="icon-box">
                """ + nb + """
                </div>
                """ + txt + """
                <i class="fas fa-chevron-right menu_chevron"></i>
            </a>
        </li>
    """

def category_end():
    return """ </ul> """


def bottom_menu(txt):

    active = ['','']
    if txt == "Menu":
        active = ['active','','','']
    elif txt == "Full":
        active = ['','active','','']
    elif txt == "Calendar":
        active = ['','','active','']
    elif txt == "Admin":
        active = ['','','','active']
        
    return """<br>
    <div class="bottom-menu">
        <a href="menu.html"  class="item """ + active[0] + """\">
            <div class="col">
                <i class="fas fa-bars bottom-menu-icon-""" + active[0] + """\"></i>
                <strong>Menu</strong>
            </div>
        </a>
        <a href="menu_full_doc.html" class="item """ + active[1] + """\">
            <div class="col">
                <i class="fas fa-search bottom-menu-icon-""" + active[1] + """\"></i>
                <strong>Full Documentation</strong>
            </div>
        </a>
        <a href="calendar.html" class="item """ + active[2] + """\">
            <div class="col">
                <i class="far fa-calendar-alt bottom-menu-icon-""" + active[2] + """\"></i>
                <strong>Calendar</strong>
            </div>
        </a>
        <!--
        <a href="admin.html" class="item """ + active[3] + """\">
            <div class="col">
                <i class="fas fa-shield-alt bottom-menu-icon-""" + active[3] + """\"></i>
                <strong>Admin</strong>
            </div>
        </a> 
        -->        
    </div>   
    """


def title(txt):
    return """
        <div class="body-title-1">""" + txt + """</div>
            """

def category_name(txt):
    return """
        <div class="category">""" + txt + """</div>
            """

def body(txt):
    return """
        <div class="body">
            """ + txt + """
        </div>
        <br>
        """

def header_menu(txt):
    return """
    <div class="header">
            """ + txt + """
    </div>
    """

def header(txt):
    return """
    <div class="header">
            """ + txt + """
    </div>
    """

def header_fluid(txt):
    return """
    <div class="header_fluid">
            """ + txt + """
    </div>
    """

def image(txt):
    return """
        <img src=\"""" + txt + """\" alt="" class="img-insert"><br>
            """

def format_txt(txt):

    #Format Links
    txt_array = [p.split(']]')[0] for p in txt.split('[[') if ']]' in p]

    for i in txt_array:
        link = "<a href='" + i + "' target='right_frame'>" + i + "</a>"
        txt = txt.replace("[[" + i + "]]",link)

    #Format Bold
    txt = txt.replace("[b]","<b>")
    txt = txt.replace("[bb]","</b>")

    #Format Italic
    txt = txt.replace("[i]","<i>")
    txt = txt.replace("[ii]","</i>")

    #Format Underline
    txt = txt.replace("[u]","<u>")
    txt = txt.replace("[uu]","</u>")

    #Format Lists
    txt = txt.replace("[ul]","<ul class='w3-ul'><li>")
    txt = txt.replace("[l]","</li><li>")
    txt = txt.replace("[lu]","</ul></li>")
    
    return txt    
    

def page_menu():
    return page_start("scroll-bar-no") + \
           capsule_menu_start() + \
           header_menu("Full Documentation") + \
           category_name("Choose with or without images") + \
           category_start() + \
           menu_item("1","full_doc.html","With Images") + \
           menu_item("1","full_doc_no_img.html","Without Images") + \
           category_end() + \
           bottom_menu("Full") +\
           page_end()
           

 
def build_hub():

    root_folder = r"C:\Users\Jonathan\Google Drive\Python\Control Center\hub"
    directory = root_folder + "\soup"
    s_split = []

    for entry in os.scandir(directory):
        if entry.path.endswith(".txt"):
            f = open(entry.path, "r")
            s_combined = f.read()
            s_split = s_split + s_combined.split("{{end}}")

    df_list = []

    for s in s_split:

        tag = []
        content = []

        for i in range(0,len(s)):
            if s[i:i+2] == '{{' and s[i+5:i+7] == '}}':
                tag.append(s[i+2:i+5])

        if tag == []:
            continue
            
        a = re.sub('{{[^}}]+}}', '{{}}', s)
        for i in a.split('{{}}')[1:]:
            content.append(i.strip())

        for idx,item in enumerate(tag):
            if item == "ref":
                filename = content[idx]
            if item == "cat":
                category = content[idx]
            if item == "hea":
                header_txt = content[idx]
                
        df_list.append([filename,category,header_txt,tag,content]) 


    column_names = ["filename","category","header","tag","content"]
    df = pd.DataFrame(data=df_list,columns=column_names)
    df = df.sort_values(by=['category'])
    df = df.reset_index(drop=True)

    #print(df)

    full_page = page_start("scroll-bar-yes") + capsule_start() + header("Full Documentation")
    full_page_no_img = page_start("scroll-bar-yes") + capsule_start() + header("Full Documentation")

    for i in df.index:

        page = page_start("scroll-bar-yes") + capsule_start()
        
        for idx,item in enumerate(df["tag"][i]):

            block = df["content"][i][idx]
        
            if item == "hea":
                page = page + header(block)
                full_page = full_page + header_fluid(block)
                full_page_no_img = full_page_no_img + header_fluid(block)
            if item == "ttl":
                page = page + title(block)
                full_page = full_page + title(block)
                full_page_no_img = full_page_no_img + title(block)
            if item == "tab":
                page = page + table(block)
                full_page = full_page + table(block)
                full_page_no_img = full_page_no_img + table(block)
            if item == "txt":
                block = format_txt(block)
                page = page + body(block)
                full_page = full_page + body(block)
                full_page_no_img = full_page_no_img + body(block)
            if item == "img":
                page = page + image(block)
                full_page = full_page + image(block)
                
        page = page + capsule_end() + page_end()

        #Print the html document
        file = open(root_folder + "\html\\" + df["filename"][i] + ".html","w") 
        file.write(page) 
        file.close()

    #Print the full documentation
    full_page = full_page + capsule_end() + page_end()
    file = open(root_folder + "\html\\full_doc.html","w") 
    file.write(full_page) 
    file.close()
    full_page_no_img = full_page_no_img + capsule_end() + page_end()
    file = open(root_folder + "\html\\full_doc_no_img.html","w") 
    file.write(full_page_no_img) 
    file.close()

    #Build the menu page
    menu = page_start("scroll-bar-no") + capsule_menu_start() + header_menu("Menu")

    for idx,item in enumerate(df["category"]):

        if idx == 0:
            menu = menu + category_name(item) + category_start()
            cat_count = 0
        elif item != df["category"][idx-1]:
            menu = menu + category_name(item) + category_start()
            cat_count = 0

        cat_count = cat_count + 1
        menu = menu + menu_item(str(cat_count),df["filename"][idx]+".html",df["header"][idx])

        if idx == len(df["category"])-1:
            menu = menu + category_end()
        elif item != df["category"][idx+1]:
            menu = menu + category_end()

    menu = menu + capsule_end() + bottom_menu("Menu") + page_end()

    file = open(root_folder + "\html\\menu.html","w") 
    file.write(menu) 
    file.close()

    #Build the calendar page
    menu = page_start("scroll-bar-no") + capsule_menu_start() + header_menu("Calendar")

    menu = menu + category_name("2021") + category_start()
    menu = menu + menu_item("12","calendar_2021_12.html","December")
    menu = menu + menu_item("11","calendar_2021_11.html","November")
    menu = menu + menu_item("10","calendar_2021_10.html","October")
    menu = menu + menu_item("9","calendar_2021_9.html","September") 
    menu = menu + menu_item("8","calendar_2021_8.html","August")
    menu = menu + menu_item("7","calendar_2021_7.html","July")
    menu = menu + menu_item("6","calendar_2021_6.html","June")
    menu = menu + menu_item("5","calendar_2021_5.html","May")    
    menu = menu + menu_item("4","calendar_2021_4.html","April")
    menu = menu + menu_item("3","calendar_2021_3.html","March")
    menu = menu + menu_item("2","calendar_2021_2.html","February")
    menu = menu + menu_item("1","calendar_2021_1.html","January")
    menu = menu + category_end()

    menu = menu + category_name("2020") + category_start()
    menu = menu + menu_item("12","calendar_2020_12.html","December")
    menu = menu + category_end()

    menu = menu + capsule_end() + bottom_menu("Calendar") + page_end()

    file = open(root_folder + "\html\\calendar.html","w") 
    file.write(menu) 
    file.close()
   
    #Build the calendar page
    menu = page_start("scroll-bar-no") + capsule_menu_start() + header_menu("Admin")

    menu = menu + category_name("Admin Tools") + category_start()
    menu = menu + menu_item("1","calendar_2021_12.html","ral")
    menu = menu + menu_item("2","C:\\Users\\Jonathan\\Google Drive\\Python\\Control Center\\","rub")
    menu = menu + category_end()

    menu = menu + capsule_end() + bottom_menu("Admin") + page_end()

    file = open(root_folder + "\html\\admin.html","w") 
    file.write(menu) 
    file.close()
    
    
    
    #Create an HTML file for the full doc menu
    file = open(root_folder + "\html\\menu_full_doc.html","w") 
    file.write(page_menu()) 
    file.close()







def table(txt):

    tab = pd.read_csv("hub\\csv\\" + txt + ".csv")
    
    width = tab.iloc[0]
    full_width = 0
    
    for i in tab.iloc[0]:
        full_width = full_width + int(i)
    
    print(full_width)
    
    html_txt =  """
        <div class='container-table100' style='width: """ + str(full_width) + """%;'>
            <div class='wrap-table100'>
                <div class='table100'>              
                    <div class='table100-head'>
                        <table class='table-width'>
                            <thead>
                                <tr>"""
    
    #Populate Header
    padding_ind = True
    for count, txt in enumerate(tab.head()):
        html_txt = html_txt + """<th style='width: """ + str(width[count]) + """%; """ + ("""padding-left: 20px;""" if padding_ind else """ """) + """'>""" + txt + """</th>"""
        padding_ind = False
        
    html_txt = html_txt + """                                   
                                </tr>
                            </thead>
                        </table>
                    </div>

                    <div class='table100-body' style='max-height: 400px;'>
                        <table class='table-width'>
                            <tbody>"""
    
    for i in range(1,len(tab.index)):   
    
        html_txt = html_txt + """<tr>"""
         
        padding_ind = True       
        for count, txt in enumerate(tab.iloc[i]):
                        
            html_txt = html_txt + """<td style='width: """ + str(width[count]) + """%; """ + ("""padding-left: 20px;""" if padding_ind else """ """) + """'>""" + str(txt) + """</td>"""
            padding_ind = False  
            
        html_txt = html_txt + """</tr>"""

                
    html_txt = html_txt + """                             
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <br>
        """
    
    return html_txt
