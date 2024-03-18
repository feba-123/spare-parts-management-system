from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Item,Category,Deadstock_Item,Booking



class SuperuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# class ItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Item
#         fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = '__all__'

class DeadstockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deadstock_Item
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'