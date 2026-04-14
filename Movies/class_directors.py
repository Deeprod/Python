#Global modules
import importlib
import os

#Local modules
import _util
import class_director
import class_movie
importlib.reload(_util)    
importlib.reload(class_director)    
importlib.reload(class_movie) 
from _util import *
from class_director import *
from class_movie import *

class Directors:
    def __init__(self, movies):
        
        path = os.getcwd()
        self.df = pd.read_csv(path + r"/df.csv")
        self.dict = {}
        
        for movie in movies.dict.values():
            for director in movie.director_names:
                if(pd.isna(director)):
                    continue
                if director not in self.dict:
                    self.dict[director] = Director(director)
                self.dict[director].add(movie)
    
    def print(self, name):
        self.dict[name].print()
        
    def top(self, top):
        list_director = sorted(self.dict.values(), key=lambda actor: len(actor.movies), reverse=True)[:top]
        return list_director