from django.shortcuts import get_object_or_404
from rest_framework.response import Response  # render 역할
from rest_framework.decorators import api_view  # require_methods 역할
from rest_framework import status
from .models import Movie
from .serializers import MovieSerializer

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()[:20]
    serializer = MovieSerializer(movies, many=True)  # context 느낌
    return Response(serializer.data)
