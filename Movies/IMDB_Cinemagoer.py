#python3 -m pip install cinemagoer
from imdb import Cinemagoer

# create an instance of the Cinemagoer class
ia = Cinemagoer()


movie_title_for_search = "The Matrix"
movie_year_for_search = 1999

# get a movie
movies_searched = ia.search_movie(movie_title_for_search)
for movie in movies_searched:
    year = movie['year']
    print(sorted(movie.keys()))
    if(year >= movie_year_for_search-1 and year <= movie_year_for_search +1):
        print(movie['title'] + ' ' + str(year))

movie = movies_searched[0]


year = movie['year']
#boxoffice = movie['box office']
cast = movie['cast']
countries = movie['countries']
director = movie['director']
writer = movie['writer']
imdbID = movie['imdbID']
runtimes = movie['runtimes']
top250rank = movie['top250rank']
rating = movie['rating']
genres = movie['genres']

##print(sorted(movie.keys()))