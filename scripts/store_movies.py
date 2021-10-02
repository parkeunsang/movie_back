#!/usr/bin/env python
# coding: utf-8
import os
import django
import requests
import datetime
import json
from tqdm import tqdm
import warnings
from movies.models import Genre, Movie, MG
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
warnings.filterwarnings(action='ignore')

import requests
from bs4 import BeautifulSoup as bs


# https://developers.themoviedb.org/3/discover/movie-discover
URL = 'https://api.themoviedb.org/3'
API_KEY = os.environ.get('MOVIE_KEY')

# ## 장르
url_genres = f'{URL}/genre/movie/list?api_key={API_KEY}'
result = requests.get(url_genres)
genres = result.json()['genres']
for g in genres:
    genre = Genre()
    genre.pk = g['id']
    genre.genre_name = g['name']
    genre.save()


# ## 영화(2000~2021)
def store_movies(year):
    print(f'storing-----------{year}')
    with open(f'./data/movie_{year}.json', 'r') as fp:
        movies = json.load(fp)
    
    # delete stored movies
    movies_year = Movie.objects.filter(release_date__year=year)
    movies_year.delete()
    # using bulk
    to_db_movies = []
    for mv in tqdm(movies):
        movie = Movie()
        movie.pk = mv['id']
        movie.title_en = mv['original_title']
        movie.title_ko = mv['title']
        movie.rate = mv['vote_average']
        movie.rate_people_count = mv['vote_count']
        movie.poster_path = mv['poster_path']
        movie.description = mv['overview']
        movie.release_date = datetime.datetime.strptime(mv['release_date'], '%Y-%m-%d')
        to_db_movies.append(movie)
        
    div = 100
    to_db_movies_batch = []
    for i in range(len(to_db_movies) // div + 1):
        to_db_movies_batch.append(to_db_movies[i*div:(i+1)*div])
        
    for idx, batch in enumerate(to_db_movies_batch):
        print(round(idx/len(to_db_movies_batch), 2), end='|')
        temp = Movie.objects.bulk_create(batch)
    # add genre
    mgs = []
    for mv in movies:
        for gid in mv['genre_ids']:
            mg = MG()
            mg.movie_id = mv['id']
            mg.genre_id = gid
            mgs.append(mg)
    temp = MG.objects.bulk_create(mgs)

# 저장
for year in reversed(range(2000, 2022)):
    store_movies(year)

