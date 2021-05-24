from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, ArticleListSerializer
from .models import Article


@api_view(['GET', 'POST'])
def article_list_or_create(request):
    
    if request.method == 'POST':

        return create_article(request)
    else:
        return article_list(request)


@api_view(['GET'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, article_pk)
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
