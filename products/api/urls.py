from django.urls import path, include
from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories',CategoryViewSet)


urlpatterns = [
    path('', include(router.urls)),

    
    # product-subcategory
    path('categories/<int:pk>/subcategory/', SubCategoryListAPIView.as_view(), name='sub-category-list'),
    path('categories/<int:pk>/subcategory-create/', SubCategoryCreateAPIView.as_view(), name='sub-category-create'),
    path('categories/subcategory/<int:pk>/', SubCategoryRetrieveUpdateDestroyAPIView.as_view(),name='sub-category-detail'),

    # product-comments
    path('products/<int:pk>/comments/', CommentsListAPIView.as_view(), name='comments-list'),
    path('products/<int:pk>/comments-create/', CommentsCreateAPIView.as_view(), name='comments-create'),
    path('products/comments/<int:pk>/', CommentsRetrieveUpdateDestroyAPIView.as_view(),name='comments-detail'),
    # product-images

    path('products/<int:pk>/images/', ImagesListAPIView.as_view(), name='images-list'),
    path('products/<int:pk>/images-create/', ImagesCreateAPIView.as_view(), name='images-create'),
    path('products/images/<int:pk>/',ImagesRetrieveUpdateDestroyAPIView.as_view(), name='images-detail'),
    # product-rating
    path('products/<int:pk>/rating/', RatingListAPIView.as_view(), name='rating-list'),
    path('products/<int:pk>/rating-create/', RatingCreateAPIView.as_view(), name='rating-create'),
    path('products/rating/<int:pk>/',RatingRetrieveUpdateDestroyAPIView.as_view(), name='rating-detail'),




]