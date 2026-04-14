#Global modules
import os
import importlib
from imdb import Cinemagoer

#Local modules
import _util
importlib.reload(_util)    
from _util import *

def append_list(row, list, nb):
    output = []
    for i in range(0,nb):
        if(list is None or len(list) <= i):
            output.append("")
        else:
            output.append(list[i])
    return row + output

class Extract:
    def __init__(self, save, max):
        ia = Cinemagoer()

        path = os.getcwd()
        legacy_df = pd.read_csv(path + r"/df_list.csv")
        new_df = pd.read_csv(path + r"/df.csv")
        new_df = new_df.iloc[:, 1:] #We remove the first column which is the index

        for loop, row in enumerate(legacy_df.itertuples(index=False)):
            
            if(loop >= max):
                return
            
            movie_name = row.Name.split("---")[0]  
            movie_search_id = 0 if len(row.Name.split("---")) == 1 else row.Name.split("---")[1]
            jk_rating = row.Rating
            date = row.Date
            movies = ia.search_movie(movie_name)

            for i in range(0,30):
                try:
                    movie_id = movies[int(movie_search_id)].movieID
                    movie = ia.get_movie(movie_id)
                    runtime = movie.get("runtime")[0]
                    break
                except:
                    print(f"Could not connect for {movie_name} {movie_id} ({i})")

            print(f"Written Title: {movie_name}")
                
            # Extract required details
            imdb_rating = movie.get("rating")
            cover = movie.get("cover url")
            genres = movie.get("genres")
            writers = movie.get("writers")
            directors = [d["name"] for d in movie.get("directors", [])]
            top_cast = [actor["name"] for actor in movie.get("cast", [])[:10]]  # Top 5 billed cast
            awards = ""

            title = movie.get("title")
            print(f"Cinemagoer Title: {title}")
            year = movie.get("year")
            print(f"Year: {year}")
            print(f"Runtime: {convert_minutes_to_hours(int(runtime))}")
            print(f"Id: {movie_id}")
            print(f"Search Id: {movie_search_id}")
            print(f"IMDb Rating: {imdb_rating}")
            print(f"Cover: {cover}")
            print("")
            print(f"Directors: ")
            display_list(directors)
            print("")
            print(f"Top-billed Cast: ")
            display_list(top_cast)
            print("")
            print(f"Genres:")
            display_list(genres)
            print("")
            print(f"Writers: ")
            display_list(writers)
            print("")
            print(" ################################ ")
            print("")

            #Generate Df
            base_columns = ['Id', 'Date', 'Name', 'Year', 'JK Rating', 'IMDB Rating', 'Runtime', 'Cover']
            genre_columns =  [f'Genre{i}' for i in range(1, 5 + 1)]
            director_columns =  [f'Director{i}' for i in range(1, 3 + 1)]
            writer_columns =  [f'Writer{i}' for i in range(1, 3 + 1)]
            cast_columns = [f'Cast{i}' for i in range(1, 15 + 1)]
            columns = base_columns + genre_columns + director_columns + writer_columns + cast_columns
            df = pd.DataFrame(columns=columns)

            row = []
            row.append(movie_id)
            row.append(date)
            row.append(title)
            row.append(year)
            row.append(jk_rating)
            row.append(imdb_rating)
            row.append(runtime)
            row.append(awards)
            row.append(cover)
            row = append_list(row, genres, 5)
            row = append_list(row, directors, 3)
            row = append_list(row, writers, 3)
            row = append_list(row, top_cast, 15)

            if(save == True):
                new_df.loc[len(new_df)] = row   
                new_df.to_csv(path + r"/df.csv")