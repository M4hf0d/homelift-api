from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MaxValueValidator,  MinValueValidator





    

class CustomerManager(BaseUserManager):
    def create_user(self, email, phone_number, fullname, wilaya,daira,street,addresse_line,mairie,code_postal,password=None):
        """
        Creates and saves a Customer with the given email, phone_number, fullname,
        and password.
        """
        if not email:
            raise ValueError('Customers must have an email address')

        customer = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            fullname=fullname,
            wilaya = wilaya,
            daira =daira,
            street = street,
            addresse_line = addresse_line,
            mairie = mairie,
            code_postal = code_postal,
        )

        customer.set_password(password)
        customer.save(using=self._db)
        return customer

    def create_superuser(self, email, phone_number, fullname, password, wilaya,daira,street,addresse_line,mairie,code_postal,):
        """
        Creates and saves a superuser with the given email, phone_number, fullname,
        and password.
        """
        customer = self.create_user(
            email=email,
            phone_number=phone_number,
            fullname=fullname,
            password=password,
            wilaya = wilaya,
            daira =daira,
            street = street,
            addresse_line = addresse_line,
            mairie = mairie,
            code_postal = code_postal,           
        )
        customer.is_active = True
        customer.is_admin = True
        customer.save(using=self._db)
        return customer



# AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
#                   'twitter': 'twitter', 'email': 'email'}


class Customer(AbstractBaseUser):
    username = models.CharField(max_length=255, blank=True , null=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    payment_info = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add = True) #Create 
    updated  = models.DateField(auto_now = True) #Update

    
    wilaya = models.CharField(max_length=255)
    daira = models.CharField(max_length=255)
    mairie = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    addresse_line = models.TextField()
    code_postal = models.PositiveIntegerField(validators=[MinValueValidator(11111),MaxValueValidator(99999)])
    
    
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))


    objects = CustomerManager()

    USERNAME_FIELD = 'email'   # Auth with EmailField
    REQUIRED_FIELDS=['phone_number','fullname','wilaya','daira','mairie','street','addresse_line','code_postal']
    def has_perm(self, perm, obj=None):
            "Does the user have a specific permission?"
            # Simplest possible answer: Yes, always
            return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @property
    def is_supersuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    