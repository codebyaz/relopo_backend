from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from typing import List

from .models import Ad
from .serializers import AdSerializer, AdCreateResponseSerializer, IdealistaAdSerializer

# Create your views here.

class AdsViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
      
    @swagger_auto_schema(
        operation_description="Retrieve a list of items",
        responses={200: AdSerializer(many=True)}
    )
    def list(self, request: Request):
        queryset = Ad.objects.all()
        serializer = AdSerializer(queryset, many=True)
        
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create 1 to n ads",
        request_body=AdSerializer(many=True),
        responses={200: AdCreateResponseSerializer(many=True)}
    )
    def create(self, request: Request, *args, **kwargs):
        serializer = AdSerializer(data=request.data, many=True)
        
        return Response({"message" : "created"})
    
    def retrieve(self, request: Request, pk=None):  
        ad = get_object_or_404(Ad, pk=pk)
        serializer = AdSerializer(ad)
        
        return Response(serializer.data)
        
        
        


# class AdsViewSet(viewsets.ModelViewSet):
    
#     queryset = Ad.objects.all()
#     permission_classes = [IsAuthenticated, IsAdminUser]
#     serializer_class = AdSerializer        
    
class MultipleAdsViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = IdealistaAdSerializer
    http_method_names = ['post']
    
    def create(self, request: Request):
        serialized_ads = IdealistaAdSerializer(data=request.data, many=True)
        serialized_ads.is_valid(raise_exception=True)
        serialized_ads.save()
        
        return Response()