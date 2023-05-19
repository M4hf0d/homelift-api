from django.urls import path, include

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
]
