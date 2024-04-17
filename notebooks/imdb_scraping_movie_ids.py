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
    return f'https://www.imdb.com/search/title/?title_type=feature&user_rating=6,&year={year}&countries=US'

def get_movie_info(movie):
    title = movie.find('a', class_='ipc-title-link-wrapper')
    id = title['href'].split('/')[2]
    year = movie.find('span', class_='dli-title-metadata-item')
    runtime = movie.find('span', class_='dli-title-metadata-item')
    rating = movie.find('span', class_='ratingGroup--imdb-rating')
    votes = movie.find('span', class_='ipc-rating-star--voteCount')
    plot = movie.find('div', class_='ipc-html-content-inner-div')
    return {
        'id': id,
        'title': title.text if title else '',
        'year': year.text if year else '',
        'runtime': runtime.text if runtime else '',
        'rating': rating.text if rating else '',
        'votes': votes.text if votes else '',
        'plot': plot.text if plot else ''
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
    print('Year:', year, 'Movies scraped:', len(movie_list))
    return movie_list


from tqdm import tqdm

# create url for year 2000 - 2025
years = list(range(2000, 2025))
all_movies = []
for year in tqdm(years):
    movies = get_movies(year)
    all_movies.extend(movies)
df = pd.DataFrame(all_movies)
df.to_csv('imdb_movies.csv', index=False)
