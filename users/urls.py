from django.urls import path,include

from .views import registration_view, logout_view,CustomTokenObtainPairView,CustomerVS


from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('customer', CustomerVS, basename='customer')

urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]