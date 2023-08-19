from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import authentication

from .serializers import ProductSerializer
from .models import Product

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that list products.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [
        authentication.TokenAuthentication, 
        authentication.SessionAuthentication,
    ]
    http_method_names = ['get']
