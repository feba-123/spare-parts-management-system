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

    item_name = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','item','item_name', 'item_price','item_image','quantity', 'address', 'notes', 'user','total_amount']
    def get_item_name(self, obj):
        return obj.item.item_name

    def get_item_price(self, obj):
        return obj.item.price
    def get_item_image(self, obj):
        return obj.item.item_image.url

    def get_total_amount(self, obj):
        return obj.quantity * obj.item.price

class BuyItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    address = serializers.CharField(max_length=255)
    notes = serializers.CharField(max_length=255)