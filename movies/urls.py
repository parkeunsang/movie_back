from django.urls import path
from .import views
urlpatterns = [
    path('', views.movie_list),
    path('data-list/<str:query>/', views.movie_data_list),
    path('search/<str:picked>/<str:query>/', views.movie_search),
]
