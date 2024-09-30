from rest_framework import serializers
from slugify import slugify
from store.models import Product, Category 

class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='category-detail',
        lookup_field='pk'
    )

    class Meta:
        model = Category    
        fields = ['id', 'title', 'slug', 'description', 'created_at', 'updated_at', 'url']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category    
        fields = ['title', 'description']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.slug = slugify(validated_data['title'])
        return super().update(instance, validated_data)
    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product    
        fields = ['id', 'title', 'slug', 'description', 'quantity', 'price', 'category', 'created_at', 'updated_at', 'url']  # Include 'url' field    

    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
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