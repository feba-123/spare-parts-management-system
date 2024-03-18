from django.contrib import admin

from cart.models import Cart
from cart.models import Order_Items,Order
admin.site.register(Cart)
admin.site.register(Order_Items)
admin.site.register(Order)
