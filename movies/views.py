from django.shortcuts import get_object_or_404
from rest_framework.response import Response  # render 역할
from rest_framework.decorators import api_view  # require_methods 역할
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer
from python_code import witm_scrap, witm_scrap_img


@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.filter(release_date__lte="2021-02-01 00:00").filter(poster_path__isnull=False)[:20]
    serializer = MovieSerializer(movies, many=True)  # context 느낌
    return Response(serializer.data)

@api_view(['GET'])
def movie_data_list(request, query):
    if query:
        movies = Movie.objects.filter(title_ko__contains=query)[:20]
        serializer = MovieSerializer(movies, many=True)  # context 느낌
        return Response(serializer.data)


# @api_view(['GET'])
# def movie_search(request, picked, query):
#     if picked == 'title':
#         movies = Movie.objects.filter(title_ko__contains=query)[:10]
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
#     else:
#         movie_list = witm_scrap.get_movie_titles(query)
#         movie_list = [x[:-7] for x in movie_list]
#         print('ml----------', movie_list)
#         movies = Movie.objects.filter(title_en__in=movie_list)
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
@api_view(['GET'])
def movie_search(request, picked, query):
    if picked == 'title':
        movies = Movie.objects.filter(title_ko__contains=query)[:10]
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    else:
        img_list = witm_scrap_img.get_movie_imgs(query)
        data = {'img_list': img_list}
        return Response(data)