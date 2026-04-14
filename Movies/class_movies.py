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

class Movies:
    def __init__(self, awards):
        
        path = os.getcwd()
        self.df = pd.read_csv(path + r"/df.csv")
        self.df_no_date = pd.read_csv(path + r"/df_no_date.csv")
        self.df_combined = pd.concat([self.df_no_date, self.df], axis=0, ignore_index=True)
                                     
        self.dict = {}
        self.dict_by_year = {}
        
        for _, row in self.df_combined.iterrows():
            movie = Movie(row, awards)
            
            if movie.name in self.dict:
                raise ValueError(f"The movie name {movie.name} appears more than once, this will create issues")
            
            #Dictionary movie by name
            self.dict[movie.name] = movie
            self.last = movie
            
            #Dictionary movie by year
            if movie.year not in self.dict_by_year:
                self.dict_by_year[movie.year] = []
            self.dict_by_year[movie.year].append(movie)
            
        #Sort the dictionary by descending order of year
        self.dict_by_year = dict(sorted(self.dict_by_year.items(), key=lambda x: x[0], reverse=True))
    
    def get_movie_by_name(self,movie_name):
        movie = self.dict.get(movie_name)
        # if movie is None:
        #     print(f"Warning: '{movie_name}' not found in 'Movies' dictionary")
        return movie

    def print(self, movie_name):
        self.dict[movie_name].print()
        
    def jk_by_year(self, year):
        return round(sum(v.jk for v in self.dict_by_year[year]) / len(self.dict_by_year[year]),1)
            