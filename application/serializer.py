from rest_framework import serializers
from .models import UserProfile, UserNotification, PaymentAccounts


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'firstname', 'lastname', 'password', 'avatar', 'age', 'gender', 'phone', 'rating')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        print('212121')
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ('id', 'user_id', 'tutor_id', 'status', 'text', 'price')




