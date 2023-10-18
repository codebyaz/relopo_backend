from rest_framework import serializers
from typing import List, Dict, OrderedDict

from .models import Ad
from relopo.locations.models import City

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class AdCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class IdealistaAdListSerializer(serializers.ListSerializer):
    def create(self, validated_data: Dict):
        ads: List[OrderedDict] = validated_data.get('ads')
        created_ads = []
        property_types = {property_type.name.lower(): property_type for property_type in Ad.PropertyTypes}
        Ad.objects.all().delete()
        for validated_ad in ads:
            current_property_type = property_types.get(validated_ad['property_type'])
            validated_ad['property_type'] = current_property_type
            validated_ad['city'] = validated_ad.get('province')
            validated_ad.pop('province')
            ad = Ad(**validated_ad)
            created_ads.append(ad)
            
        return Ad.objects.bulk_create(created_ads)

class IdealistaAdSerializer(serializers.ModelSerializer):
    
    propertyCode = serializers.IntegerField(source='external_code')
    province = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    numPhotos = serializers.IntegerField(source='number_photos')
    municipality = serializers.CharField(source='neighborhood')
    url = serializers.CharField(source='source_url')
    propertyType = serializers.ChoiceField(source='property_type', choices=[property_type.name.lower() for property_type in Ad.PropertyTypes])
    floor = serializers.IntegerField(allow_null=True, read_only=True)
    hasLift = serializers.BooleanField(source='has_lift', required=False)
    
    class Meta:
        model = Ad
        # list_serializer_class = IdealistaAdListSerializer # for bulk creation
        fields = [
            'propertyCode',
            'numPhotos',
            'municipality',
            'url',
            'propertyType',
            'hasLift',
            'thumbnail',
            'floor',
            'price',
            'size',
            'rooms',
            'bathrooms',
            'address',
            'province',
            'district',
            'latitude',
            'longitude',
        ]
        
    def create(self, validated_data: Dict):
        property_types = {property_type.name.lower(): property_type for property_type in Ad.PropertyTypes}
        current_property_type = property_types.get(validated_data['property_type'])
        validated_data['property_type'] = current_property_type
        validated_data['city'] = validated_data.get('province')
        validated_data.pop('province')
        
        # create or update to avoid losing internal id relation
        ad = Ad.objects.update_or_create(
            defaults=validated_data,
            external_code=validated_data.get('external_code')
        )
        
        return ad
            