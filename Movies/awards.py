import pandas as pd
from imdb import Cinemagoer
import numpy as np

# Initialize the IMDb object
ia = Cinemagoer()

def display(list):
    count = 0
    if(list is None):
        return
    for item in list:
        if len(item) > 0:
            count +=1
            print(f"{count}) {item}")
            
path = r"C:\\temp\\github\\act-python\\Jonathan\\Movies\\"
df = pd.read_csv(path + "df_awards.csv")
df = df.iloc[:, 1:] #We remove the first column which is the index
          
count = 0                         
for index, row in df.iterrows():
       
    # We only iterate record with missing Ids
    if(not np.isnan(df['Id'][index])):
        continue
    
    count += 1
    if(count > 5):
        break
    
    movie_name = df['Title'][index].split("---")[0]  
    movie_search_id = 0 if len(df['Title'][index].split("---")) == 1 else df['Title'][index].split("---")[1]
    
    for i in range(0,30):
        try:
            movies = ia.search_movie(movie_name)
            movie_id = movies[int(movie_search_id)].movieID
            movie = ia.get_movie(movie_id)
            runtime = movie.get("runtime")[0]
            break
        except:
            print(f"Could not connect for {movie_name} ({i})")
    
    # Extract required details
    title = movie.get("title")
    year = movie.get("year")
    imdb_rating = movie.get("rating")
    metascore = movie.get("metascore")
    genres = movie.get("genres")
    writers = movie.get("writers")
    directors = [d["name"] for d in movie.get("directors", [])]
    top_cast = [actor["name"] for actor in movie.get("cast", [])[:10]]  # Top 5 billed cast

    print(f": {title} ({year}) Id: {movie_id} Search Id: {movie_search_id}")
    print(f"Search Id: {movie_search_id}")
    print(f"IMDb Rating: {imdb_rating}")
    print("")
    print(f"Directors: ")
    display(directors)
    print("")
    print(f"Top-billed Cast: ")
    display(top_cast)
    print("")
    print(" ################################ ")
    print("")
    
    df.loc[index, 'Id'] = int(movie_id)

    # df['Id'] = df['Id'].astype(int)
    df.to_csv(path + "df_awards.csv")