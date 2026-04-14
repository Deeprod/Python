import os
os.chdir(r"C:/temp/github/act-python/Jonathan/Movies")

import importlib
import class_actors
import class_movies
import class_extract
importlib.reload(class_actors)  
importlib.reload(class_movies)  
importlib.reload(class_extract)  
from class_actors import *
from class_movies import *
from class_extract import Extract

#This is to allow Ctrl+A and Ctrl+Enter to run the import only
#Then select the relevant rows below and Ctrl+Enter
if(1==0):
    actors = Actors()
    actors.print("Colin Farrell")
    actors.top10()

    Extract(False, 1)

# if(1==0):
    movies = Movies()
    movies.print("The Godfather")
    movies.last.directors
    

if(1==0):
    from imdb import Cinemagoer
    ia = Cinemagoer()

    print(ia.get_popular100_movies())
    print(ia.get_person_filmography())

    ia.search_person() #0000217
    type(ia.get_person_filmography("0000217")) #"Martin Scorsese"


    filmography = ia.get_person_filmography("0000217")["titlesRefs"]
    print(filmography)

    for index, (key, value) in enumerate(filmography.items()):
        print(value.movieID)