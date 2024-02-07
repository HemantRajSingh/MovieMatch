# -*- coding: utf-8 -*-
import pandas as pd
import requests
import re

df = pd.read_csv('movie_list_2000.csv')

keys = ['Rated',
        'Released',
        'Runtime',
        'Genre',
        'Director',
        'Writer',
        'Actors',
        'Plot',
        'Language',
        'Country',
        'Awards',
        'Poster',
        'Ratings',
        'imdbRating',
        'BoxOffice',
        'imdbID'
      ]
for key in keys:
  df[key] = ''

def get_movie_details(title):
  r = requests.get(f'https://www.omdbapi.com/?apikey={key}&t={title}')
  return r.json()

for idx, row in df.iterrows():
  movie_title = row['Movie Title']
  title = re.sub(r'\s\(.+\)', '', movie_title)
  year = row['Year']
  data = get_movie_details(title)
  if data['Response'] == 'True':
    for key in keys:
      df.at[idx, key] = data.get(key, None)
    df.at[idx, 'omdb Year'] = data.get('Year', None)
    df.at[idx, 'omdb Title'] = data.get('Title', None)

df.to_csv('movie_list_2000_omdb.csv')

