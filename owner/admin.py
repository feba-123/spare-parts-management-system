from django.contrib import admin

from .models import Item,Category,Deadstock_Item,Booking

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Deadstock_Item)
admin.site.register(Booking)