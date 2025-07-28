# progress/serializers.py
from rest_framework import serializers
from .models import LearningProgress, Vocabulary

class LearningProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningProgress
        fields = '__all__'
        read_only_fields = ['user']

class VocabularySerializer(serializers.ModelSerializer):
    mastery_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Vocabulary
        fields = '__all__'
        read_only_fields = ['user', 'times_encountered', 'times_correct']
    
    def get_mastery_percentage(self, obj):
        if obj.times_encountered == 0:
            return 0
        return min((obj.times_correct / obj.times_encountered) * 100, 100)
