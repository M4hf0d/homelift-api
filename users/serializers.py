from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Customer 
from .utils import Util 

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse



        
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'fullname','phone_number', 'username','email', 'password','payment_info','wilaya','daira','mairie','street','addresse_line','code_postal']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta :    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

        fields = [ 'fullname','phone_number', 'username','email', 'password','payment_info','wilaya','daira','mairie','street','addresse_line','code_postal']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    
    def save(self):

        password = self.validated_data['password']
        fullname = self.validated_data['fullname']
        wilaya = self.validated_data['wilaya']
        daira = self.validated_data['daira']
        mairie = self.validated_data['mairie']
        street = self.validated_data['street']
        address_line = self.validated_data['address_line']
        code_postal = self.validated_data['code_postal']

        if Customer.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        

        if Customer.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error': 'Phone Number already exists!'})

        account = Customer(email=self.validated_data['email'], phone_number=self.validated_data['phone_number'], fullname = fullname,wilaya=wilaya,daira=daira,mairie=mairie,street=street,address_line=address_line,code_postal=code_postal)
        account.set_password(password)
        account.save()

        return account
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email 
        token['phone_number'] = user.phone_number 
        token['fullname'] = user.fullname 
        return token
    

    
    
    
    
    
    
    
    
    
    
    
# Password_reset_serializers

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    
    class Meta :
        fields=['email']
        
    # def validate(self, attrs):
            # email = attrs['data'].get('email','')
            # if Customer.objects.filter(email=email).exists():
            #     user = Customer.objects.get(email=email)
            #     uidb64 = urlsafe_base64_encode(user.id)
            #     token = PasswordResetTokenGenerator().make_token(user)
            #     current_site = get_current_site( 
            #                          request=attrs['data'].get('request')).domain
            #     relativeLink = reverse(
            #         'password_reset_confirm',kwargs={'uidb64':uidb64 , 'token':token})
            #     absurl = 'https://'+current_site+relativeLink
            #     email_body = 'Hi'+Customer.fullname+'Use the link below so you can reset your password \n' + absurl
            #     data={'email_body': email_body,
            #           'to_email': user.email,
            #           'email_subject':'Verify your email'}
                
            #     Util.send_email(data)
            
            # return super().validate(attrs)
    
class SetNewPasswordSerializer (serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    
    class Meta:
        fields=['password','token','uidb64']
        
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            
            id = force_str(urlsafe_base64_decode(uidb64))
            user= Customer.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise AuthenticationFailed('The reset link is invalid',401)
            
            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid',401)
            
        return super().validate(attrs)
    
