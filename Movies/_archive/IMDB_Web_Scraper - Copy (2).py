#https://bit.ly/2NyxdAG
from bs4 import BeautifulSoup
import requests
import re

#py -m pip install mysql-connector-python
import mysql.connector

#py -m pip install pandas
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)


def curr_conv(money):
    if "EUR" in money:
        return int(money.replace('EUR','')) * 1.19
    elif "KRW" in money:
        return int(money.replace('KRW','')) * 0.000852558
    else:
        return int(money)

    
#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
mycursor.execute("SELECT Movies, Search, Year, Rating FROM Tab_Movies Where Rating > 0 ")
#AND Movies = 'The Old Man & The Gun'
myresult = mycursor.fetchall()
mydb.close()

sql_data = pd.DataFrame(myresult)
sql_data.columns = ['name','search','year','jk_score']

#Fetch the movie title and year, for more accurate search in IMDB
index_name = 0
index_search = 1
index_year = 2
index_rating = 3

for i in sql_data.index:
    if sql_data['search'][i] == '':
        sql_data.at[i,'search'] = sql_data['name'][i] + " (" + sql_data['year'][i] + ")"

print(sql_data)
print('')

##########################################################################################
# Initialize new columns
##########################################################################################
imdb_score_nc = []
meta_score_nc = []
budget_nc = []
revenue_nc = []

error = []

##########################################################################################
# Loop through all the records in the SQL Query
##########################################################################################
imdb_url = 'https://www.imdb.com/'
search_tag  = 'find?q='

for i in sql_data.index:

    print('Search: ' + sql_data['search'][i])

    search_movie = sql_data['search'][i].replace(' ','+')
    url = imdb_url + search_tag + search_movie

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    ##########################################################################################
    #Fetch the first link available from the search
    ##########################################################################################
    links = [a.attrs.get('href') for a in soup.select('td.result_text a')]
    
    try:
        url = imdb_url + links[0]
        print('Url: ' + url)
    except:
        print("No links were found for the search: " + url)
        Error.append('No links were found for the search: ' + url)
        continue
    
    ##########################################################################################
    #Access the movie webpage from the previous search
    ##########################################################################################
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    #print(soup.prettify())
    #break

    ##########################################################################################
    #Fetch Directors and Writers
    ##########################################################################################
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

    ##########################################################################################
    #Fetch the IMDB score from the website
    ##########################################################################################
    imdb_score = soup.find("span", {"class": "rating"}).get_text(strip=True) \
               .replace('/10','')

    imdb_score_nc.append(imdb_score)

    print('IMDB Score: ' + imdb_score)

    ##########################################################################################
    #Fetch the metascore from the website
    ##########################################################################################
    try:
        meta_score = soup.find("div", {"class": "metacriticScore"}) \
                         .get_text(strip=True)
    except:
        meta_score = 'NA'

    meta_score_nc.append(meta_score)
        
    print('Meta Score: ' + meta_score)
    print('JK Score: ' + sql_data['jk_score'][i])

    ##########################################################################################
    #Fetch the full cast (firt billed)
    ##########################################################################################
    full_cast = soup.select('table.cast_list a')
    full_cast_list = []
    for a in full_cast:
        if "name" in a.attrs.get('href'):
            if a.get_text(strip=True) != '':
                full_cast_list.append(a.get_text(strip=True))

    print('Full Cast: ' + ', '.join(full_cast_list))

    ##########################################################################################
    #Fetch the Genres
    ##########################################################################################
    genre = soup.find_all("div", {"class": "see-more inline canwrap"})
    try:
        print('Genre: ' + genre[1].get_text(strip=True)
                              .replace('|', ', ') \
                              .replace('Genre:','') \
                              .replace('Genres:',''))
    except:
        print('Genre: Not Found')

    ##########################################################################################
    #Fetch the Budget
    ##########################################################################################
    boxoffice_soup = soup.select('div.txt-block')

    budget = "0"
    revenue = "0"
    for div in boxoffice_soup:
        div_soup = BeautifulSoup(str(div), "html.parser")
        field_find = str(div_soup.find("h4", {"class": "inline"}))
        if "Budget:" in field_find:
            budget = div.get_text(strip=True) \
                              .replace('Budget:', ', ') \
                              .replace('(estimated)','') \
                              .replace('$','') \
                              .replace(',','')
            
        if "Cumulative Worldwide Gross:" in field_find:
            revenue = div.get_text(strip=True) \
                              .replace('Cumulative Worldwide Gross:', ', ') \
                              .replace('(estimated)','') \
                              .replace('$','') \
                              .replace(',','')
            
    budget_nc.append(curr_conv(budget))
    revenue_nc.append(curr_conv(revenue))
    
    print("Budget: " + budget if curr_conv(budget) != 0 else 'Unknown')
    print("Revenue: " + revenue)
    
    ##########################################################################################
    #Fetch the Budget
    ##########################################################################################

    print('')

print(error)

sql_data['imdb_score'] = imdb_score_nc
sql_data['meta_score'] = meta_score_nc
sql_data['budget'] = budget_nc
sql_data['revenue'] = revenue_nc
sql_data['profit'] = sql_data['revenue'] - sql_data['budget']
sql_data['profit_pc'] = 100 * sql_data['profit'].divide(sql_data['budget'])

print(sql_data)











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

















