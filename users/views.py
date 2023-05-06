from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework import mixins,viewsets
from rest_framework import generics


from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from djoser.views import UserViewSet



from .serializers import (RegistrationSerializer,MyTokenObtainPairSerializer,
                          CustomerSerializer,RequestPasswordResetEmailSerializer,
                          SetNewPasswordSerializer)

from .models import Customer

from .utils import Util 

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse





class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    response = Response()
    response.delete_cookie('refresh_token')
    data = {
            'response': 'Logged out!',
        }
    return Response(data)


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = "Registration Successful!"
            data['phone_number'] = account.phone_number
            data['email'] = account.email   
            data['wilaya']= account.wilaya
            data['daira'] = account.daira
            data['street'] = account.street
            data ['address_line'] = account.address_line
            data['code_postal'] = account.code_postal

            # token = Token.objects.get(user=account).key
            # data['token'] = token

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
       
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)

class CustomerVS(mixins.ListModelMixin,
              mixins.RetrieveModelMixin,
              viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    

# Reset_password_views

class RequestPasswordResetEmail(generics.GenericAPIView):
    
    serializer_class = RequestPasswordResetEmailSerializer
    
    def post(self,request):
        
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if Customer.objects.filter(email=email).exists():
                user = Customer.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site( 
                                     request=request).domain
                relativeLink = reverse(
                    'password_reset_confirm',kwargs={'uidb64':uidb64 , 'token':token})
                absurl = 'http://'+current_site+relativeLink
                email_body = 'Use the link below so you can reset your password \n' + absurl
                data={'email_body': email_body,
                      'to_email': user.email,
                      'email_subject':'Reset you password'}
                
                
                Util.send_email(data)
                return Response({'success' :
                        'We have sent you a link to reset your password , please check your email'},
                         status=status.HTTP_200_OK)
        else: 
            return Response('This email does not exist , please enter your registration email' )
        

        
class PasswordTokenCheckAPI(generics.GenericAPIView):
    
    def get(self,request,uidb64,token):
        
        try:
            id= smart_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(id=id)
            
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error' : 'Token is not valid, please request a new one.'})
            
            return Response({'success':True,'message':'Credentials Valid','uidb64':uidb64,'token':token},
                             status=status.HTTP_200_OK)
            
            
        except DjangoUnicodeDecodeError as identifier :
            if not PasswordResetTokenGenerator().check_token(user): 
                return Response({'error' : 'Token is not valid, please request a new one.'})
            
            


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    
    def put (self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True,'message':'Password Reset Success'}, 
                        status=status.HTTP_200_OK)

