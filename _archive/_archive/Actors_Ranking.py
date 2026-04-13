#https://bit.ly/2NyxdAG
from bs4 import BeautifulSoup
from statistics import mean
from collections import Counter

import requests
import re

#py -m pip install mysql-connector-python
import mysql.connector

#py -m pip install pandas
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

   
#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

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
director_list= []
writer_list = []
genre_list = []

#Create a list including duplicates of all cast, director and writer
for i in sql_data.index:
    
    split_cast = sql_data['cast'][i].split(", ")
    for i_cast in split_cast:
        if i_cast != "":
            cast_list.append(i_cast)

    split_director = sql_data['director'][i].split(", ")
    for i_director in split_director:
        if i_director != "":
            director_list.append(i_director)
        
    split_writer = sql_data['writer'][i].split(", ")
    for i_writer in split_writer:
        if i_writer != "":
            writer_list.append(i_writer)

    split_genre = sql_data['genre'][i].split(", ")
    for i_genre in split_genre:
        if i_genre != "":
            genre_list.append(i_genre)
        
#Remove duplicated of all the lists
c = Counter(cast_list)
cast_unique = []
cast_count = [] 
for cast in c:
    cast_unique.append(cast)
    cast_count.append(c[cast])
cast = pd.DataFrame(list(zip(cast_unique, cast_count)), columns =['cast', 'cast_count']).sort_values(by='cast_count', ascending=False)
cast.reset_index(inplace=True)

c = Counter(director_list)
director_unique = []
director_count = [] 
for director in c:
    director_unique.append(director)
    director_count.append(c[director])
director = pd.DataFrame(list(zip(director_unique, director_count)), columns =['director', 'director_count']).sort_values(by='director_count', ascending=False)
director.reset_index(inplace=True)

c = Counter(writer_list)
writer_unique = []
writer_count = [] 
for writer in c:
    writer_unique.append(writer)
    writer_count.append(c[writer])
writer = pd.DataFrame(list(zip(writer_unique, writer_count)), columns =['writer', 'writer_count']).sort_values(by='writer_count', ascending=False)
writer.reset_index(inplace=True)

c = Counter(genre_list)
genre_unique = []
genre_count = [] 
for genre in c:
    genre_unique.append(genre)
    genre_count.append(c[genre])
genre = pd.DataFrame(list(zip(genre_unique, genre_count)), columns =['genre', 'genre_count']).sort_values(by='genre_count', ascending=False)
genre.reset_index(inplace=True)





#Cast
movie_list = []
jk_score_mean_list = []
jk_score_list = []

for i_cast in cast.index:
    movies = []
    jk_score = []
    jk_score_str = []
    imdb_score = []
    meta_score = []
    for i_sql in sql_data.index:
        if cast['cast'][i_cast] in sql_data['cast'][i_sql]:
            movies.append(sql_data['movie'][i_sql].title())
            jk_score.append(float(sql_data['jk_score'][i_sql]))
            jk_score_str.append(str(int(sql_data['jk_score'][i_sql])))
            imdb_score.append(sql_data['imdb_score'][i_sql])
            meta_score.append(sql_data['meta_score'][i_sql])
            
    movie_list.append(", ".join(movies))
    jk_score_list.append(", ".join(jk_score_str))
    jk_score_mean_list.append(round(mean(jk_score),1))

cast['jk_score_mean'] = jk_score_mean_list
cast['jk_score'] = jk_score_list
cast['movie'] = movie_list
cast.to_csv('cast.csv')




sql_update_sql_header = """
    INSERT INTO
        Tab_Actor (Actor, Count_Movie, JKScore_Avg, JKScore_Hist, Movie_List)
    VALUES"""

sql_update_sql_record = []
for i in cast.index:
        
    sql_update_sql_record.append("""
        ('""" + cast['cast'][i].replace("'","") + """', '""" + str(cast['cast_count'][i]) + """', '""" + str(cast['jk_score_mean'][i]) + """', '""" + cast['jk_score'][i] + """', '""" + cast['movie'][i].replace("'","") + """')""")

sql_update_sql = sql_update_sql_header + ", ".join(sql_update_sql_record) + ';'

mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
print(sql_update_sql)
mycursor.execute("DELETE FROM Tab_Actor")
mydb.commit()
mycursor.execute(sql_update_sql)
mydb.commit()
mydb.close()








#Director
movie_list = []
jk_score_mean_list = []
jk_score_list = []

for i_director in director.index:
    movies = []
    jk_score = []
    jk_score_str = []
    imdb_score = []
    meta_score = []
    for i_sql in sql_data.index:
        if director['director'][i_director] in sql_data['director'][i_sql]:
            movies.append(sql_data['movie'][i_sql].title())
            jk_score.append(float(sql_data['jk_score'][i_sql]))
            jk_score_str.append(str(int(sql_data['jk_score'][i_sql])))
            imdb_score.append(sql_data['imdb_score'][i_sql])
            meta_score.append(sql_data['meta_score'][i_sql])
            
    movie_list.append(", ".join(movies))
    jk_score_list.append(", ".join(jk_score_str))
    jk_score_mean_list.append(round(mean(jk_score),1))

director['jk_score_mean'] = jk_score_mean_list
director['jk_score'] = jk_score_list
director['movie'] = movie_list
director.to_csv('director.csv')









#Writer
movie_list = []
jk_score_mean_list = []
jk_score_list = []

for i_writer in writer.index:
    movies = []
    jk_score = []
    jk_score_str = []
    imdb_score = []
    meta_score = []
    for i_sql in sql_data.index:
        if writer['writer'][i_writer] in sql_data['writer'][i_sql]:
            movies.append(sql_data['movie'][i_sql].title())
            jk_score.append(float(sql_data['jk_score'][i_sql]))
            jk_score_str.append(str(int(sql_data['jk_score'][i_sql])))
            imdb_score.append(sql_data['imdb_score'][i_sql])
            meta_score.append(sql_data['meta_score'][i_sql])
            
    movie_list.append(", ".join(movies))
    jk_score_list.append(", ".join(jk_score_str))
    jk_score_mean_list.append(round(mean(jk_score),1))

writer['jk_score_mean'] = jk_score_mean_list
writer['jk_score'] = jk_score_list
writer['movie'] = movie_list
writer.to_csv('writer.csv')



#Genre
movie_list = []
jk_score_mean_list = []
jk_score_list = []

for i_genre in genre.index:
    movies = []
    jk_score = []
    jk_score_str = []
    imdb_score = []
    meta_score = []
    for i_sql in sql_data.index:
        if genre['genre'][i_genre] in sql_data['genre'][i_sql]:
            movies.append(sql_data['movie'][i_sql].title())
            jk_score.append(float(sql_data['jk_score'][i_sql]))
            jk_score_str.append(str(int(sql_data['jk_score'][i_sql])))
            imdb_score.append(sql_data['imdb_score'][i_sql])
            meta_score.append(sql_data['meta_score'][i_sql])
            
    movie_list.append(", ".join(movies))
    jk_score_list.append(", ".join(jk_score_str))
    jk_score_mean_list.append(round(mean(jk_score),1))

genre['jk_score_mean'] = jk_score_mean_list
genre['jk_score'] = jk_score_list
genre['movie'] = movie_list
genre.to_csv('genre.csv')
