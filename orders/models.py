from django.db import models
from users.models import Customer
from products.models import Product


class Item(models.Model):
    Product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="PRODUCT", editable=False
    )
    Quantity = models.IntegerField(default=1)
    Created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.Product_id.name) + " (" + str(self.Quantity) + ")"


class Cart(models.Model):
    Customer_id = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="USER", editable=False
    )
    Created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, blank=True, related_name="carti")

    def __str__(self):
        return str(self.id) + "  " + str(self.Customer_id.email)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    items = models.ManyToManyField(Item)
    # STATUS_CHOICES = (
    #     ('P', 'Pending'),
    #     ('C', 'Completed'),
    #     ('X', 'Cancelled'),
    # )
    # status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    def calculate_total_amount(self):
        items = self.items.all()
        total = sum(item.quantity * item.Product_id.price for item in items)
        self.total_amount = total
        self.save()

    def __str__(self):
        return str(self.id)
