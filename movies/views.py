from django.shortcuts import get_object_or_404
from rest_framework.response import Response  # render 역할
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Movie, MovieUserScore
from .serializers import MovieSerializer
from python_code import witm_scrap, witm_scrap_img
import datetime
import re

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


@api_view(['GET'])
def movie_search_title(request, query):
    movies = Movie.objects.filter(title_ko__contains=query)[:10]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def movie_search_keywords(request, query):
    img_list = witm_scrap_img.get_movie_imgs(query)
    data = {'img_list': img_list}
    return Response(data)

@api_view(['GET'])
def movie_recent(request):
    movies = Movie.objects.filter(release_date__gte=datetime.datetime.now()).filter()
    pattern_ko = re.compile('[가-힣]+')  # 한글영화만
    ids = [x.id for x in movies if re.match(pattern_ko, x.title_ko)]
    movies = Movie.objects.filter(id__in=ids).order_by('release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_movie_score(request, movie_id):
    mus = MovieUserScore.objects.filter(movie_id=movie_id)
    n = len(mus)
    if len(mus):
        score = 0
        for i in range(n):
            score += mus[i].score
        score = round(score/n, 2)
    else:
        score = 0
    return Response({'score': score})

# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def movie_score(request):
    movie_id = request.data['movie_id']
    score = float(request.data['value'])
    user_id = request.user.id
    print(movie_id)
    print(user_id)
    if len(MovieUserScore.objects.filter(movie_id=movie_id, user_id=user_id)):
        return Response(status=403)
    mus = MovieUserScore()
    mus.movie_id = movie_id
    print(request.user)
    mus.user_id = user_id
    mus.score = score
    mus.save()
    data = {
        'succuess': True,
        }
    return Response(data=data, status=204)
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def movie_score(request):
#     mus = MovieUserScore()
#     mus.movie_id = request.data.movie_id
#     mus.user_id = request.user.id
#     mus.score = float(request.data.score)
#     mus.save()
#     data = {
#         'succuess': True,
#         }
#     return Response(data=data, status=204)
