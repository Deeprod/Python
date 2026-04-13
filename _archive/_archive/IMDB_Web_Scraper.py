#https://bit.ly/2NyxdAG
from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.set_option("display.max_rows", None, "display.max_columns", None)  

##########################################################################################
# Initialize new columns
##########################################################################################
imdb_score_nc = []
meta_score_nc = []
budget_nc = []
revenue_nc = []
cast_nc = []
director_nc = []
writer_nc = []
genre_nc = []

error = []
error_oscar_cat = []
error_oscar_out = []

##########################################################################################
# Loop through all the records in the SQL Query
##########################################################################################
imdb_url = 'https://www.imdb.com/'
imdb_search = 'find?q='
rotten_url = 'https://www.rottentomatoes.com/'
rotten_search = 'search?search='

movie_name = "A simple favour"
search_movie = "A simple favour 2018"

##########################################################################################
# Rotten Tomatoes URL
##########################################################################################

url = rotten_url + rotten_search + search_movie
print(url)
response = requests.get(url)
rotten_soup = BeautifulSoup(response.text, "html.parser")
rotten_soup_find_type = rotten_soup.find(attrs={'type': 'movie'})
rotten_soup_find_class = rotten_soup_find_type.find(attrs={'class': 'unset'})
links = rotten_soup_find_class.attrs.get('href')
print(links)

try:
    url = links
    print('Rotten Tomatoes url: ' + str(url))
except:
    print("No links were found for the search on Rotten Tomatoes: " + str(url))

print("")

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

##########################################################################################
#Fetch Directors and Writers
##########################################################################################
movie_info = soup.find_all("li", {"class": "meta-row clearfix"})

print("Movie Info:")
for mi in movie_info:
    print("  " + mi.get_text(strip=True))

print("") 
for mi in movie_info:
    mit = mi.get_text(strip=True).strip()
    #print(mit)
    
    if "Writer:" in mit:
        writer = mit.replace("Writer:", "")
        writer = writer.split(",")
        writer = ", ".join(writer)
        writer_nc.append(writer)
        print("Writer:")
        print("  " + writer)

    if "Director:" in mit:
        director = mit.replace("Director:", "")
        director = director.split(",")
        director = ", ".join(director)
        director_nc.append(director)
        print("Director:")
        print("  " + director)

    if "Genre:" in mit:
        genre = mit.replace("Genre:", "")
        genre = genre.split(",")
        genre = [g.strip() for g in genre]
        genre = ", ".join(genre)
        genre_nc.append(genre)
        print("Genre:")
        print("  " + genre)

##########################################################################################
#Fetch the full cast (firt billed)
##########################################################################################
full_cast = soup.find_all("span", {"class": "characters subtle smaller"})
full_cast_trim = []

print("Cast:")
for fc in full_cast:
    actor_role = fc.get_text(strip=True)
    actor_name = fc.attrs.get('title')

    if actor_role == "Director":
        break
    
    full_cast_trim.append(actor_name)
    print("  " + actor_name)

cast_nc.append(', '.join(full_cast_trim))