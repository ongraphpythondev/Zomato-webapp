from rest_framework import serializers
from .models import MenuItem, OrderModel

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = '__all__'

