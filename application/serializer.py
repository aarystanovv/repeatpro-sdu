from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'username', 'password', 'avatar', 'age', 'gender', 'phone', 'rating')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        print('212121')
        user = UserProfile.objects.create_user(**validated_data)
        return user