from django.db import models
from django.contrib.auth.models import AbstractUser

class Costumer(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=150 )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    payment_info = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add = True) #Create 
    updated  = models.DateField(auto_now = True) #Update
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    USERNAME_FIELD = 'email'   # Auth with EmailField
    REQUIRED_FIELDS=['phone_number']

    def __str__(self):
        return self.email
