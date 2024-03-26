from django.db import models
from owner.models import Item
from user.models import CustomUser
class Cart(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=True)
    date_added=models.DateField(auto_now_add=True)

    def subtotal(self):
        return self.quantity*self.item.price

    def reduce_quantity(self, quantity_to_reduce):
        if self.quantity > 0:
            self.quantity -= quantity_to_reduce
            self.save()


    def __str__(self):
        return self.item.item_name

class Order_Items(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE,null=True,blank=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def _str_(self):
        return str(self.user_id)

class Order(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=100, null=True,blank=True)
    notes=models.CharField(max_length=100,null=True,blank=True)
    date=models.ForeignKey(Order_Items,on_delete=models.CASCADE,null=True,blank=True)
    # item_name = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    # item_price = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
