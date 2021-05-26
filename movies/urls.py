from django.urls import path
from .import views
urlpatterns = [
    path('', views.movie_list),
    path('data-list/<str:query>/', views.movie_data_list),
    path('search/title/<str:query>/', views.movie_search_title),
    path('search/keywords/<str:query>/', views.movie_search_keywords),
    path('recent/', views.movie_recent),
]
