import sys
module_path = "/Users/jonathanventuri/Documents/Python/Movies"

if module_path not in sys.path:
    sys.path.append(module_path)

import matplotlib.pyplot as plt
import streamlit as st
import importlib

import class_awards
import class_directors
import class_actors
import class_movies
import class_extract
import streamlit_barchart
import streamlit_divergeplot
import streamlit_ecdf
import streamlit_top10chart
importlib.reload(class_awards)  
importlib.reload(class_directors)  
importlib.reload(class_actors)  
importlib.reload(class_movies)  
importlib.reload(class_extract)  
importlib.reload(streamlit_barchart)  
importlib.reload(streamlit_divergeplot)  
importlib.reload(streamlit_ecdf)  
importlib.reload(streamlit_top10chart)  
from class_awards import *
from class_movies import *
from class_directors import *
from class_actors import *
from class_extract import *
from streamlit_barchart import *
from streamlit_divergeplot import *
from streamlit_ecdf import *
from streamlit_top10chart import *

# Access to the config.toml file
# C:\Users\Jonathan.Venturi\.streamlit

# Shell to run the server manually
# cd Jonathan && cd Movies && py -m streamlit run streamlit_page.py
# cd.. && cd Jonathan && cd Movies && py -m streamlit run streamlit_page.py

# Documentation
# https://docs.streamlit.io/develop/api-reference/text
# https://www.markdownguide.org/basic-syntax/

# @st.cache_data
def load_actors_data(movies):
    return Actors(movies)

# @st.cache_data
def load_movies_data(awards):
    return Movies(awards)

# @st.cache_data
def load_directors_data(movies):
    return Directors(movies)

# @st.cache_data
def load_awards_data():
    return Awards()

awards = load_awards_data()
movies = load_movies_data(awards)
actors = load_actors_data(movies)
directors = load_directors_data(movies)

top_nb = 50
top_actors = actors.top(top_nb)
top_directors = directors.top(top_nb)

# # 🔥❤️⚠️❌
# col1,col2,col3,col4,col5=st.columns(5)
# col1.button(""" 2025 """)
# col2.button("""🏆 **2024** *2/5* """)
# col3.button("""❌ **2023** 0/7""")
# col4.button("""⚠️ **2022** *1/4* """)
# col5.button("""**2021** (2/5)""")
# st.markdown("---")

options=[]
options.append("Home Page")
options.append("Actors by name")
options.append("Actors by top")
options.append("Movies by Name")
options.append("Movies by Year")
options.append("Directors by name")
options.append("Directors by top")
options.append("Awards")

radio_type = st.sidebar.radio(f"Search for:", options=options)

if(radio_type == "Actors by top"):

    options = {}
    for index, actor in enumerate(top_actors):
        options[f"{len(actor.movies)}: {actor.name} ({days_compared_to(actor.movies[-1].date)})"] = actor
    
    selected = st.sidebar.radio(f"### Top {top_nb} actors", options=list(options.keys()), format_func=lambda x: x)
    actor = options[selected]
    actor.print_streamlit()

elif(radio_type == "Actors by name"):
    
    options = {}
    for key, value in actors.dict.items():
        options[f"{key}"] = value
    selected = st.sidebar.selectbox("### Type a name:", options=list(actors.dict.keys()), format_func=lambda x: x)
    actor = options[selected]
    actor.print_streamlit()

elif(radio_type == "Directors by top"):

    options = {}
    for index, directors in enumerate(top_directors):
        options[f"{len(directors.movies)}: {directors.name} ({days_compared_to(directors.movies[-1].date)})"] = directors
    
    selected = st.sidebar.radio(f"### Top {top_nb} directors", options=list(options.keys()), format_func=lambda x: x)
    director = options[selected]
    director.print_container_with_list_of_movies()

elif(radio_type == "Directors by name"):
    
    options = {}
    for key, value in directors.dict.items():
        options[f"{key}"] = value
    selected = st.sidebar.selectbox("### Type a name:", options=list(directors.dict.keys()), format_func=lambda x: x)
    director = options[selected]
    director.print_container_with_list_of_movies()
    
elif(radio_type == "Movies by Name"):

    options = {}
    for key, value in movies.dict.items():
        options[f"{key}"] = value
    
    #Last movie is selected as default
    selected_default_index = len(options)-1
    
    selected = st.sidebar.selectbox("### Type a name:", options=list(movies.dict.keys()), format_func=lambda x: x, index=selected_default_index)
    movie = options[selected]
    movie.print_streamlit([], actors)
    
elif(radio_type == "Movies by Year"):

    options = {}
    for i, (key, value) in enumerate(movies.dict_by_year.items()):
        options[f"{key} ({len(value)}) :grey[{movies.jk_by_year(key)}]"] = value
        
        #The last movie watched is used as default year
        if(movies.last.year == key):
            selected_default_index = i
        
    selected = st.sidebar.radio("### Choose a year:", options=list(options.keys()), format_func=lambda x: x, index=selected_default_index)
    movies_by_selected_year = options[str(selected)]
    
    for movie in movies_by_selected_year:
        movie.print_streamlit(directors)
     
elif(radio_type == "Home Page"): 
    barchart_movies(movies.df)
    divergeplot_movies(movies.df)
    ecdf(movies.df)
    top_imdb_chart(movies.df, 20)
    
elif(radio_type == "Awards"): 
    
    options = {}     
    for i, (key, value) in enumerate(awards.dict_movie_name_by_year.items()):
        movie_count = 0
        movie_seen = 0
        movie_golden_globe_winner_seen = False
        movie_winner_seen = False
        movie_palme_seen = False
        
        for movie_name in value:
            movie = movies.get_movie_by_name(movie_name)
            movie_count += 1
            if movie is not None:
                movie_seen += 1
                if awards.is_winner(movie_name):
                    movie_winner_seen = True
                if awards.is_palme(movie_name):
                    movie_palme_seen = True
                if awards.is_golden_globe(movie_name):
                    movie_golden_globe_winner_seen = True
                
        txt = ('🌿' if movie_palme_seen else '❌') + ' ' +  ('🌍' if movie_golden_globe_winner_seen else '❌') + ' ' + ('🏆' if movie_winner_seen else '❌') + ' ' + str(movie_seen) + "/" + str(movie_count)
        options[f"{int(key)} {txt}"] = key
        
    selected = st.sidebar.radio("### Choose a year:", options=list(options.keys()), format_func=lambda x: x, index=0)
    awards_by_selected_year = options[str(selected)]
    
    awards.print_movies_by_year(movies, awards_by_selected_year)

        
    # for movie_name in awards.movies_not_watched_by_year(awards_by_selected_year):
    #     st.markdown(movie_name)
    