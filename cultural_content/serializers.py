# cultural_content/serializers.py
from rest_framework import serializers
from .models import CulturalContent, UserContentInteraction

class CulturalContentSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    
    class Meta:
        model = CulturalContent
        fields = '__all__'
    
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            interaction = UserContentInteraction.objects.filter(
                user=user, content=obj
            ).first()
            return interaction.liked if interaction else False
        return False
    
    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            interaction = UserContentInteraction.objects.filter(
                user=user, content=obj
            ).first()
            return interaction.bookmarked if interaction else False
        return False

class UserContentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContentInteraction
        fields = '__all__'