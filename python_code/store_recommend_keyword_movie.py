#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import django
import requests
import datetime
import json
from tqdm import tqdm
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import re
import requests
import pickle
from bs4 import BeautifulSoup as bs
from collections import Counter, OrderedDict

pattern = re.compile('<[a-zA-Z0-9가-힣, ]+>|\([a-zA-Z0-9가-힣, ]+\)|\"[a-zA-Z0-9가-힣, ]+|\"|\'[a-zA-Z0-9가-힣, ]+\'|\[[a-zA-Z0-9가-힣, ]+\]')
pattern_all = re.compile('<.+>|\(.+\)|\".+|\"|\'.+\'|\[.+\]')
pattern_order = re.compile('[0-9 ]+\.[a-zA-Z0-9가-힣, ]+')
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
over2020 = Movie.objects.filter(release_date__gte='2000-01-01 00:00').order_by('-release_date')
# movie_titles = [x.title_ko.replace(' ', '') for x in over2020]
movie_titles = [re.sub('[:.\-_ ]', '', x.title_ko) for x in over2020]
movie_pks = [x.pk for x in over2020]


# ## Keyword로 urls 찾기

# ### 구글
def get_urls(url_data, keyword_origin):
    url = f'https://www.google.com/search'    
    url_data[keyword_origin] = []
    keyword = f'{keyword_origin} 영화 추천'
    keyword = keyword.replace(' ', '+')
    for start in range(0, 101, 10):
        params = {
            'q': keyword,
            'start': start
        }
        soup = bs(requests.get(url, headers=headers, params=params).text, 'lxml')
        table = soup.find_all('div', {'class':'g'})
        if start == 0:
            l = 1
        else:
            l = 0

        r = len(table)
        for i in range(l, r):
            if table[i].find('h3'):  # 광고때문인지 없는경우가있음
                title = table[i].find('h3').text.strip()
                url_link = table[i].find('div', {'class':'yuRUbf'}).find('a')['href']
                url_data[keyword_origin].append({
                    'title': title,
                    'url_link': url_link
                })
            else:
                continue
    return url_data


# ### 네이버
# url = 'https://m.search.naver.com/search.naver?page=2&query=%EB%B0%98%EC%A0%84+%EC%98%81%ED%99%94+%EC%B6%94%EC%B2%9C&sm=mtb_pge&start=1&where=m_web'

# url_data = {}

# keyword_origin = '반전'

# url_data[keyword_origin] = []

# keyword = f'{keyword_origin} 영화 추천'
# keyword = keyword.replace(' ', '+')

# for start in tqdm(range(0, 101, 10)):
#     params = {
#         'q': keyword,
#         'start': start
#     }

#     soup = bs(requests.get(url, headers=headers, params=params).text, 'lxml')
#     table = soup.find_all('div', {'class':'g'})
#     if start == 0:
#         l = 1
#     else:
#         l = 0

#     r = len(table)
#     for i in range(l, r):
#         title = table[i].find('h3').text.strip()
#         url_link = table[i].find('div', {'class':'yuRUbf'}).find('a')['href']
#         url_data[keyword_origin].append({
#             'title': title,
#             'url_link': url_link
#         })

# soup = bs(requests.get(url, headers=headers, params=params).text, 'lxml')

# soup.find_all('div', {'class':'total_tit_group'})[1].find('a')['href']


# ## Urls에서 영화 수집
def get_movie_titles(arr):
    arr = [re.sub('[:.\-_\xa0]', '', x).strip() for x in arr]  # 특수문자 제거
    arr = [x for x in arr if not x.isdigit() and len(x) > 1]  # 그냥 이름이 숫자인 영화랑 한글자인 영화는 제외하기로
    
    dummies_contain = ['폰트', '본문', '블로그', '검색', '공유', '추천', '댓글']
    dummies_equal = ['공감', '상세보기', '태그', 'Password', '홈', '링크', '.', '()', '로그인',
                    '부동산', 'TAG', '서울', '부산', 'Calendar', 'Tag', '음악', 'Next', '네이버', '팔로우',
                    '공포', '패션', '연애', '청소년', '스포주의', '스포', '라이프', '인터뷰', '사진', '로맨스', 'TV']
    temp = []
    for text in arr:
        if text in dummies_equal:
            continue
        for dummy in dummies_contain:
            if dummy in text:
                break
        else:
            temp.append(text)
    
    result = []
    for mt in set(temp):
        if mt.replace(' ', '') in movie_titles:
            result.append(mt.replace(' ', ''))
    return result

# 1. 패턴으로 check
def check_pattern(soup):
    unique1 = []  # [title], 'title' 이런 것들
    unique2 = []  # 연도랑 같이 있는 것들
    unique3 = []  # 1. title 이런 것들
    for sf in soup.find_all():
        text = sf.text.strip()
        if len(text) < 50:
            compiled1 = re.search(pattern, text)
            compiled2 = re.search(pattern_all, text)
            compiled3 = re.search(pattern_order, text)
            if compiled1:
                unique1.append(compiled1.group()[1:-1])
            if compiled2:
                unique2.append(text.replace(compiled2.group(), '').strip())
            if compiled3:
                unique3.append(compiled3.group().split('.')[1].strip())
    #         if compiled1:
    #             unique1.append((compiled1.group()[1:-1], sf.name, tuple(sf.get_attribute_list('class'))))
    #         if compiled2:
    #             unique2.append((text.replace(compiled2.group(), '').strip(), sf.name, tuple(sf.get_attribute_list('class'))))
    #         if compiled3:
    #             unique3.append((compiled3.group().split('.')[1].strip(), sf.name, tuple(sf.get_attribute_list('class'))))
    return get_movie_titles(unique1) + get_movie_titles(unique2) + get_movie_titles(unique3)  # 특정한 형식이 갖춰져있는 추천영화들

# 2. 볼드체나 h태그로
def check_tags(soup):
    possible_tags = []
    for i in range(1, 6):
        possible_tags.extend(soup.find_all(f'h{i}'))
    possible_tags.extend(soup.find_all('b'))
    possible_tags.extend(soup.find_all('strong'))
    
    possible_tags = [x.text for x in possible_tags]
    return get_movie_titles(possible_tags)

# 3. 없으면 다 check
def check_all(soup):
    all_tags = [(x.text.strip(), x.name, tuple(x.get_attribute_list('class'))) for x in soup.find_all() if x.text]
    all_tags = [x for x in all_tags if x[0] != '' and len(x[0]) < 20]
    all_text = [re.sub('[:.-_\xa0]', '', x[0]).strip() for x in all_tags]
    return get_movie_titles(all_text)


url_data = {}
keyword_data = {}
keywords = ['반전', '비올때', '이별', '공포', '넷플릭스', '스포츠', '프로그래머',
           '감동', '왓챠', '역사', '혼자보기좋은', '혼술', '짧은', '명작', '죽기전에봐야할']
for keyword_origin in keywords:
    url_data = get_urls(url_data, keyword_origin)

    kws = []
    for url_d in tqdm(url_data[keyword_origin]):
        url = url_d['url_link']
        if '영화' not in url_d['title']:  # 글제목이 영화와 관계가 없을경우
            continue
        if 'youtube' in url or 'namu.wiki' in url:
            continue
        try:
            soup = bs(requests.get(url, headers=headers).text)
        except:
            print('error', url)
            continue
        pattern_movies = check_pattern(soup)
        possible_tags = check_tags(soup)
        all_tags = check_all(soup)

        mts = list(set(pattern_movies + possible_tags + all_tags))  # 해당 글의 영화제목들
        if mts:
            kws.append(mts)
    keyword_data[keyword_origin] = kws

print(keyword_data.keys())


# ### 저장/로드
# with open('url_data_0526.pkl', 'wb') as f:
#     pickle.dump(url_data, f)

# with open('keyword_data_0526.pkl', 'wb') as f:
#     pickle.dump(keyword_data, f)
# with open('url_data_0528.pkl', 'rb') as f:
#     url_data = pickle.load(f) # 단 한줄씩 읽어옴
# with open('keyword_data_0528.pkl', 'rb') as f:
#     keyword_data = pickle.load(f) # 단 한줄씩 읽어옴


def movie_order(kws):
    temp = []
    for k in kws:
        temp += k
    return list(OrderedDict(Counter(temp).most_common()).items())


Keyword.objects.all().delete()
# keyword 저장
for key in keyword_data.keys():
    keyword = Keyword()
    keyword.word = key
    keyword.save()

# 관계 설정
for key in tqdm(keyword_data.keys()):

    word_pk = Keyword.objects.filter(word=key)[0].pk
    mv_od = movie_order(keyword_data[key])
    maximum = mv_od[0][1]
    minimum = min(2, 10 / maximum)

    for mo in mv_od:
        km = KM()
        idx = movie_titles.index(mo[0])
        movie_pk = Movie.objects.filter(pk=movie_pks[idx])[0].pk
        km.word_id = word_pk
        km.movie_id = movie_pk
        km.score = round(minimum + (10 - minimum) * (mo[1]-1)/maximum, 2)
        km.save()
