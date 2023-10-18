from django.conf import settings
from django.core.cache import cache
from typing import Dict
import requests
import base64

from .helpers import Cache
from relopo.locations.models import City

class ExternalSourceAuthentication:
    
    auth_cache_key: str
    
    def __init__(self) -> None:
        pass
    
    class Meta:
        abstract: True
    
    def authenticate(self):
        pass
    
    def get_auth_token(self, source: str) -> str:
        self.auth_cache_key = Cache.get_auth_storage_key(source)
        return cache.get(self.auth_cache_key)
 
class IdealistaRequest(ExternalSourceAuthentication):
    
    def url(self) -> str:
        return settings.IDEALISTA_API_BASE_URL + '/' + self.city.country.lower() + '/search'
    
    def __init__(self, city: City, page: int = 1) -> None:
        self.city = city
        self.page = page
        super().__init__()
    
    def make_request(self) -> Dict:
        url = self.url()

        payload = self.mount_payload()
        token = self.authenticate()
    
        headers = {
            'Content-Type': 'Content-Type: multipart/form-data',
            'Authorization' : 'Bearer ' + token
        }
        
        response = requests.post(
            url=url,
            headers=headers,
            params=payload
        )

        return response.json()
        
    def mount_payload(self) -> Dict:
        payload = {
            "locale" : 'en',
            "maxItems" : 50,
            "numPage" : self.page,
            "operation" : 'rent',
            "center" : self.city.center,
            "distance": self.city.radius,
            "language" : 'en',
            "hasMultimedia" : True,
            "propertyType": 'homes',
            "sinceDate": 'M'
        }
        
        return payload
        
    
    def authenticate(self) -> str :
        
        token = self.get_auth_token(source=Cache.Source.IDEALISTA)
        
        if token is None: 
            print('=> refreshing oauth token!')
            api_key = settings.IDEALISTA_API_KEY
            secret = settings.IDEALISTA_SECRET
            token_url = settings.IDEALISTA_AUTH_URL

            key_secret = api_key + ":" + secret
            
            headers = {
                "Authorization" : "Basic " + base64.b64encode(key_secret.encode("ascii")).decode("ascii"),
                "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8"
            }
            payload = {
                "grant_type" : "client_credentials",
                "scope" : "read"
            }
            response = requests.post(
                    token_url,
                    headers = headers,
                    params = payload
                ).json()
            
            token = response['access_token']
            expires_in = response['expires_in']

            print('GENERATED OAUTH TOKEN => ', token)

            cache.set(self.auth_cache_key, token, timeout=expires_in)
            
        return token