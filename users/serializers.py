from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Customer
from .utils import Util
from .models import Customer
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "fullname",
            "email",
            "phone_number",
            "wilaya",
            "daira",
            "mairie",
            "street",
            "addresse_line",
            "code_postal",
            "role",
            "blocked",
            "profile_picture",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        customer = Customer(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "fullname",
            "email",
            "phone_number",
            "wilaya",
            "daira",
            "mairie",
            "street",
            "addresse_line",
            "code_postal",
            "role",
            "blocked",
            "profile_picture",
        ]


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "username",
            "fullname",
            "email",
            "phone_number",
            "wilaya",
            "daira",
            "mairie",
            "street",
            "addresse_line",
            "code_postal",
            "role",
            "blocked",
            "profile_picture",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Customer
        fields = [
            "fullname",
            "phone_number",
            "username",
            "email",
            "password",
            "wilaya",
            "daira",
            "mairie",
            "street",
            "addresse_line",
            "code_postal",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self):

        password = self.validated_data["password"]
        fullname = self.validated_data["fullname"]
        wilaya = self.validated_data["wilaya"]
        daira = self.validated_data["daira"]
        mairie = self.validated_data["mairie"]
        street = self.validated_data["street"]
        address_line = self.validated_data["address_line"]
        code_postal = self.validated_data["code_postal"]

        if Customer.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists!"})

        if Customer.objects.filter(
            phone_number=self.validated_data["phone_number"]
        ).exists():
            raise serializers.ValidationError({"error": "Phone Number already exists!"})

        account = Customer(
            email=self.validated_data["email"],
            phone_number=self.validated_data["phone_number"],
            fullname=fullname,
        )
        account.set_password(password)
        account.save()

        return account


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["phone_number"] = user.phone_number
        token["fullname"] = user.fullname
        token["id"] = user.id
        token["role"] = user.role
        token["blocked"] = user.blocked
        return token


from djoser.serializers import TokenSerializer


class CustomTokenSerializer(TokenSerializer):
    blocked = serializers.BooleanField()

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context["user"]
        data["blocked"] = user.blocked
        return data


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()
        except Exception as e:
            raise AuthenticationFailed("The reset link is invalid", 401)

        return super().validate(attrs)
