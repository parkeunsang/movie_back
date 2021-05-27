from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('articles/', views.article_list_or_create),
    path('articles/check/<int:article_pk>/', views.article_check),
    path('comment/check/<int:comment_pk>/', views.comment_check),
    # path('articles/', views.create_article),
    path('articles/<int:article_pk>/', views.article_detail),
    path('comment/<int:pk>/', views.comment_list_or_create_or_delete),
]