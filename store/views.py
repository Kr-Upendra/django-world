from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from . import models
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer, CategoryCreateSerializer

class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.object.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can not be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'PUT']:
            return CategoryCreateSerializer
        return CategorySerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if models.Product.object.filter(category_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Category can not be deleted because it is associated with a product.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)