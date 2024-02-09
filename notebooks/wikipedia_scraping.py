# -*- coding: utf-8 -*-
import requests
import re

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm 

from imdb import IMDb
imdb = IMDb()

from database.database import initialize_database, insert_movies

root = 'https://en.wikipedia.org'

def export_csv(df, path): 
    df.to_csv(path) 

def fetch(url):
    res = requests.get(url)
    return res.text

def scrape_movie_list(year):
    url = f"{root}/wiki/List_of_American_films_of_{year}"
    content=fetch(url)
    soup=BeautifulSoup(content, 'html.parser')

    tables = soup.findAll('table', class_='wikitable sortable')
    all_links=[]
    for table in tables:
        tr = table.find_all('tr')
        for row in table.find_all('tr')[1:]:
            link = row.find('a', href=re.compile(r'^/wiki/'))
            if link:
                all_links.append(link['href'])

    return all_links

def scrape_movies_content(year):
    all_movies=scrape_movie_list(year)
    movies = []
    
    for movie_url in tqdm(all_movies):
        source_url = f"{root}/{movie_url}"
        content=fetch(source_url)
        soup=BeautifulSoup(content,'html.parser')
        
        
        plot = None
        year = None
        rated = None
        released_date = None
        runtime = None
        genre = None
        director = None
        writer = None
        actors = None
        language = None
        country = None
        awards = None
        cover_image_url = None
        imdb_rating = None
        imdb_id = None 
        trailer_link = None
        
        title = soup.find('h1',id='firstHeading').get_text()
        info_box = image_tag = soup.find('table', class_='infobox vevent')
        if info_box:
            image_tag = info_box.find('img')
        if image_tag:
            cover_image_url = image_tag.get('src').lstrip('//')
        
        for e in soup.findAll('h2'):
            k=e.text
            if k.startswith('Plot'):
                for s in e.find_next_siblings():
                    if s.name == 'h2':
                        break
                    if s.name == 'p':
                        plot = s.get_text().strip()
                        plot += plot + '\n'

        # get the extra movie details from imdb which aren't available on wikipedia
        movie_imdb_search = imdb.search_movie(title)
        if movie_imdb_search:
            movie_imdb = movie_imdb_search[0]
            imdb.update(movie_imdb)
            
            movie_details = {
                'title': title,
                'plot': plot,
                'cover_image_url': cover_image_url or movie_imdb.get('cover url'),
                'year': movie_imdb.get('year'),
                'rated': movie_imdb.get('certificates') if movie_imdb.get('certificates') else None,
                'released_date': movie_imdb.get('original air date'),
                'runtime': movie_imdb.get('runtimes')[0] if movie_imdb.get('runtimes') else None,
                'genre': ', '.join(movie_imdb.get('genres')) if movie_imdb.get('genres') else None,
                'director': ', '.join([d.get('name') for d in movie_imdb.get('directors')]) if movie_imdb.get('directors') else None,
                'writer': ', '.join([str(w) for w in movie_imdb.get('writers')]) if movie_imdb.get('writers') else None,
                'actors': ', '.join([a.get('name') for a in movie_imdb.get('cast')[:5]]) if movie_imdb.get('cast') else None,
                'language': ', '.join(movie_imdb.get('languages')) if movie_imdb.get('languages') else None,
                'country': ', '.join(movie_imdb.get('countries')) if movie_imdb.get('countries') else None,
                'awards': movie_imdb.get('awards'),
                'imdb_rating': movie_imdb.get('rating'),
                'imdb_id': movie_imdb.get('imdbID'),
                'source_url': source_url,
                'trailer_link': movie_imdb.get('videos')[0] if movie_imdb.get('videos') else None
            }
            print(movie_details)
            movies.append(movie_details)
                
            insert_movies(movies)
    return movies


def scrape_movie_data(all_links):
    #all_links = ['https://en.wikipedia.org/wiki/The_Last_of_Us_(TV_series)', 'https://en.wikipedia.org/wiki/Friends','https://en.wikipedia.org/wiki/Modern_Family']
    dfs = []

    for i in all_links:
        table_GDP = pd.read_html(i, match='Genre')
        df_transposed = table_GDP[0].T.reset_index().rename(columns={'index': 'Movie_name'})
        
    
        
        dfs.append(df_transposed)
        
  

    df_result = pd.concat(dfs, ignore_index=True)
    
    return df_result

def data_preprocessing(df_transposed):
    df_transposed.drop(columns={0},inplace=True)# dropping the column with all null values 

    columns_name=df_transposed.iloc[0].tolist() #get the name of the columns
    columns_name

    #rename the name of columns
    for i in range (len(columns_name)):
        df_transposed.rename(columns={i:columns_name[i]}, inplace=True)

    df_transposed.drop(0,inplace=True)
    df_transposed= df_transposed[::2]
    
    df_transposed.reset_index(drop=True,inplace=True)
    
    return df_transposed
        

def export_to_csv(df, path):
    export_csv(df, path)

# Call the function to initialize the database and table
initialize_database()

# for year in range(2020, 2024):
#     movies_data = scrape_movies_content(year)
#     insert_movies(movies_data)




movies_data = scrape_movies_content(2023)
insert_movies(movies_data)


# movie_details= scrape_movie_data()
# data_preprocessing(movie_details)

    

    
# Example usage:
# movies_to_insert = [
#     ('Title1', 'Plot1', 'Image1.jpg', 2022, 'Source1', 'Trailer1'),
#     ('Title2', 'Plot2', 'Image2.jpg', 2023, 'Source2', 'Trailer2'),
#     # Add more entries as needed
# ]
# insert_movies(movies_to_insert)

