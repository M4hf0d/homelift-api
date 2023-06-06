from django.urls import path, include
from django.conf import settings
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"orders", OrdersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("weekltyorders/",  WeeklyOrders.as_view(), name="WeeklyOrders"),
    path("bestseller/",  BestSeller.as_view(), name="BestSeller"),
    path("cards/",  Cards.as_view(), name="Cards"),
    path("latestproducts/",  LatestProducts.as_view(), name="LatestProducts"),

    path(
        "<int:user_id>/<int:product_id>/addtocart/",
        AddToCartAPIView.as_view(),
        name="add_to_cart",
    ),
    path("<int:user_id>/view-cart/", CartCheckAV.as_view(), name="check_cart"),
    path("<int:user_id>/verify-cart/", CartCheckView.as_view(), name="verify_cart"),
    path("<int:user_id>/checkout/", CheckoutView.as_view(), name="checkout"),
    path("<int:user_id>/MyOrders/", UserOrdersView.as_view(), name="My-Orders"),
    path(
        "<int:user_id>/view-cart/<int:pk>/",
        ItemDetailsAV.as_view(),
        name="Cart_details",
    ),
    path("confirm-payment/", 
         ConfirmPayment.as_view(), 
         name="confirm-payment"),
    path("cart/<int:order_id>/<int:user_id>/pay/",
         CreatePayment.as_view(),
         name="create-payment"),
    path(
        "payment-status/<slug:invoice_number>/",
        PaymentStatus.as_view(),
        name="payment-status",
    ),
    
]

if settings.DEBUG: 
    urlpatterns = urlpatterns + [
        path(
            "fake-payment/<slug:invoice_number>/",
            FakePayment.as_view(),
            name="fake-payment",
        ),
]
