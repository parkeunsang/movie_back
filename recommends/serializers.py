from rest_framework import serializers
from .models import KM


class KMSerializer(serializers.ModelSerializer):
    class Meta:
        model = KM
        fields = '__all__'