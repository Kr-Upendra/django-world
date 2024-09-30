from rest_framework import serializers
from slugify import slugify
from store.models import Product, Category 
from django.urls import reverse

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category    
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product    
        fields = ['id', 'title', 'slug', 'description', 'quantity', 'price', 'category', 'created_at', 'updated_at', 'product_url']  # Include 'url' field    

    product_url = serializers.HyperlinkedIdentityField(
        view_name='product_detail',
        lookup_field='pk'
    )


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product    
        fields = ['title', 'description', 'quantity', 'price', 'category']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.slug = slugify(validated_data['title'])
        return super().update(instance, validated_data)