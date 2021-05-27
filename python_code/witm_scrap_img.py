import requests
from bs4 import BeautifulSoup
from googletrans import Translator
# pip install googletrans==3.1.0a0

def ko_to_en(word):
    translator = Translator()
    result = translator.translate(word, dest="en")
    return result.text

def get_movie_imgs(keywords):
    keywords = ko_to_en(keywords)
    keywords = keywords.replace(' ','+')
    url = f'https://www.whatismymovie.com/results?text={keywords}'
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'lxml')
    table = soup.find('div', {'class':'tab-content'})
    img_links = soup.find_all('div', {'class':'cover-thumbnail'})
    img_links = [x.img['src'] for x in img_links]
    return img_links[:20]
