# challenges/models.py
from django.conf import settings
from django.db import models

class DailyChallenge(models.Model):
    CHALLENGE_TYPE_CHOICES = [
        ('conversation', 'Conversation'),
        ('vocabulary', 'Vocabulaire'),
        ('pronunciation', 'Prononciation'),
        ('listening', 'Écoute'),
        ('translation', 'Traduction'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPE_CHOICES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    target_language = models.CharField(max_length=2)
    xp_reward = models.PositiveIntegerField(default=50)
    estimated_duration = models.PositiveIntegerField()  # in minutes
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserChallenge(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigné'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='channels_challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='assigned')
    progress = models.PositiveIntegerField(default=0)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = [['user', 'challenge']]

