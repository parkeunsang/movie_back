from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ('article', )
        # read_only_fields = ('article', )  # 검증 취소 필드


# class ArticleSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(min_length=2, max_length=100)
#     content = serializers.CharField(min_length=1)  # form, serilizer에는 text field 없음
#     comment_set = CommentSerializer(many=True, read_only=True)  # article에서 comment를 수정할수는없다.
#     # comment_set으로 해야됨
#     class Meta:
#         model = Article
#         fields = '__all__'
#         # fields = ('title', )


# class ArticleListSerializer(serializers.ModelSerializer):
#     # 댓글 개수 확인
#     comment_set = CommentSerializer(many=True, read_only=True)
#     # 없는 필드 만들어서 JSON 구성
#     comment_count = serializers.IntegerField(source='comment_set.count')  # 쿼리셋
#     class Meta:
#         model = Article
#         # fields = '__all__'
#         fields = ('pk', 'title', 'comment_set', 'comment_count')
#         read_only_fields = fields  # 못바꾸게