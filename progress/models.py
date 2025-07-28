# progress/models.py
from django.conf import settings
from django.db import models

class LearningProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField()
    conversations_count = models.PositiveIntegerField(default=0)
    study_time_minutes = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)
    words_learned = models.PositiveIntegerField(default=0)
    challenges_completed = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

class Vocabulary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vocabulary')
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    language = models.CharField(max_length=2)
    pronunciation = models.CharField(max_length=200, blank=True)
    difficulty_level = models.PositiveIntegerField(default=1)
    times_encountered = models.PositiveIntegerField(default=1)
    times_correct = models.PositiveIntegerField(default=0)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'word', 'language']
