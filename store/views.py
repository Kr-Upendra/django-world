from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . import models
from .serializers import ProductSerializer, ProductCreateSerializer, CategorySerializer, CategoryCreateSerializer


class ProductList(APIView):
    def get(self, request):
        queryset = models.Product.objects.select_related('category').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product created successfully'}, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get_object(self, pk):
        product = get_object_or_404(models.Product, pk=pk)
        return product
    
    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product.orderitem_set.count() > 0: 
            return Response({'error': 'Product can not be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):
    def get(self, request):
        categories = models.Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data) 

    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Category created successfully'}, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    def get_object(self, pk):
        category = get_object_or_404(models.Category, pk=pk)
        return category

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        category = self.get_object(pk)
        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Category updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category.product_set.count() > 0: 
            return Response({'error': 'Category can not be deleted because it is associated with an a product.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        category.delete();
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
