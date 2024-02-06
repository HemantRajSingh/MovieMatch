# -*- coding: utf-8 -*-
import requests
import re

from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm 

from database.database import insert_movies

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
    titles=[]
    summaries=[]
    cover_images = []
    wikipedia_links=[]
    all_movies=scrape_movie_list(year)
    movies = []
    
    for movie_url in tqdm(all_movies):
        source_url = f"{root}/{movie_url}"
        content=fetch(source_url)
        soup=BeautifulSoup(content,'html.parser')
        title = soup.find('h1',id='firstHeading').get_text()
        info_box = image_tag = soup.find('table', class_='infobox vevent')
        cover_image_url = None
        if info_box:
            image_tag = info_box.find('img')
        if image_tag:
            cover_image_url = image_tag.get('src').lstrip('//')

        plot = ''
        for e in soup.findAll('h2'):
            k=e.text
            if k.startswith('Plot'):
                for s in e.find_next_siblings():
                    if s.name == 'h2':
                        break
                    if s.name == 'p':
                        plot = s.get_text().strip()
                        plot += plot + '\n'

        titles.append(title)
        summaries.append(plot)
        cover_images.append(cover_image_url)
        wikipedia_links.append(source_url)
        movies.append((title, plot, cover_image_url, year, source_url, ''))

    # df = pd.DataFrame({'Movie Title': titles, 'Plot Summary': summaries, 'Cover Image': cover_images, 'Year': year, 'Source': wikipedia_links})

    # CREATE TABLE Movie (
    #     id SERIAL PRIMARY KEY,
    #     title VARCHAR(255) NOT NULL,
    #     plot TEXT,
    #     year INT,
    #     genres VARCHAR(255),
    #     director VARCHAR(255),
    #     actors TEXT,
    #     imdb_rating FLOAT,
    #     release_date DATE,
    #     running_time INT,
    #     language VARCHAR(100),
    #     country VARCHAR(100),
    #     production_company VARCHAR(255),
    #     awards TEXT,
    #     trailer_url VARCHAR(255),
    #     poster_image_url VARCHAR(255)
    # );
    # get movie attributes for the above column and insert those into movie database using postgres.
    # Create methods to connect to postgres db

    # path = f'./dataset/movie_list_{year}.csv'
    # export_csv(df, path)    
    
    return movies
        

def export_to_csv(df, path):
    export_csv(df, path)

# for year in range(2000, 2024):
#     movies_data = scrape_movies_content(year)

movies_data = scrape_movies_content(2023)
insert_movies(movies_data)

    

    
# Example usage:
# movies_to_insert = [
#     ('Title1', 'Plot1', 'Image1.jpg', 2022, 'Source1', 'Trailer1'),
#     ('Title2', 'Plot2', 'Image2.jpg', 2023, 'Source2', 'Trailer2'),
#     # Add more entries as needed
# ]
# insert_movies(movies_to_insert)

