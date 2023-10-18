from django.core.cache import cache
from django.db.models.functions import Cast
from rest_framework import serializers
from typing import Dict
from relopo.locations.models import City
from .utils import IdealistaRequest
from .helpers import Cache

class LoadAdsSerializer(serializers.Serializer):
    
    city = serializers.SlugRelatedField(slug_field='slug_name', queryset=City.objects.all())

    def create(self, validated_data: Dict):
        """
        Update current cached `Ads`
        """

        city = validated_data.get('city')
        cache_ads_storage_key = Cache.get_ads_storage_key(Cache.Source.IDEALISTA)
        ads = cache.get(cache_ads_storage_key)
        
        if ads is None:
            
            print("FETCHING IDEALISTA DATA!")

            ads = []
            current_page = 1
            total_pages = 1
            
            while total_pages >= current_page:
                
                idealistaRequest = IdealistaRequest(city=city, page=current_page)
                response = idealistaRequest.make_request()
                total_pages = response.get('totalPages')
                current_page = response.get('actualPage') + 1
                ads.extend(response.get('elementList'))
                
            cache.set(cache_ads_storage_key, ads, timeout=None)
        
        return ads