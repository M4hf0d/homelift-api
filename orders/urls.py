from django.urls import path, include
from django.conf import settings
from .views import *

urlpatterns = [
    path(
        "<int:user_id>/<int:product_id>/addtocart/",
        AddToCartAPIView.as_view(),
        name="add_to_cart",
    ),
    path("<int:user_id>/view-cart/", CartCheckAV.as_view(), name="check_cart"),
    path(
        "<int:user_id>/view-cart/<int:pk>/",
        ItemDetailsAV.as_view(),
        name="Cart_details",
    ),
    path("confirm-payment/", 
         ConfirmPayment.as_view(), 
         name="confirm-payment"),
    path("cart/pay/",
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
