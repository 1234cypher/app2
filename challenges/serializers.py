# challenges/serializers.py
from rest_framework import serializers
from .models import DailyChallenge, UserChallenge

class DailyChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyChallenge
        fields = '__all__'

class UserChallengeSerializer(serializers.ModelSerializer):
    challenge = DailyChallengeSerializer(read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = UserChallenge
        fields = '__all__'
    
    def get_progress_percentage(self, obj):
        return min(obj.progress, 100)