from rest_framework import serializers

from .models import City

class CitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = City
        fields = ['id', 'name', 'slug_name']