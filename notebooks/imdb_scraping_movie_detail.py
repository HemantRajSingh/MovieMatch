import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

import time
import json
from tqdm import tqdm

# Using sesson to let imdb persists parameters across requests
session = requests.Session()
# Added User-Agent in headers to avoid 403 error
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
})
    
df = pd.read_csv('imdb_movies.csv')

def create_url(id, attribute=[]):
    url = "https://www.imdb.com/title/"+str(id)+"/"
    if 'synopsis' in attribute:
        url += "plotsummary/"
    return url

def load_page(url):
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_movie_data(id):
    url = create_url(id)
    soup = load_page(url)
    movie_data = soup.find('script',{"type":"application/ld+json"})
    movie = {}

    if movie_data is not None:
        movie_data = json.loads(movie_data.string)
        movie['image_link'] = movie_data.get('image', '')
        movie['imdb_id'] = id
        aggregate_rating = movie_data.get('aggregateRating', {})
        movie['rating_count'] = aggregate_rating.get('ratingCount', '')
        movie['best_rating'] = aggregate_rating.get('bestRating', '')
        movie['worst_rating'] = aggregate_rating.get('worstRating')
        movie['rating'] = aggregate_rating.get('ratingValue')
        movie['genre'] = movie_data.get('genre')
        movie['keywords'] = movie_data.get('keywords', '').split(',')
        movie['trailer_link'] = movie_data.get('trailer', {}).get('url', '')
        movie['actors'] = [actor.get('name', '') for actor in movie_data.get('actor', [])]
        movie['director'] = [director.get('name', '') for director in movie_data.get('director', [])]
        
        synopsis_soup = load_page(create_url(id, attribute=['synopsis']))
        synopsis_div = synopsis_soup.select_one('[data-testid="sub-section-synopsis"] .ipc-html-content-inner-div')
        if synopsis_div is not None:
            movie['synopsis'] = synopsis_div.text
        summary_div = synopsis_soup.select_one('[data-testid="sub-section-summaries"] .ipc-html-content-inner-div')
        if summary_div is not None:
            movie['summary'] = summary_div.text
    
    return movie

movies = []
for id in tqdm(df['id']):
    print(id)
    try: 
        movie = get_movie_data(id)
        # Append the movie data to movies_df
        if movie != {}:
            movies.append(movie)
            time.sleep(3)
    except Exception as e:
        print(e)

movies_df = pd.DataFrame(movies)
movies_df.to_csv('imdb_movies_detail_1000.csv', index=False)