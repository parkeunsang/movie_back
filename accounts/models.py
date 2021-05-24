from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
    # email = models.CharField(max_length=100)