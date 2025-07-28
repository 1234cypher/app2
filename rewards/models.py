# rewards/models.py
from django.conf import settings
from django.db import models

class Badge(models.Model):
    CATEGORY_CHOICES = [
        ('conversation', 'Conversation'),
        ('vocabulary', 'Vocabulaire'),
        ('grammar', 'Grammaire'),
        ('pronunciation', 'Prononciation'),
        ('streak', 'Série'),
        ('cultural', 'Culture'),
        ('achievement', 'Accomplissement'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50)  # Icon name or emoji
    requirement_value = models.PositiveIntegerField()
    xp_reward = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']

class XPTransaction(models.Model):
    ACTIVITY_CHOICES = [
        ('conversation', 'Conversation'),
        ('challenge', 'Défi'),
        ('badge', 'Badge'),
        ('streak', 'Série'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_transactions')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    xp_amount = models.IntegerField()
    description = models.CharField(max_length=200)
    reference_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
