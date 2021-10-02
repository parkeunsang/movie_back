import os
import django
import requests
import datetime
import json
from tqdm import tqdm
import warnings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
warnings.filterwarnings(action='ignore')

import re
import requests
import pickle
from bs4 import BeautifulSoup as bs
from collections import Counter, OrderedDict

print(Genre)
# url_genres = f'{URL}/genre/movie/list?api_key=164acb58532a315bea423c96031d8a71'
# result = requests.get(url_genres)
# genres = result.json()['genres']

# for g in genres:
#     genre = Genre()
#     genre.pk = g['id']
#     genre.genre_name = g['name']
#     genre.save()