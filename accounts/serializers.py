# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreferences

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'native_language', 'target_language', 
                 'current_level', 'total_xp', 'current_streak', 'best_streak', 
                 'is_premium', 'avatar', 'date_joined']
        read_only_fields = ['id', 'total_xp', 'date_joined']

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = '__all__'
        read_only_fields = ['user']
