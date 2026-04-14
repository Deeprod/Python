import importlib
import streamlit as st
import _util
import class_actor
importlib.reload(_util)    
importlib.reload(class_actor)   
from _util import *
from class_actor import *

class Movie:
    def __init__(self, row, awards):
        self.date = row['Date'] 
        self.name = row["Name"]
        self.year = row["Year"]
        self.jk = row["JK Rating"]
        self.imdb = row["IMDB Rating"]
        self.runtime = row["Runtime"]
        self.cast = []
        self.genres = []
        self.director_names = []
        self.writers = []
        self.is_nominee = awards.is_nominee(self.name)
        self.is_winner = awards.is_winner(self.name)
        self.is_palme = awards.is_palme(self.name)
        self.is_golden_globe = awards.is_golden_globe(self.name)
        
        for i in range(0,15):
            cast = row['Cast' + str(i+1)]
            if isinstance(cast, str):
                self.cast.append(cast)
            
        for i in range(0,3):
            director = row['Director' + str(i+1)]
            if isinstance(director, str):
                self.director_names.append(director)
            
        for i in range(0,3):
            writer = row['Writer' + str(i+1)]
            if isinstance(writer, str):
                self.writers.append(writer)
            
        for i in range(0,5):
            genre = row['Genre' + str(i+1)]
            self.genres.append(genre)
                
    def print(self):
        print(f"Name: {self.name}")
        print(f"Year:{self.year}")
        print(f"Runtime: {convert_minutes_to_hours(int(self.runtime))}")
        print(f"IMDb Rating: {self.imdb}")
        print(f"JK Rating: {self.jk}")
        print(f"Cover: {self.cover}")
        print("")
        print(f"Genres:")
        display_list(self.genres)
        print("")
        print(f"Directors: ")
        display_list(self.directors)
        print("")
        print(f"Writers: ")
        display_list(self.writers)
        print("")
        print(f"Top-billed Cast: ")
        display_list(self.cast)
        print("")
        print(" ################################ ")
        print("")
    
    def print_awards(self):
        return f"{'🌿' if self.is_palme else ''}{'🌍' if self.is_golden_globe else ''}{'🏆' if self.is_winner else ''}{'🏅' if self.is_nominee else ''}"

        
    def print_streamlit(self, directorss = [], actors = []):
        with st.container(border=False):
            # col1, col2 = st.columns([8, 1])

            # with col1:
            st.markdown(f"##### {self.print_awards()} {self.name} {jk_color_theme(self.jk)} :grey[({self.year})] :grey[{self.imdb}] :grey[{convert_minutes_to_hours(self.runtime)}]")
            # st.markdown(f"##### ")
            
            if directorss:
                for director_name in self.director_names:
                    director = directorss.dict[director_name]
                    expander = st.expander(str(director_name) + " (" + str(len(director.movies)) + ")")
                    expander.markdown(director.string_list_of_movies(header = False))  
            else:
                # st.markdown(f"""##### {self.name}""")
                st.markdown(f"**{', '.join([str(item) for item in self.director_names if item])}**")
                # st.markdown(f"**{', '.join([str(item) for item in self.directors if item])}**, :grey[{', '.join([str(item) for item in self.writers if item])}]")

            # with col2:
                
            
            if actors:           
                for _, actor in enumerate(self.cast):
                    if pd.isna(actor):
                        continue
                    actor = actors.dict[actor]
                    actor.print_streamlit()
                    
        st.markdown("")
                
