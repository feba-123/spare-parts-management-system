from rest_framework import serializers
from owner.models import Item
from user.models import CustomUser
from cart.models import Cart

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    item=serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['item', 'user', 'quantity', 'date_added']

    def get_user(self, obj):
        user = CustomUser.objects.get(id=obj.user.id)

        # user_details = model_to_dict(user)  # converting to dictionary or json
        return user.username

    def get_item(self, obj):
        item = Item.objects.get(id=obj.item.id)
        return item.item_name

