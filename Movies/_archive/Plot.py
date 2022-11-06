from plotnine import *
import adjustText

#py -m pip install mysql-connector-python
import mysql.connector

#py -m pip install plotnine
import pandas as pd
import numpy as np
pd.set_option("display.max_rows", None, "display.max_columns", None)

    
#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
mycursor.execute("SELECT Movies, Rating, IMDB, Metacritic FROM Tab_Movies")
myresult = mycursor.fetchall() 
mydb.close()

sql_data = pd.DataFrame(myresult)
sql_data.columns = ['Name','JK_Score','IMDB_Score','Meta_Score']

sql_data["JK_Score"]   = pd.to_numeric(sql_data["JK_Score"]  ,downcast="integer")
sql_data["JK_Score"]   = sql_data["JK_Score"].astype(object)
sql_data["IMDB_Score"] = pd.to_numeric(sql_data["IMDB_Score"],downcast="float")
sql_data["Meta_Score"] = pd.to_numeric(sql_data["Meta_Score"],downcast="float")/10
sql_data["Name"] = sql_data["Name"].str.title()

sql_data = sql_data[(sql_data.JK_Score > 0) & (sql_data.IMDB_Score > 0) & (sql_data.Meta_Score > 0)]

sql_data_label = sql_data[(sql_data.JK_Score == 9)    \
                        | (sql_data.Name == "The Meg")  \
                        | (sql_data.Name == "Parasite")  \
                        | (sql_data.Name == "Shawshank Redemption")  \
                        | (sql_data.Name == "The First Purge")  \
                        | (sql_data.Name == "Seven Pounds")  \
                        | (sql_data.Name == "The Assistant")  \
                        | (sql_data.Name == "The Dark Tower")  \
                        | (sql_data.Name == "Stowaway")  \
                        | (sql_data.Name == "The Green Mile")  \
                          
                          ]

print(sql_data_label)

#rects <- data.frame(xstart = seq(0,80,20), xend = seq(20,100,20), col = letters[1:5])

print(ggplot(sql_data)              \
          + aes(x="IMDB_Score"      \
               ,y="Meta_Score"      \
               ,xmin=3              \
               ,ymin=3              \
               ,xmax=10.5             \
               ,ymax=10.5             \
               ,color="JK_Score"    \
               ,size=5              \
               ,alpha=0.5)           \
          + theme_bw() \
          #+ geom_rect(data = rects, aes(xmin = xstart, xmax = xend, ymin = -Inf, ymax = Inf, fill = col), alpha = 0.4) 
          + scale_x_continuous(breaks = range(3,11))
          + scale_y_continuous(breaks = range(3,11))
          + geom_point()            \
          + geom_label(aes(label="Name"), nudge_y=0.2, alpha=0.9, data=sql_data_label, size=10)    \
         #+ scale_color_gradient(low="blue",high="red")) \
          + scale_colour_manual(values=["red", "orange", "blue", "green", "purple"])


  
          
     )











