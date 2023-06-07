from rest_framework import serializers
from .models import Item, Cart, Payment, Order
from users.serializers import CustomerListSerializer


class ItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="Product_id.name", read_only=True)
    image = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    items_price = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def validate_Quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value

    def get_items_price(self, obj):
        return int(int(obj.Product_id.price) * int(obj.Quantity))

    def get_unit_price(self, obj):
        return obj.Product_id.price
    
    def get_image(self,obj): #إعمل نفسك ميت
        return 'http://127.0.0.1:8000/images/' +str(obj.Product_id.image)


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerListSerializer()
    items = ItemSerializer(many=True)
    shipping_adress = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "customer", "created_at", "total_amount", "items","shipping_adress"]
        read_only_fields = ["id", "created_at", "total_amount"]
    def get_shipping_adress(self,obj):
        return obj.customer.code_postal
    

class CartSerializer(serializers.ModelSerializer):
    # items = serializers.CharField(source="items.Product_id.name", many= True)
    items = ItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_total_amount(self, obj):
        total = sum(item.Quantity * item.Product_id.price for item in obj.items.all())
        return "{:.2f}".format(total)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["client", "client_email", "amount", "mode"]
