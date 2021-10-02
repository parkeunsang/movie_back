import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "board.settings")

django.setup()

from movie_back.movies.models import Movie
print(Movie.objects.all())
# From now onwards start your script..