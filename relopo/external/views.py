from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import viewsets
# from rest_framework.generics import UpdateAPIView
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken
import requests

from .serializers import LoadAdsSerializer

# Create your views here.
class LoadAdsViewSet(viewsets.ModelViewSet):
    
    """
    API to load external data.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = LoadAdsSerializer
    http_method_names = ['post']
    
    def get_queryset(self):
        pass
    
    def create(self, serializer):
        
        serialized_data = LoadAdsSerializer(data=self.request.data)
        serialized_data.is_valid(raise_exception=True)
        ads = serialized_data.save()
        
        # TODO: isolate in an authentication app
        internal_requests_user = User.objects.get(username=settings.INTERNAL_REQUESTS_USERNAME)
        refresh = RefreshToken.for_user(internal_requests_user)
        url = f'{settings.APP_BASE_URL}api/ads/'
        header = {
            'Authorization': f'Bearer {refresh.access_token}',
            'Content-Type': 'application/json',
        }
        
        response = requests.post(
            url=url,
            json=ads,
            headers=header,
        )
        
        response.raise_for_status()
        
        return Response()