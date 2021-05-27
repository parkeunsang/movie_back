from rest_framework import serializers
from .models import Movie, MovieUserScore

class MovieSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ('article', )
        # read_only_fields = ('article', )  # 검증 취소 필드
    def get_score(self, obj):
        mus = MovieUserScore.objects.filter(movie_id=obj.id)
        n = len(mus)
        if len(mus):
            score = 0
            for i in range(n):
                score += mus[i].score
            score = round(score/n, 2)
        else:
            score = 0
        return score


  