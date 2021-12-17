from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import Profile

PASSWORD_REGEX = RegexValidator(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})')

PHONE_NUMBER_REGEX = RegexValidator(r'^09(0[1-5]|[1 3]\d|2[0-2]|98)\d{7}$')


class RegisterEmailSerializer(serializers.ModelSerializer):
    """
    Register user with email,password
    """
    username = serializers.CharField(min_length=8, max_length=30)
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30, validators=[PASSWORD_REGEX])

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone', 'password')


class RegisterPhoneSerializer(serializers.ModelSerializer):
    """
    Register user with phone,password
    """
    username = serializers.CharField(min_length=8, max_length=30)
    phone = serializers.CharField(validators=[PHONE_NUMBER_REGEX])
    password = serializers.CharField(min_length=8, max_length=30, validators=[PASSWORD_REGEX])

    class Meta:
        model = get_user_model()
        fields = ('username', 'phone', 'password')


class LoginSerializer(serializers.ModelSerializer):
    """
    Login user with email and password
    """
    username = serializers.CharField()
    password = serializers.CharField(max_length=30)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class ForgotPasswordEmailSerializer(serializers.Serializer):
    """
    user can enter email and send token to your email
    """
    email = serializers.EmailField()


class ForgotPasswordPhoneSerializer(serializers.Serializer):
    """
    user can enter phone and send token to your phone number
    """
    phone = serializers.CharField()


class ChangePasswordWithForgotTokenSerializer(serializers.Serializer):
    """
    user must enter token that send to email or phone , password for change password
    """
    password = serializers.CharField(max_length=30)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField(validators=[PASSWORD_REGEX])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')

    def update(self, instance, validated_data):
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        if first_name:
            instance.user.first_name = first_name

        if last_name:
            instance.user.last_name = last_name

        instance.user.save()
        instance.save()
        return super(ProfileUpdateSerializer, self).update(instance, validated_data)


class AddEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class AddPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[PHONE_NUMBER_REGEX])
