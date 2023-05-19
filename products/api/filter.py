import django_filters.rest_framework as filters

from ..models import Product


class ProductFilter(filters.FilterSet):

    price_exact = filters.NumberFilter(field_name="price", lookup_expr="exact")
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    archived = filters.BooleanFilter(field_name="archived")

    class Meta:
        model = Product
        fields = ["price_exact", "min_price", "max_price", "archived"]
