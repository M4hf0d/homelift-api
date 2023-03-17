from django.urls import path, include
from .views import *



urlpatterns = [

    path("", ApiOverviewAV.as_view(), name='Overview'),
   
]