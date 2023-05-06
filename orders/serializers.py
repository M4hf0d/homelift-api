from rest_framework import serializers
from .models import Item,Cart
from products.models import Product

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id','Cart_id','Product_id','Quantity','Created_at']   
  
        
class CartSerializer(serializers.ModelSerializer):
    Items = ItemSerializer(many=True,)
    class Meta:
        model = Cart
        fields = "__all__"

class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Item
        fields=['Quantity']
        
    def save(self,Cart_id,Product_id,Quantity):
        
        item_queryset = Item.objects.filter(Product_id=Product_id,Cart_id=Cart_id)

        if item_queryset.exists():
            raise serializers.ValidationError("already Added , just modify the quantity or cancel")
        
        if int(Quantity) > Product.objects.get(pk=Product_id).quantity :
            raise serializers.ValidationError("Unavailable quantity")

        item = Item(Cart_id=Cart.objects.get(pk=Cart_id),Quantity=Quantity,Product_id=Product.objects.get(pk=Product_id))
        item.save()

        return item
    