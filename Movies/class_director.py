import streamlit as st
import importlib
import _util
importlib.reload(_util)    
from _util import *

class Director:
    def __init__(self, name):
        self.name = name
        self.movies = []
        
    def add(self, movie):
        self.movies.append(movie)
        
    def avg_jk(self):
        return round(sum(movie.jk for movie in self.movies) / len(self.movies),1)

    def avg_imdb(self):
        return round(sum(movie.imdb for movie in self.movies) / len(self.movies),1)
    
    def print(self):
        print(f"Name: {self.name}")
        print("Movies:")
        count = 1
        for movie in self.movies:
            print(f"{count}) {movie.name} (JK:{movie.jk})  (IMDB:{movie.imdb})")
            count += 1
        print(f"Average JK rating: {self.avg_jk()}")
        print(f"Average IMDB rating: {self.avg_imdb()}")
        
    def print_container_with_list_of_movies(self):
        with st.container(border=True):
            st.markdown(self.string_list_of_movies())
            
    def string_list_of_movies(self, header = True):
        s = ""
        
        if header:
            s += f"""##### {self.name}
"""
        for movie in self.movies:
            s += (f"""-  {':grey[00/00/0000]' if movie.date == '?' else movie.date} **{jk_color_theme(movie.jk)}** ({movie.year}) {movie.imdb} --- {movie.print_awards()} {movie.name} 
""")
        s += """
"""
        return s