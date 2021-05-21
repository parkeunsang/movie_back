from django.db import models
from django.conf import settings
from movies.models import Movie
# Create your models here.
class Keyword(models.Model):
    word = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='recommend_words')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='keywords')