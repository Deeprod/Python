#Global modules
import importlib

#Local modules
import _util
import class_movies
import class_movie
importlib.reload(_util)    
importlib.reload(class_movies)
importlib.reload(class_movie) 
from _util import *
from class_movies import *
from class_movie import *

class Awards:
    def __init__(self):
        
        path = os.getcwd()
        self.df = pd.read_csv(path + r"/df_awards.csv")
        self.dict_movie_name_by_year = {}
        self.list_movie_name = []
        self.list_oscar_nominee_movie_name = []
        self.list_oscar_winner_movie_name = []
        self.list_golden_globe_winner_movie_name = []
        self.list_palme_dor_movie_name = []
        
        for index, row in self.df.iterrows():
            movie_name = row.Name
            movie_year = row.Year
            movie_award = row.Award
            movie_outcome = row.Outcome

            if movie_year not in self.dict_movie_name_by_year:
                self.dict_movie_name_by_year[movie_year] = []
            
            if movie_name not in self.dict_movie_name_by_year[movie_year]:
                self.dict_movie_name_by_year[movie_year].append(movie_name)
                self.list_movie_name.append(movie_name)
                
            if 'Oscar' in movie_award:
                if movie_outcome == "Winner":
                    self.list_oscar_winner_movie_name.append(movie_name)
                else:
                    self.list_oscar_nominee_movie_name.append(movie_name)
                    
            if 'Golden Globe' in movie_award:
                if movie_outcome == "Winner":
                    self.list_golden_globe_winner_movie_name.append(movie_name)
                    
            if 'Palme' in movie_award:
                self.list_palme_dor_movie_name.append(movie_name)
                
                
    def list_movie_names_for_year(self, year):
        return self.dict_movie_name_by_year[year]
    
    def is_nominee(self, movie_name):
        return movie_name in self.list_oscar_nominee_movie_name
    
    def is_winner(self, movie_name):
        return movie_name in self.list_oscar_winner_movie_name

    def is_golden_globe(self, movie_name):
        return movie_name in self.list_golden_globe_winner_movie_name
    
    def is_palme(self, movie_name):
        return movie_name in self.list_palme_dor_movie_name
     
    def print_movies_by_year(self, movies, year):
        for movie_name in self.list_movie_names_for_year(year):
            movie = movies.get_movie_by_name(movie_name)
            if movie is not None:
                movie.print_streamlit()
            else:
                with st.container(border=True):
                    col1, col2 = st.columns([8, 1])

                    with col1:
                        st.markdown(f":red[{movie_name}]")