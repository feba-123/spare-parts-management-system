from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    phone_number = models.IntegerField(unique=True,blank=True,null=True)

    def __str__(self):
        return self.username
