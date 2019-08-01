from rest_framework import serializers

from .models import Item, UserItem, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id =serializers.IntegerField(write_only = True)
    class Meta:
        model = Item
        fields = ['id', 'title', 'category', 'category_id', 'description', 'created', 'price', 'image']


class UserItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = UserItem
        fields = ['item', 'user', 'count']

