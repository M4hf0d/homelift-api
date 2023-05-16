from rest_framework import serializers
from .models import Item,Cart
from products.models import Product

class ItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="Product_id.name", read_only = True)
    unit_price = serializers.SerializerMethodField()
    items_price = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ['id','Product_id','Quantity','Created_at','product_name','items_price','unit_price']

    def validate_Quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be a positive integer')
        return value 

    def get_items_price(self,obj): 
        return int(obj.Product_id.price) * obj.Quantity
    def get_unit_price(self,obj):
        return obj.Product_id.price
    # def save(self,Product_id, data):
    #     theitem = self.Item_set.items.filter(Product_id == Product_id)

    #     if theitem : 
    #         theitem.Quantity += data['Quantity']

    #     theitem.save()

    #     return theitem
    
    


class CartSerializer(serializers.ModelSerializer):
    # items = serializers.CharField(source="items.Product_id.name", many= True)
    items = ItemSerializer()
    # total_amount = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = "__all__"
    # def get_total_amount(self, obj):
    #     if obj.items is not None:
    #         total = sum(int(item.Quantity) * int(item.Product_id.price) for item in obj.items)
    #         return '{:.2f}'.format(total)
    #     else:
    #         return '0.00'



# class AddToCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Item
#         fields=['Quantity']

#     def save(self,Cart_id,Product_id,Quantity):

#         item_queryset = Item.objects.filter(Product_id=Product_id,Cart_id=Cart_id)

#         if item_queryset.exists():
#             raise serializers.ValidationError("already Added , just modify the quantity or cancel")

#         if int(Quantity) > Product.objects.get(pk=Product_id).quantity :
#             raise serializers.ValidationError("Unavailable quantity")

#         item = Item(Cart_id=Cart.objects.get(pk=Cart_id),Quantity=Quantity,Product_id=Product.objects.get(pk=Product_id))
#         item.save()

#         return item
    