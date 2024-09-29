from rest_framework import serializers
from store.models import Product, Category 


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category    
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product    
        fields = ['id', 'title', 'slug', 'description', 'quantity', 'price', 'category'] # to select all fields use this '__all__'
    

        

