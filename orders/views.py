from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import ItemSerializer, CartSerializer
from .models import Item, Cart
from users.models import Customer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from products.models import Product
from .models import *

# class AddToCart(generics.CreateAPIView):

#     serializer_class=ItemSerializer
#     def get_queryset(self):
#         return Item.objects.all()

#     def perform_create(self, serializer):
#         user_id = self.kwargs.get('user_id')
#         Product_id = self.kwargs.get('product_id')
#         quantity = self.request.data['Quantity']
#         Cart.objects.get_or_create(Customer_id=Customer.objects.get(pk=user_id))
#         Cart_id=Cart.objects.get(Customer_id=Customer.objects.get(pk=user_id)).pk
#         serializer.save(Cart_id,Product_id,quantity)


class AddToCartAPIView(CreateAPIView):
    serializer_class = ItemSerializer

    def post(self, request, user_id, product_id):
        # product_id = product_id
        # quantity = request.POST["Quantity"]
        quantity = request.data["Quantity"]
        if int(quantity) <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")

        cster = Customer.objects.get(id=user_id)
        try:
            cart = Cart.objects.get(Customer_id=cster)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(Customer_id=cster)
        item = Item.objects.filter(carti__id=cart.id, Product_id=product_id).first()
        if item:
            item.Quantity += int(quantity)
            item.save()
        else:
            # item = Item.objects.create(Product_id_id=product_id, Quantity=quantity)
            # cart.items.add(item)
            item = Item.objects.create(Product_id_id=product_id, Quantity=quantity)
            item.carti.set([cart])

        serializer = self.serializer_class(item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class CartCheckAV(APIView):
#     def get(self, request, user_id):
#         print(f'user_id: {user_id}')
#         try:
#             cart = Cart.objects.get(Customer_id=user_id)
#         except Cart.DoesNotExist:
#             print('Cart does not exist')
#             return Response({'message': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
#         items = Item.objects.filter(Cart_id=cart.id)
#         serializer = CartSerializer( many=True)
#         return Response(serializer.data)


class CartCheckAV(ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Cart.objects.filter(Customer_id=user_id)


class ItemDetailsAV(APIView):
    def get(self, request, pk, user_id):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(
                {"error": "Item Not Found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def patch(self, request, pk, user_id):
        item = Item.objects.get(pk=pk)
        serializer = ItemSerializer
        quantity = request.data["Quantity"]
        if int(quantity) > Product.objects.get(name=item.Product_id).quantity:
            return Response(
                {"error": "non valid quantity"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            item.Quantity = int(quantity)
            item.save()
            serializer = ItemSerializer(item)
            return Response(serializer.data)

    def delete(self, request, pk, user_id):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
