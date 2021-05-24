from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('articles/', views.article_list_or_create),
    path('articles/<int:article_pk>/', views.article_detail),
]