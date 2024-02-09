from django.db import models

class Item(models.Model):
        item_name = models.CharField(max_length=255, null=False)
        price = models.CharField(max_length=255, null=False)
        description = models.CharField(max_length=255, null=False)
        stock = models.IntegerField()
        available = models.BooleanField(default=True)

        def __str__(self):
            return self.item_name
