from django.urls import path
from . import views
urlpatterns = [
    path('keywords/<str:keywords>/', views.recommend_movies),
]
