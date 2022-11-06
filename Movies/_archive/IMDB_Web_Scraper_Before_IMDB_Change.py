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
    elif "CAD" in money:
        return int(money.replace('CAD','')) * 0.78
    elif "JPY" in money:
        return int(money.replace('JPY','')) * 0.0096
    elif "GBP" in money:
        return int(money.replace('GBP','')) * 1.4
    elif "MVR" in money:
        return int(money.replace('MVR','')) * 0.065
    else:
        return int(money)

def oscar_cat_acr(cat):
    best_actor = []
    best_actor.append("Best Performance by an Actor in a Leading Role")
    best_actor.append("Best Actor in a Leading Role")

    best_sup_actor = []
    best_sup_actor.append("Best Performance by an Actor in a Supporting Role")
    best_sup_actor.append("Best Actor in a Supporting Role")
    
    best_actress = []
    best_actress.append("Best Performance by an Actress in a Leading Role")
    best_actress.append("Best Actress in a Leading Role")

    best_sup_actress = []
    best_sup_actress.append("Best Performance by an Actress in a Supporting Role")
    best_sup_actress.append("Best Actress in a Supporting Role")

    best_cinematography = []
    best_cinematography.append("Best Achievement in Cinematography")
    best_cinematography.append("Best Cinematography")
    
    best_adapted_screenplay = []
    best_adapted_screenplay.append("Best Adapted Screenplay")
    best_adapted_screenplay.append("Best Writing, Screenplay Based on Material Previously Produced or Published")
    best_adapted_screenplay.append("Best Writing, Adapted Screenplay")
    
    best_original_screenplay = []
    best_original_screenplay.append("Best Original Screenplay")
    best_original_screenplay.append("Best Writing, Original Screenplay")
    
    best_editing = []
    best_editing.append("Best Achievement in Film Editing")
    best_editing.append("Best Film Editing")

    best_music_orginal_score = []
    best_music_orginal_score.append("Best Music, Original Dramatic Score")
    best_music_orginal_score.append("Best Music, Original Score")
    best_music_orginal_score.append("Best Achievement in Music Written for Motion Pictures (Original Score)")

    best_costume = []
    best_costume.append("Best Achievement in Costume Design")
    
    best_movie = []
    best_movie.append("Best Motion Picture of the Year")

    best_sound = []
    best_sound.append("Best Achievement in Sound Mixing")
    best_sound.append("Best Achievement in Sound Editing")

    best_song = []
    best_song.append("Best Achievement in Music Written for Motion Pictures (Original Song)")
    best_song.append("Best Music, Original Song")

    best_makeup = []
    best_makeup.append("Best Makeup")

    best_doco = []
    best_doco.append("Best Documentary Feature")
    
    if cat in best_actor:
        return "A"
    elif cat in best_sup_actor:
        return "a"
    elif cat in best_actress:
        return "B"
    elif cat in best_sup_actress:
        return "b"
    elif cat in best_cinematography:
        return "C"
    elif cat in best_costume:
        return "Co"
    elif cat == "Best Achievement in Directing":
        return "D"
    elif cat in best_doco:
        return "Do"
    elif cat in best_editing:
        return "E"
    elif cat == "Best International Feature Film":
        return "I"
    elif cat in best_movie:
        return "M"
    elif cat in best_music_orginal_score:
        return "Mo"
    elif cat in best_makeup:
        return "Mu"
    elif cat == "Best Achievement in Production Design":
        return "P"
    elif cat in best_adapted_screenplay:
        return "s"
    elif cat in best_original_screenplay:
        return "S"
    elif cat in best_sound:
        return "So"
    else:
        return "Z"

def oscar_outcome_acr(outc):
    if outc == "Winner":
        return "W"
    elif outc == "Nominee":
        return "N"
    else:
        return "Z"
    
    
#Fetch data from the SQL Database
mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
mycursor.execute("SELECT Movies, Search, Year, Rating FROM Tab_Movies Where ID = 106")
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
cast_nc = []
director_nc = []
writer_nc = []
genre_nc = []
oscar_nc = []

error = []
error_oscar_cat = []
error_oscar_out = []

##########################################################################################
# Loop through all the records in the SQL Query
##########################################################################################
imdb_url = 'https://www.imdb.com/'
search_tag  = 'find?q='

for i in sql_data.index:

    print('')
    print('Search: ' + sql_data['search'][i])
    movie_name = sql_data['search'][i]
    
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

    print("")
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
    #director_writer = soup.find_all("div", {"class": "credit_summary_item"})
    director_writer = soup.find_all("li", {"class": "ipc-metadata-list__item"})

    director = ",".join(director_writer[0].strings)
    director = director.split(",")
    director = director[1:]
    director = ", ".join(director)   
    director_nc.append(director)

    writer = ",".join(director_writer[1].strings)
    writer = writer.split(",")
    writer = writer[1:]
    writer = ", ".join(writer)   
    writer_nc.append(writer)
    
    print('Director(s): ' + director)
    print('Writer(s): ' + writer)
    print('')
    
    ##########################################################################################
    #Fetch the IMDB score from the website
    ##########################################################################################
    imdb_score = soup.find_all("a", {"aria-label": "View User Ratings"})         
    imdb_score = imdb_score[0].get_text(strip=True)
    imdb_score = imdb_score[:imdb_score.find("/10")]
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
    print('')
    
    ##########################################################################################
    #Fetch the full cast (firt billed)
    ##########################################################################################
    full_cast = soup.find_all("section", {"class": "ipc-page-section"})
    full_cast = ",".join(full_cast[4].strings)
    full_cast = full_cast[full_cast.find("Edit,"):full_cast.find(",Director")]
    full_cast = full_cast.split(",")

    full_cast_trim = []
    for fc in range(len(full_cast)):
        if fc % 3 == 1:
            full_cast_trim.append(full_cast[fc])
            
    cast_nc.append(', '.join(full_cast_trim))
    print('Full Cast: ' + ', '.join(full_cast_trim))
    print('')

    #full_cast = soup.select('table.cast_list a')
    #full_cast_list = []
    #for a in full_cast:
    #    if "name" in a.attrs.get('href'):
    #        if a.get_text(strip=True) != '':
    #            full_cast_list.append(a.get_text(strip=True))

    #cast_nc.append(', '.join(full_cast_list))
    #print('Full Cast: ' + ', '.join(full_cast_list))
    #print('')
    
    ##########################################################################################
    #Fetch the Genres
    ##########################################################################################
    genre_soup = soup.find_all("div", {"class": "see-more inline canwrap"})
    try:
        genre = genre_soup[1].get_text(strip=True) \
                              .replace('|', ', ') \
                              .replace('Genre:','') \
                              .replace('Genres:','')
    except:
        genre = ''

    genre_nc.append(genre)
    print('Genre: ' + genre)
    
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
    
    print("Budget: " + budget if curr_conv(budget) != 0 else 'Budget: Unknown')
    print("Revenue: " + revenue)
    print('')
    
    ##########################################################################################
    #Fetch Awards
    ##########################################################################################
    url_award = url + "awards?ref_=tt_awd"

    response = requests.get(url_award)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())

    award_name = []
    award_out = []
    award_cat = []
    
    award_outcome_soup = soup.find_all("td", {"class": "title_award_outcome"})
    for aw in award_outcome_soup:

        #Need to convert the outcome of the soup find_all to str for it to work
        s = str(aw)
        
        pattern = "rowspan=\"" + "(.*?)" + "\">"
        aw_nb = int(re.search(pattern, s).group(1))

        pattern = "<b>" + "(.*?)" + "</b>"
        aw_out = re.search(pattern, s).group(1)

        pattern = "<span class=\"award_category\">" + "(.*?)" + "</span>"
        aw_name = re.search(pattern, s).group(1)

        for i in range(aw_nb):
            award_name.append(aw_name)
            award_out.append(aw_out)
  
    award_description_soup = soup.find_all("td", {"class": "award_description"})
    for aw in award_description_soup:

        #Need to convert the outcome of the soup find_all to str for it to work
        #Also need to remove the return to line
        s = str(aw).replace('\r', '').replace('\n', '')

        try:
            pattern = "<td class=\"award_description\">" + "(.*?)" + "<br"
            aw_cat = re.search(pattern, s).group(1).strip()
            award_cat.append(aw_cat)
        except:
            print("Issues in retrieving some award Info")


    #print(len(award_name))
    #print(len(award_cat))
    award = pd.DataFrame(list(zip(award_name, award_out, award_cat)), columns =['Name', 'Outcome', 'Category'])

    #Special treattment for oscards only
    award_oscar = award[award["Name"] == "Oscar"]
    print(award_oscar)
    
    oscar_sql_data = []
    for a in award_oscar.index:
        acr_cat = oscar_cat_acr(award_oscar["Category"][a])
        acr_outcome = oscar_outcome_acr(award_oscar["Outcome"][a])
        oscar_sql_data.append(acr_cat + ":" + acr_outcome)

        if acr_cat == "Z":
            error_oscar_cat.append(movie_name + ":" + award_oscar["Category"][a])
        if acr_outcome == "Z":
            error_oscar_out.append(movie_name + ":" + award_oscar["Outcome"][a])

    oscar_sql_data = '/'.join(oscar_sql_data)
    oscar_nc.append(oscar_sql_data)
    print(oscar_sql_data)

print('')
print("General Error:")
print(error)
print('')
print("Oscar Error:")
print(error_oscar_cat)
print(error_oscar_out)
print('')

sql_data['director'] = director_nc
sql_data['writer'] = writer_nc
sql_data['cast'] = cast_nc
sql_data['genre'] = genre_nc
sql_data['imdb_score'] = imdb_score_nc
sql_data['meta_score'] = meta_score_nc
sql_data['budget'] = budget_nc
sql_data['revenue'] = revenue_nc
sql_data['profit'] = sql_data['revenue'] - sql_data['budget']
sql_data['profit_pc'] = 100 * sql_data['profit'].divide(sql_data['budget'])
sql_data['oscar'] = oscar_nc

#print(sql_data)

##########################################################################################
#Update SQL Database
##########################################################################################

mydb = mysql.connector.connect(user='joxsrbmy_WPFE6'
                              ,password='qwe123QWE,./qq'
                              ,host='162.241.30.119'
                              ,database='joxsrbmy_WPFE6')

mycursor = mydb.cursor()
print('')
for i in sql_data.index:
    sql_query = "UPDATE Tab_Movies SET " + \
                                             "Director='" + sql_data['director'][i].replace('\'','\'\'') + "'" + \
                                             ",Writer='" + sql_data['writer'][i].replace('\'','\'\'') + "'" + \
                                             ",Cast='" + sql_data['cast'][i].replace('\'','\'\'') + "'" \
                                             ",IMDB='" + sql_data['imdb_score'][i] + "'" \
                                             ",Metacritic='" + sql_data['meta_score'][i] + "'" \
                                             ",Genre='" + sql_data['genre'][i].replace('\'','\'\'') + "'" \
                                             ",Budget='" + str(sql_data['budget'][i]) + "'" \
                                             ",Revenue='" + str(sql_data['revenue'][i]) + "'" \
                                             ",Oscar='" + str(sql_data['oscar'][i]) + "'" \
                   + " WHERE Movies = '" + sql_data['name'][i].replace('\'','\'\'') + "'"

    print(sql_query)
    print('')
    
    mycursor.execute(sql_query)

mydb.close()





        
    











