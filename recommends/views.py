from movies import serializers
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Keyword, KM
from rest_framework.response import Response
from collections import OrderedDict
from movies.models import Movie
from django.http import JsonResponse
from .models import Keyword
from .serializers import KeywordSerializer
import numpy as np
# Create your views here.
def mm(arr):
    mm_result = (arr - min(min(arr), 2)) / (max(arr) - min(min(arr), 2))
    other = [x-int(x) for x in arr]
    return mm_result, other


@api_view(['GET'])
def all_keywords(request):
    keywords = Keyword.objects.all()
    data = []
    for keyword in keywords:
        temp = {}
        temp['name'] = keyword.word
        temp['id'] = keyword.id
        data.append(temp)
    data = {
        'data': data
    }
    return Response(data)


@api_view(['GET'])
def recommend_movies(request, keywords):
    keywords = keywords.split(' ')
    movie_dict = {}
    for keyword in keywords:
        kw_object = Keyword.objects.get(word=keyword)
        movies = kw_object.movies.all()
        movie_ids = [x.id for x in movies]
        recommend_list = KM.objects.filter(movie__in=movie_ids, word=kw_object.pk)
        # recommend_list.order_by('-score')[:20]

        for rl in recommend_list:
            mv = rl.movie
            if movie_dict.get(mv.id):
                movie_dict[mv.id] += rl.score
            else:
                movie_dict[mv.id] = rl.score
    top20 = list(OrderedDict(sorted(movie_dict.items(), key=lambda t:-t[1])).items())[:20]
    result = mm(np.array([x[1] for x in top20]))
    result = [round(x, 2) for x in result[0] * 9 + result[1]]
    top20_ = []
    for i in range(len(top20)):
        top20_.append((top20[i][0], result[i]))
    data = []
    for i in top20_:
        mv_id = i[0]
        score = i[1]
        mv = Movie.objects.get(pk=mv_id)
        movie_data = {
            'id': mv.pk,
            'title_ko': mv.title_ko,
            'poster_path': mv.poster_path,
            'score': score
            }
        data.append(movie_data)

    result = {'data':  data}
    return Response(result)