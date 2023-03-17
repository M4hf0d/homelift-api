from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Costumer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Costumer
        fields = ['first_name', 'last_name','phone_number', 'username','email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if Costumer.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        

        if Costumer.objects.filter(phone_number=self.validated_data['phone_number']).exists():
            raise serializers.ValidationError({'error': 'Phone Number already exists!'})

        account = Costumer(email=self.validated_data['email'], phone_number=self.validated_data['phone_number'])
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
        token['first_name'] = user.first_name 
        token['last_name'] = user.username 


        
        return token