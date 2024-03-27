#python3 -m pip install beautifulsoup4
from bs4 import BeautifulSoup
from statistics import mean
from collections import Counter

#python3 -m pip install requests
import requests
import re

#python3 -m pip install mysql-connector-python
import mysql.connector

#python3 -m pip install pandas
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

#Optionsdd
rtype = 'cast'

#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='u830871656_Online'
                              ,password='Deepunder2!'
                              ,host='191.101.230.1'
                              ,database='u830871656_Online')

mycursor = mydb.cursor()
mycursor.execute("""
                    SELECT
                         ID
                        ,Cast
                        ,Director
                        ,Writer
                        ,Genre
                        ,Rating
                        ,IMDB
                        ,Metacritic
                        ,Movies
                    FROM
                        Tab_Movies
                    WHERE
                        Rating > 0
                    ORDER BY
                        ID ASC
                    LIMIT 500;
                 """)

myresult = mycursor.fetchall() 
mydb.close()

sql_data = pd.DataFrame(myresult)
sql_data.columns = ['ID','cast','director','writer','genre','jk_score','imdb_score','meta_score','movie']

cast_list = []

cast_list_m = []
director_list= []
writer_list = []
genre_list = []

#Create a list including duplicates of all cast, director and writer
sql_field = [rtype] #, 'director', 'writer', 'genre']

for field in sql_field:

    list_name = {}
    d = -1
    master_list_w_dup = []
    master_list_wo_dup = []
    master_list = []
    temp_list = []
    temp_list_m = []
    
    for i in sql_data.index:

        split_temp = sql_data[field][i].split(", ")
        for temp in split_temp:
            if temp != "":
                temp_list.append(temp)
                if i <= len(sql_data) - 80:
                    temp_list_m.append(temp)

    master_list_w_dup.append(temp_list)
    d = d + 1
    list_name[field] = d

    master_list_w_dup.append(temp_list_m)
    d = d + 1
    list_name[field + '_m'] = d

    #Remove duplicated of all the lists
    for key in list_name:

        key_sql = key.replace("_m", "")
        
        c = Counter(master_list_w_dup[list_name[key]])
        temp_unique = []
        temp_count = [] 
        for temp in c:
            temp_unique.append(temp)
            temp_count.append(c[temp])
        temp = pd.DataFrame(list(zip(temp_unique, temp_count)), columns =[key_sql, key + '_count'])
        temp.reset_index(inplace=True)

        master_list_wo_dup.append(temp)

        #Attach information to the list without duplicates
        movie_list = []
        jk_score_mean_list = []
        jk_score_list = []

        temp_list = []
        temp_list = master_list_wo_dup[list_name[key]]

        for i_cast in temp_list.index:
            movies = []
            jk_score = []
            jk_score_str = []
            imdb_score = []
            meta_score = []
            for i_sql in sql_data.index:
                if temp_list[key_sql][i_cast] in sql_data[key_sql][i_sql]:
                    movies.append(sql_data['movie'][i_sql].title())
                    jk_score.append(float(sql_data['jk_score'][i_sql]))
                    jk_score_str.append(str(int(sql_data['jk_score'][i_sql])))
                    imdb_score.append(sql_data['imdb_score'][i_sql])
                    meta_score.append(sql_data['meta_score'][i_sql])
                    
            movie_list.append(", ".join(movies))
            jk_score_list.append(", ".join(jk_score_str))
            jk_score_mean_list.append(round(mean(jk_score),1))
            
        temp_list['jk_score_mean'] = jk_score_mean_list
        temp_list['jk_score'] = jk_score_list
        temp_list['movie'] = movie_list
        temp_list = temp_list.sort_values(by=[key + '_count', 'jk_score_mean'], ascending = (False, False))
        temp_list.reset_index(inplace=True)
        temp_list['rank'] = range(1, len(temp_list) + 1)
        temp_list.to_csv(key +'.csv')
        
        master_list.append(temp_list)




cast = master_list[list_name[rtype]]
castl = master_list[list_name[rtype]]
castr = master_list[list_name[rtype +'_m']]
castr.rename(columns = {'rank':'rank_m'}, inplace = True)

cast = pd.merge(castl,castr[[rtype,'rank_m',rtype + '_m_count']],on=rtype,how='left')
cast.fillna(0, inplace=True)
cast.to_csv('merge.csv')


if rtype == 'cast':
    sql_tab = 'Tab_Actor'
    sql_header_field = 'Actor'
elif rtype == 'director':
    sql_tab = 'Tab_Director'
    sql_header_field = 'Director'
    
sql_update_sql_header = """
    INSERT INTO
        """ + sql_tab + """ (""" + sql_header_field + """, Count_Movie, Count_Movie_m, JKScore_Avg, JKScore_Hist, Movie_List, Rank, Rank_m)
    VALUES"""

#print(cast['rank_m'])

sql_update_sql_record = []
for i in cast.index:
        
    sql_update_sql_record.append("""
                     ('""" + cast[rtype][i].replace("'","")
              + """', '""" + str(cast[rtype + '_count'][i])
              + """', '""" + str(cast[rtype + '_m_count'][i])
              + """', '""" + str(cast['jk_score_mean'][i])
              + """', '""" + cast['jk_score'][i]
              + """', '""" + cast['movie'][i].replace("'","")
              + """', '""" + str(int(cast['rank'][i]))
              + """', '""" + str(int(cast['rank_m'][i]))
              + """')""")

    sql_update_sql = sql_update_sql_header + ", ".join(sql_update_sql_record) + ';'

mydb = mysql.connector.connect(user='u830871656_Online'
                              ,password='Deepunder2!'
                              ,host='191.101.230.1'
                              ,database='u830871656_Online')

mycursor = mydb.cursor()
#print(sql_update_sql)
mycursor.execute("DELETE FROM " + sql_tab)
mydb.commit()
mycursor.execute(sql_update_sql)
mydb.commit()
mydb.close()