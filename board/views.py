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


# views in view
def article_list(request):
    articles = Article.objects.all()
    serializers = ArticleListSerializer(articles, many=True)
    return Response(serializers.data)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=201)
    elif request.method == 'DELETE':
        if article.user != request.user:
            return Response(status=400)
        article.delete()
        data = {
            'succuess': True,
            'message': f'{article_pk} 번 게시글 삭제'
        }
        return Response(data=data, status=204)
    elif request.method == 'PUT':
        if article.user != request.user:
            return Response(status=400)
        serializer = ArticleSerializer(article, request.data)
        if serializer.is_valid():
            article = serializer.save()
            return Response(serializer.data, status=201)  # 생성성공시 201
        return Response(serializer.errors, status=400)


@permission_classes([IsAuthenticated])  # is_loggedin
def create_article(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def comment_list_or_create_or_delete(request, pk):
    if request.method == 'POST':
        return create_comment(request, pk)
    elif request.method == 'GET':
        return comment_list(request, pk)
    else:
        return delete_comment(request, pk)

@permission_classes([IsAuthenticated])  # is_loggedin
def create_comment(request, pk):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, review=Article.objects.get(pk=pk))
        return Response(serializer.data)


def comment_list(request, pk):
    comments = Article.objects.get(pk=pk).comment_set.all()
    data = []
    for comment in comments:
        temp = {}
        temp['user'] = comment.user.username
        temp['content'] = comment.content
        temp['comment_id'] = comment.pk
        temp['user_id'] = comment.user.id
        data.append(temp)
    return Response({'data': data})


@permission_classes([IsAuthenticated])
def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if comment.user != request.user:
        return Response(status=400)
    comment.delete()
    data = {
            'succuess': True,
            'message': f'{pk} 번 댓글 삭제'
        }
    return Response(data=data, status=204)