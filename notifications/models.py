# notifications/models.py
from django.conf import settings
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('reminder', 'Rappel'),
        ('achievement', 'Accomplissement'),
        ('challenge', 'Défi'),
        ('streak', 'Série'),
        ('social', 'Social'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
