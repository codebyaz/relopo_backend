from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import City
from .serializers import CitySerializer

# Create your views here.
class CityViewSet(ReadOnlyModelViewSet):
    
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer 
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [
        TokenAuthentication, 
        SessionAuthentication,
    ]
    http_method_names = ['get']
    