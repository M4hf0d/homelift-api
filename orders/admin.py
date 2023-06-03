from django.contrib import admin
from .models import Item, Cart , Payment,Order 

admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(Order)

# Register your models here.
