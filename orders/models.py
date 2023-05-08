from django.db import models
from users.models import Customer
from products.models import Product


class Cart(models.Model):
    Customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name = 'USER',editable=False)
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Item(models.Model):
    Cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'CART',editable=False)
    Product_id = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='PRODUCT',editable=False)
    Quantity = models.PositiveBigIntegerField(default=1)
    Created_at = models.DateTimeField(auto_now_add=True)


