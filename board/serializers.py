from rest_framework import serializers

from .models import Article
from accounts.serializers import UserSerializer

# from movies.serializers import MovieSerializer

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # is_valid() 검증 X
    # movie = MovieSerializer(required=False)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('like_users', )