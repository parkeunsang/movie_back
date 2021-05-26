from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer, CommentListSerializer
from .models import Article, Comment


@api_view(['GET', 'POST'])
def article_list_or_create(request):
    if request.method == 'POST':
        return create_article(request)
    else:
        return article_list(request)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)


# views in view
def article_list(request):
    articles = Article.objects.all()
    serializers = ArticleListSerializer(articles, many=True)
    return Response(serializers.data)


@permission_classes([IsAuthenticated])  # is_loggedin
def create_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def comment_list_or_create(request, article_pk):
    if request.method == 'POST':
        return create_comment(request, article_pk)
    else:
        return comment_list(request, article_pk)


@permission_classes([IsAuthenticated])  # is_loggedin
def create_comment(request, article_pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=Article.objects.get(pk=article_pk))
        return Response(serializer.data)


def comment_list(request, article_pk):
    Comments = Article.objects.get(pk=article_pk).comment_set.all()
    serializer = CommentListSerializer(Comments, many=True)
    return Response(serializers.data)