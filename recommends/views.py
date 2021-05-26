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
# Create your views here.
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
    data = []

    for i in top20:
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