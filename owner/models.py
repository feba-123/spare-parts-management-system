from django.db import models
from user.models import CustomUser

class Category(models.Model):
    category_name = models.CharField(max_length=255, null=False)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.category_name

class Item(models.Model):
        item_name = models.CharField(max_length=255, null=False)
        price = models.DecimalField(max_digits=7,decimal_places=2)
        description = models.CharField(max_length=255, null=False)
        stock = models.IntegerField()
        available = models.BooleanField(default=True)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        manufacturer=models.CharField(max_length=255,null=False)
        item_image = models.ImageField(upload_to='item_images/', null=True, blank=True)
        def __str__(self):
            return self.item_name


class Deadstock_Item(models.Model):
    deadstock_item = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255, null=False)
    stock = models.IntegerField(null=True,blank=True)
    available = models.BooleanField(default=True,null=True,blank=True)
    manufacturer = models.CharField(max_length=255, null=False)
    item_image = models.ImageField(upload_to='item_images/', null=True, blank=True)

    def _str_(self):
        return self.deadstock_item

class Booking(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    item = models.ForeignKey(Deadstock_Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, null=True,blank=True)
    notes = models.CharField(max_length=100, null=True,blank=True)

    def _str_(self):
        return f"Booking for {self.quantity} of {self.item.deadstock_item} by {self.user.username}"