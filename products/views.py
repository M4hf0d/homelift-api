from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from rest_framework import filters

# Create your views here.


class ApiOverviewAV(APIView):

    def get(self, request):
        api_urls = {
            'Status': '✅',
        }
        return Response(api_urls)
    
    # permission_classes = [IsAuthenticated]