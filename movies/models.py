from django.db import models


class Genre(models.Model):
    genre_name = models.CharField(max_length=50)


class Movie(models.Model):
    title_en = models.CharField(max_length=200)
    title_ko = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name = 'movies')
    rate = models.IntegerField()
    rate_people_count = models.IntegerField()
    poster_path = models.TextField()
    description = models.TextField()
    

