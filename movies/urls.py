from django.urls import path
from .import views
urlpatterns = [
    path('', views.movie_list),
    path('data-list/<str:query>/', views.movie_data_list),
    path('search/title/<str:query>/', views.movie_search_title),
    path('search/keywords/<str:query>/', views.movie_search_keywords),
    path('score/', views.movie_score),
    path('score/<int:movie_id>/', views.get_movie_score),
    # path('score/<int:user_id>/', views.movie_score),  # test
    path('recent/', views.movie_recent),
]
