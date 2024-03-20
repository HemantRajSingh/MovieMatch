import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

def create_url(year):
    return f'https://www.imdb.com/search/title/?title_type=feature&user_rating=7,&year={year}&num_votes=1000&countries=US'

def get_movie_info(movie):
    title = movie.find('a', class_='ipc-title-link-wrapper')
    id = title['href'].split('/')[2]
    year = movie.find('span', class_='dli-title-metadata-item').text
    runtime = movie.find('span', class_='dli-title-metadata-item').text
    rating = movie.find('span', class_='ratingGroup--imdb-rating').text
    votes = movie.find('span', class_='ipc-rating-star--voteCount').text
    plot = movie.find('div', class_='ipc-html-content-inner-div').text
    return {
        'id': id,
        'title': title.text,
        'year': year,
        'runtime': runtime,
        'rating': rating,
        'votes': votes,
        'plot': plot
    }
    
def get_movies(year):
    url = create_url(year)
    # Using sesson to let imdb persists parameters across requests
    session = requests.Session()
    # Added User-Agent in headers to avoid 403 error
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
    response = session.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    driver = webdriver.Chrome()
    driver.get(url)

    # Wait up to 10 seconds for the page to load and the button to become clickable
    wait = WebDriverWait(driver, 10)

    while True:
        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-see-more__button')))
            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            driver.execute_script("arguments[0].click();", load_more_button)
            
            time.sleep(3)
        except Exception as e:
            break
        
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')
    
    movie_list = []
    for movie in movies:
        movie_list.append(get_movie_info(movie))
        
    print('Total movies scraped:', len(movie_list))
    df = pd.DataFrame(movie_list)
    df.to_csv(f'imdb_movies_{year}.csv', index=False)
    return movie_list


# create url for year 2020 - 2024
years = list(range(2020, 2025))
df = pd.DataFrame()
for year in years:
    movies = get_movies(year)
    df = df.append(pd.DataFrame(movies))

df.to_csv('imdb_movies.csv', index=False)