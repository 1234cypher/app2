# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    LANGUAGE_CHOICES = [
        ('fr', 'Français'),
        ('en', 'English'),
        ('es', 'Español'),
        ('de', 'Deutsch'),
        ('zh', '中文'),
        ('ja', '日本語'),
    ]
    
    LEVEL_CHOICES = [
        ('A1', 'Débutant'),
        ('A2', 'Élémentaire'),
        ('B1', 'Intermédiaire'),
        ('B2', 'Intermédiaire avancé'),
        ('C1', 'Avancé'),
        ('C2', 'Maîtrise'),
    ]
    
    native_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='fr')
    target_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    current_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default='A1')
    total_xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    premium_expires_at = models.DateTimeField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    notifications_enabled = models.BooleanField(default=True)
    reminder_time = models.TimeField(default='19:00')
    dark_mode = models.BooleanField(default=False)
    voice_speed = models.FloatField(default=1.0)
    auto_translation = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
