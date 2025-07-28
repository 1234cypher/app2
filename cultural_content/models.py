# cultural_content/models.py
from django.conf import settings
from django.db import models

class CulturalContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('music', 'Musique'),
        ('video', 'Vidéo'),
        ('expression', 'Expression'),
        ('fact', 'Fait culturel'),
    ]
    
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    language = models.CharField(max_length=2)
    difficulty_level = models.CharField(max_length=2)
    content = models.TextField()
    translation = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    media_file = models.FileField(upload_to='cultural/', null=True, blank=True)
    tags = models.CharField(max_length=200, blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserContentInteraction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.ForeignKey(CulturalContent, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'content']
