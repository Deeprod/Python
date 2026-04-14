#Global modules
import importlib
import os

#Local modules
import _util
import class_actor 
import class_movie
importlib.reload(_util)    
importlib.reload(class_actor)    
importlib.reload(class_movie) 
from _util import *
from class_actor import *
from class_movie import *

class Actors:
    def __init__(self, movies):
        
        path = os.getcwd()
        self.df = pd.read_csv(path + r"/df.csv")
        self.dict = {}
        
        for movie in movies.dict.values():
            for actor in movie.cast:
                if(pd.isna(actor)):
                    continue
                if actor not in self.dict:
                    self.dict[actor] = Actor(actor)
                self.dict[actor].add(movie)
    
    def print(self, actor_name):
        self.dict[actor_name].print()
        
    def top(self, top):
        list_actor = sorted(self.dict.values(), key=lambda actor: len(actor.movies), reverse=True)[:top]
        return list_actor