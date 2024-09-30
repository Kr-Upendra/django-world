from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from . import models
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer, CategoryCreateSerializer


class ProductList(ListCreateAPIView):
    queryset = models.Product.objects.select_related('category').all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ProductCreateSerializer
        return ProductSerializer
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product.orderitem_set.count() > 0: 
            return Response({'error': 'Product can not be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST']:
            return CategoryCreateSerializer
        return CategorySerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
class CategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Category.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return CategoryCreateSerializer
        return CategorySerializer

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category.product_set.count() > 0: 
            return Response({'error': 'Category can not be deleted because it is associated with an a product.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete();
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
