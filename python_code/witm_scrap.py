import requests
from bs4 import BeautifulSoup
from googletrans import Translator
# pip install googletrans==3.1.0a0

def ko_to_en(word):
    translator = Translator()
    result = translator.translate(word, dest="en")
    return result.text

def get_movie_titles(keywords):
    keywords = ko_to_en(keywords)
    print('kw-----------', keywords)
    keywords = keywords.replace(' ','+')
    url = f'https://www.whatismymovie.com/results?text={keywords}'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    table = soup.find('div', {'class':'tab-content'})
    titles = [x.text for x in table.find_all('h3', {'class':'panel-title'})][::2]
    return titles


# keywords = ko_to_en('마동석 형사')
# print(get_movie_titles(keywords))
