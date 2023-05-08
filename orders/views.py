from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ItemSerializer,CartSerializer
from .models import Item,Cart
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from products.models import Product

class AddToCart(generics.CreateAPIView):

    serializer_class=ItemSerializer
    def get_queryset(self):
        return Item.objects.all() 

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')
        product_id = self.kwargs.get('product_id') 
        quantity = self.request.POST.get('Quantity')
        cart, _ = Cart.objects.get_or_create(Customer_id=user_id)
        serializer.save(Cart_id=cart, Product_id=Product.objects.get(pk=product_id), Quantity=quantity)


class CartCheckAV(APIView):
    def get(self, request,user_id):
        items = Item.objects.filter(Cart_id=(Cart.objects.get(Customer_id=user_id)).id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)





class ItemDetailsAV(APIView):
    def get(self, request,pk,user_id):
        try:
           item = Item.objects.get(pk=pk)
        except  Item.DoesNotExist:
           return Response({'error':'Item Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer=ItemSerializer(item)
        return Response(serializer.data)
    def put(self,request,pk,user_id):
        item = Item.objects.get(pk=pk)
        serializer=ItemSerializer
        quantity=request.data['Quantity']
        if int(quantity) > Product.objects.get(name=item.Product_id).quantity :
            return Response({'error':'non valid quantity'},status=status.HTTP_400_BAD_REQUEST)
        else:
            item.Quantity=int(quantity)
            item.save()
            serializer=ItemSerializer(item)
            return Response(serializer.data)

    def delete(self,request,pk,user_id):
            item=Item.objects.get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# class ItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Item
#     serializer_class = UptodateCartSerializer
# class ItemDetailsAV(generics.CreateAPIView):

#     serializer_class=ItemSerializer
#     def get_object(self):
#         queryset = self.get_queryset()

#     def get_queryset(self):
#         pk= self.kwargs.get('pk')
#         return Item.objects.get(pk=pk) 

#     def  perform_update(self, serializer):
#         pk=self.kwargs.get('pk')
#         Product_id = Item.objects.get(pk=pk).Product_id
#         Cart_id = Item.objects.get(pk=pk).Cart_id
#         quantity = self.request.PUT.get('Quantity')
#         serializer.save(Cart_id,quantity,Product_id,)