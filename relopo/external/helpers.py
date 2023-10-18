from enum import Enum
from django.conf import settings

class Cache:
    
    class Source(Enum):
        IDEALISTA = 'idealista'
        
    def get_auth_storage_key(source: Source):
        return settings.CACHE_PREFIX_AUTH_DATA + "_" + source.value
    
    def get_ads_storage_key(source: Source):
        settings.CACHE_PREFIX_EXTERNAL_ADS_DATA + "_" + source.value