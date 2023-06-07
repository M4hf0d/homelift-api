from django.shortcuts import render
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import *
from users.models import Customer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from products.models import Product
import json
from .models import *
from products.api.serializers import ProductSerializer
from users.models import Customer
from chargily_epay_django.views import (
    CreatePaymentView,
    PaymentConfirmationView,
    PaymentObjectDoneView,
    FakePaymentView,
)
from django.db.models import Sum, Count
from datetime import date, timedelta
import django_filters.rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter


class UserOrdersView(APIView):
    def get(self, request, user_id):
        oCustomer = Customer.objects.get(pk=user_id)
        orders = Order.objects.filter(customer=oCustomer)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["customer__fullname", "email"]
    ordering_fields = ["total_amount", "customer__fullname"]


class AddToCartAPIView(CreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        # Return an empty queryset since we are creating a new item
        return Item.objects.none()

    def post(self, request, user_id, product_id):
        product_id = Product.objects.get(id=product_id)
        # quantity = request.POST["Quantity"]
        quantity = request.data["Quantity"]
        if int(quantity) <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        if int(quantity) > product_id.quantity:
            raise serializers.ValidationError("Quantity not available for "  + product_id.name)
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


class CartCheckView(APIView):
    def get(self, request, user_id):
        cart = Cart.objects.get(
            Customer_id=user_id
        )  # Retrieve the cart for the authenticated user

        if cart:
            for item in cart.items.all():
                if item.Quantity > item.Product_id.quantity:
                    print(item.Product_id.name)
                    return Response(
                        {
                            "error": f"{item.Product_id.name}'s Quantity exceeds available stock."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response({"message": "All Set."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "User Doesnt have a cart"}, status=status.HTTP_400_BAD_REQUEST
            )


class CheckoutView(APIView):
    def post(self, request, user_id):

        cart = Cart.objects.get(
            Customer_id=user_id
        )  # Retrieve the cart for the authenticated user
        if cart.items.count() == 0:
            return Response(
                {"error": "Order Can't Be empty"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not cart:
            return Response(
                {"error": "User Doesn't have a cart"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for item in cart.items.all():
            if item.Quantity > item.Product_id.quantity:
                print(item.Product_id.name)
                return Response(
                    {
                        "error": f"{item.Product_id.name}'s Quantity exceeds available stock."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Subtract the item quantity from the available stock
            item.Product_id.quantity -= item.Quantity
            item.Product_id.save()

        # Create an order with the items from the cart
        customer = cart.Customer_id
        order = Order.objects.create(customer=customer)
        order.items.set(cart.items.all())
        order.calculate_total_amount()

        # Clear the cart
        cart.items.clear()

        # Return a success response
        return Response({"message": "Checkout successful."}, status=status.HTTP_200_OK)


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


from .forms import PaymentForm


class CreatePayment(CreatePaymentView):
    payment_create_faild_url = ""
    template_name: str = "payment/payment.html"
    form_class = PaymentForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_id = self.kwargs.get("user_id")
        customer = Customer.objects.get(id=user_id)
        order_id = self.kwargs.get("order_id")
        order = Order.objects.get(id=order_id)
        form.initial = {
            "client": customer.fullname,
            "client_email": customer.email,
            "amount": order.total_amount,
        }
        return form


class PaymentStatus(PaymentObjectDoneView):
    model = Payment
    template_name: str = "payment/payment-status.html"


class ConfirmPayment(PaymentConfirmationView):
    model = Payment


class FakePayment(FakePaymentView):
    model = Payment


# stats
class Cards(APIView):
    def get(self, request):
        Revenue = Order.objects.aggregate(total_amount=Sum("total_amount"))[
            "total_amount"
        ]
        Total_Customer = Customer.objects.filter(role=Customer.CLIENT).count()
        Total_Users = Customer.objects.all().count()
        withorders = (
            Customer.objects.filter(role=Customer.CLIENT)
            .filter(orders__isnull=False)
            .distinct()
            .count()
        )
        Total_Price = Order.objects.aggregate(Profit=Sum("items__Product_id__price"))[
            "Profit"
        ]
        Total_Bulk = Order.objects.aggregate(Bulk=Sum("items__Product_id__bulk_price"))[
            "Bulk"
        ]

        if not Total_Price:
            Total_Price = 0
        if not Total_Bulk:
            Total_Bulk = 0
        if not Revenue:
            Revenue = 0

        Resp = {
            "Revenue": Revenue,
            "Total_Customer": Total_Customer,
            "Conversion_rate": withorders * 100 / Total_Customer,
            "Total_Profit": Total_Price - Total_Bulk,
        }
        return Response(Resp)


class WeeklyOrders(APIView):
    def get(self, request):
        today = date.today()
        start_week = today - timedelta(days=today.weekday() + 2)

        saturday = Order.objects.filter(created_at__date=start_week).count()
        sunday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=1)
        ).count()
        monday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=2)
        ).count()
        tuesday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=3)
        ).count()
        wednesday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=4)
        ).count()
        thursday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=5)
        ).count()
        friday = Order.objects.filter(
            created_at__date=start_week + timedelta(days=6)
        ).count()
        Resp = {
            "saturday": saturday,
            "sunday": sunday,
            "monday": monday,
            "tuesday": tuesday,
            "wednesday": wednesday,
            "thursday": thursday,
            "friday": friday,
        }
        return Response(Resp)


class BestSeller(APIView):
    def get(self, request):
        q = Product.objects.annotate(sales=Count("PRODUCT__order_item")).order_by(
            "-sales"
        )[:5]
        serializer = ProductSerializer(q, many=True)

        i = 0
        for element in serializer.data:
            element["Times_Sold"] = q[i].sales
            json.dumps(element)
            i = i + 1
        return Response(serializer.data)


class LatestProducts(APIView):
    def get(self, request):
        q = Order.objects.all().order_by("-created_at")

        latest_products = [
            item.Product_id for order in q for item in order.items.all()
        ][:10]
        unique = []
        seen = set()

        for prodd in latest_products:
            if prodd not in seen:
                unique.append(prodd)
                seen.add(prodd)
        serializer = ProductSerializer(unique, many=True)
        return Response(serializer.data)
