from rest_framework import serializers
from django.conf import settings
from .models import Article, Comment
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


    # def get_ssn(self, obj):
    #      return '***-**-{}'.format(obj.ssn.split('-')[-1]


class ArticleListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    created_at_simple = serializers.SerializerMethodField()
    updated_at_simple = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'
    def get_user_name(self, obj):
        usr_name = obj.user.username
        return usr_name


    def get_created_at_simple(self, obj):
        date_simple = obj.created_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple
    

    def get_updated_at_simple(self, obj):
        date_simple = obj.updated_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # is_valid() 검증 X
    user_name = serializers.SerializerMethodField()
    created_at_simple = serializers.SerializerMethodField()
    updated_at_simple = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('like_users', )
    def get_user_name(self, obj):
        usr_name = obj.user.username
        return usr_name


    def get_created_at_simple(self, obj):
        date_simple = obj.created_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple
    

    def get_updated_at_simple(self, obj):
        date_simple = obj.updated_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple


class CommentListSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    created_at_simple = serializers.SerializerMethodField()
    updated_at_simple = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_user_name(self, obj):
        usr_name = obj.user.username
        return usr_name

    def get_created_at_simple(self, obj):
        date_simple = obj.created_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple
    
    def get_updated_at_simple(self, obj):
        date_simple = obj.updated_at + timedelta(hours=9)
        date_simple = date_simple.strftime('%Y-%m-%d %H:%M')      
        return date_simple


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)  # is_valid() 검증 X
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)