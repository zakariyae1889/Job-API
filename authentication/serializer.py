from rest_framework import serializers
from .models import Profile, User
from django.db import transaction, IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',"roles", 'password', 'password_confirmation']
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True, 'required': True, 'allow_blank': False, 'min_length': 8},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError({"password_confirmation": "Passwords do not match"})
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["user", "phone", "country", "city", "bio"]

    def validate(self, data):
        user_data = data.get('user', {})
        username = user_data.get('username')
        email = user_data.get('email')

        if User.objects.filter( Q(email__iexact=email) | Q(username__iexact=username)).exists():
            raise serializers.ValidationError({"error": "This Email or  Username already exists"})
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')

        try:
            with transaction.atomic():
                user = User.objects.create_user(**user_data)
                user.set_password(password)
                user.save()
                profile = Profile.objects.create(user=user, **validated_data)
                return profile

        except IntegrityError:
            raise serializers.ValidationError({"details": "An error occurred while creating the account"})


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords must match."})
        
        validate_password(attrs['new_password'], user=self.context['request'].user)
        
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError({"new_password": "New password cannot be the same as the old password."})
        
        return attrs
