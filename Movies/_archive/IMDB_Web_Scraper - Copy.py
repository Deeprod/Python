#https://bit.ly/2NyxdAG
from bs4 import BeautifulSoup
import requests
import re

#py -m pip install mysql-connector-python
import mysql.connector

#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
mycursor.execute("SELECT Movies, Search, Year, Rating FROM Tab_Movies")
myresult = mycursor.fetchall()
mydb.close()

#Fetch the movie title and year, for more accurate search in IMDB
movie_title = []

index_name = 0
index_search = 1
index_year = 2
index_rating = 3

for x in range(15):
    if myresult[x][index_name] != myresult[x][index_search]:
        movie_title.append(myresult[x][index_search])
    else:
        movie_title.append(myresult[x][index_name] + " (" + myresult[x][index_year] + ")")

print(movie_title)

# Download IMDB's Top 250 data
imdb_url = 'https://www.imdb.com/'
search_tag  = 'find?q='

for movie in movie_title:

    print(movie)

    search_movie = movie.replace(' ','+')
    url = imdb_url + search_tag + search_movie

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    #Fetch the first link available from the search
    links = [a.attrs.get('href') for a in soup.select('td.result_text a')]
    #print(links)
    try:
        url = imdb_url + links[0]
    except:
        print("No links were found for the search: " + url)
        continue

    #Access the movie webpage from the previous search
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    #Fetch Directors and Writers
    director_writer = soup.find_all("div", {"class": "credit_summary_item"})
        
    director = director_writer[0].get_text(strip=True) \
               .replace('Directors:','') \
               .replace('Director:','') \
               .split(',') \

    director = ', '.join(director)
        
    print('Director(s): ' + director)

    writer = director_writer[1].get_text(strip=True) \
               .replace('Writer:','') \
               .replace('Writers:','') \
               .split(',') \

    writer = ', '.join(writer)
        
    print('Writer(s): ' + writer)

    #Fetch the IMDB from the website   
    imdb_score = soup.find("span", {"class": "rating"}).get_text(strip=True) \
               .replace('/10','') \
               .split(',') \

    imdb_score = ', '.join(imdb_score)

    print('IMDB Score: ' + imdb_score)

    #Fetch the metascore from the website
    try:
        meta_score = soup.find("div", {"class": "metacriticScore"}) \
                         .get_text(strip=True)
    except:
        meta_score = 'NA'
        
    print('Meta Score: ' + meta_score)

    print('')














#print(soup.prettify())
#crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
#ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
#votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]
#
#imdb = []
#
## Store each item into dictionary (data), then put those into a list (imdb)
#for index in range(0, len(movies)):
#    # Seperate movie into: 'place', 'title', 'year'
#    movie_string = movies[index].get_text()
#    movie = (' '.join(movie_string.split()).replace('.', ''))
#    movie_title = movie[len(str(index))+1:-7]
#    year = re.search('\((.*?)\)', movie_string).group(1)
#    place = movie[:len(str(index))-(len(movie))]
#    data = {"movie_title": movie_title,
#            "year": year,
#            "place": place,
#            "star_cast": crew[index],
#            "rating": ratings[index],
#            "vote": votes[index],
#            "link": links[index]}
#    imdb.append(data)
#
#for item in imdb:
#    print(item['place'], '-', item['movie_title'], '('+item['year']+') -', 'Starring:', item['star_cast'])
