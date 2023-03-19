from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager




class CostumerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # create and save a new user with given email and password
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, username=None, **extra_fields):
        # create and save a new superuser with given email and password
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', username)
        return self.create_user(email, password, **extra_fields)



# AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
#                   'twitter': 'twitter', 'email': 'email'}


class Costumer(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=150 )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    payment_info = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add = True) #Create 
    updated  = models.DateField(auto_now = True) #Update
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))


    objects = CostumerManager()

    USERNAME_FIELD = 'email'   # Auth with EmailField
    REQUIRED_FIELDS=['phone_number']

    def __str__(self):
        return self.email
