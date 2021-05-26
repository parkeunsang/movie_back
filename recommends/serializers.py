from rest_framework import serializers
from .models import KM, Keyword

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'

        
class KMSerializer(serializers.ModelSerializer):
    class Meta:
        model = KM
        fields = '__all__'