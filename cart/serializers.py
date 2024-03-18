from rest_framework import serializers
from owner.models import Item
from user.models import CustomUser
from cart.models import Cart
from .models import Order_Items,Order


class CartSerializer(serializers.ModelSerializer):
    # user = serializers.SerializerMethodField()
    # item=serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['item', 'user', 'quantity', 'date_added']

    # def get_user(self, obj):
    #     user = CustomUser.objects.get(id=obj.user.id)
    #
    #     # user_details = model_to_dict(user)  # converting to dictionary or json
    #     return user.username
    #
    # def get_item(self, obj):
    #     item = Item.objects.get(id=obj.item.id)
    #     return item.item_name

# class Order_ItemsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order_Items
#         fields = '__all__'
#
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'

# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ['item', 'quantity']



class Order_ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Items
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
