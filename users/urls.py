from django.urls import path,include

from .views import *


from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()


urlpatterns = [
    # path('login/', obtain_auth_token, name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),



    
    
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name='request_reset_email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), 
                                                             name='password_reset_confirm'),
    path('password-reset-complete/',SetNewPasswordAPIView.as_view(), name='password_reset_complete'),
    
    path('<int:pk>/view-profile/',ProfileDetailsAV.as_view(), name='view_profile'),
    path('staff-list/',StaffListAPIView.as_view(), name='staff-list'),
    path('staff-list/add/',StaffCreateAPIView.as_view(), name='add-staff'),
    path('staff-list/<int:pk>/',StaffRetrieveUpdateDestroyAPIView.as_view(), name='staff-details'),

    path('customer-list/',CustomerListAPIView.as_view(), name='customer-list'),
    path('customer-list/<int:pk>/',CustomerRetrieveUpdateDestroyAPIView.as_view(), name='customer-details'),

    path('blocked/',CustomerListAPIView.as_view(), name='blocked-users-list'),


]