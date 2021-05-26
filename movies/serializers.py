from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ('article', )
        # read_only_fields = ('article', )  # 검증 취소 필드
