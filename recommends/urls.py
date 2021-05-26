from django.urls import path
from . import views
urlpatterns = [
    path('keywords/', views.all_keywords),
    path('keywords/<str:keywords>/', views.recommend_movies),
]
