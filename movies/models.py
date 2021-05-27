from django.db import models
from django.conf import settings
from django.db.models.fields import related

class Genre(models.Model):
    genre_name = models.CharField(max_length=50)


class Movie(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='movies', through='MovieUserScore')
    title_en = models.CharField(max_length=200)
    title_ko = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name = 'movies', through= 'MG')
    rate = models.IntegerField()
    rate_people_count = models.IntegerField()
    poster_path = models.TextField(null=True)
    description = models.TextField()
    release_date = models.DateTimeField()
    

class MG(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class MovieUserScore(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.FloatField()