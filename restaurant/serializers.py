from rest_framework import serializers

from .models import restaurant_model
 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = restaurant_model
        fields = '__all__'
 
