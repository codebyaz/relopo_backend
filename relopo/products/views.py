from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication

from .serializers import ProductSerializer
from .models import Product

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that list products.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.TokenAuthentication, 
        authentication.SessionAuthentication,
    ]
