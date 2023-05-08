from django.contrib import admin
from .models import Product , Category ,ArchivedProduct, ProductComment , ProductRating ,ProductImage , SubCategory
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ProductImage)
admin.site.register(ProductRating)
admin.site.register(ProductComment)
admin.site.register(ArchivedProduct)

