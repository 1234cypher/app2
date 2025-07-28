# LinguaChat AI - Django Application
# Structure complète du projet

# ========================
# 1. SETTINGS.PY
# ========================

# linguachat/settings.py
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'channels',
    'accounts',
    'conversations',
    'rewards',
    'challenges',
    'progress',
    'cultural_content',
    'notifications',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linguachat.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='linguachat'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Channels Configuration
ASGI_APPLICATION = 'linguachat.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# API Keys Configuration
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
GOOGLE_TRANSLATE_KEY = config('GOOGLE_TRANSLATE_KEY', default='')
GOOGLE_TTS_KEY = config('GOOGLE_TTS_KEY', default='')
ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY', default='')

# File Upload Settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ========================
# 2. MODELS
# ========================

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

# conversations/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Conversation(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Terminée'),
        ('paused', 'En pause'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    duration_seconds = models.PositiveIntegerField(default=0)
    xp_earned = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']

class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('user', 'Utilisateur'),
        ('ai', 'IA'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=4, choices=MESSAGE_TYPE_CHOICES)
    original_text = models.TextField()
    translated_text = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio/', null=True, blank=True)
    pronunciation_score = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']

# rewards/models.py
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xp_transactions')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    xp_amount = models.IntegerField()
    description = models.CharField(max_length=200)
    reference_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# challenges/models.py
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(DailyChallenge, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='assigned')
    progress = models.PositiveIntegerField(default=0)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = [['user', 'challenge', 'assigned_at__date']]

# progress/models.py
class LearningProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabulary')
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

# cultural_content/models.py
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(CulturalContent, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'content']

# notifications/models.py
class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('reminder', 'Rappel'),
        ('achievement', 'Accomplissement'),
        ('challenge', 'Défi'),
        ('streak', 'Série'),
        ('social', 'Social'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# ========================
# 3. SERIALIZERS
# ========================

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

# conversations/serializers.py
from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['conversation', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ['user', 'xp_earned', 'started_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()

# rewards/serializers.py
from rest_framework import serializers
from .models import Badge, UserBadge, XPTransaction

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = '__all__'

class XPTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = XPTransaction
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

# ========================
# 4. SERVICES
# ========================

# services/ai_service.py
import openai
from django.conf import settings
import json

class AIConversationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    def generate_response(self, user_message, conversation_history, user_level, target_language):
        """Generate AI response for conversation"""
        system_prompt = self._build_system_prompt(user_level, target_language)
        messages = self._build_message_history(conversation_history, system_prompt)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Désolé, je ne peux pas répondre pour le moment. Erreur: {str(e)}"
    
    def _build_system_prompt(self, user_level, target_language):
        return f"""Tu es un assistant IA pour l'apprentissage du {target_language}. 
        L'utilisateur a un niveau {user_level}. Adapte tes réponses à son niveau:
        - Utilise un vocabulaire approprié
        - Corrige gentiment les erreurs
        - Encourage l'apprentissage
        - Reste conversationnel et engageant"""
    
    def _build_message_history(self, conversation_history, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history[-10:]:  # Garde les 10 derniers messages
            role = "user" if msg.message_type == "user" else "assistant"
            messages.append({"role": role, "content": msg.original_text})
        return messages

# services/translation_service.py
from google.cloud import translate_v2 as translate
from django.conf import settings

class TranslationService:
    def __init__(self):
        self.client = translate.Client(api_key=settings.GOOGLE_TRANSLATE_KEY)
    
    def translate_text(self, text, target_language, source_language=None):
        """Translate text using Google Translate API"""
        try:
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            return result['translatedText']
        except Exception as e:
            return f"Erreur de traduction: {str(e)}"
    
    def detect_language(self, text):
        """Detect the language of given text"""
        try:
            result = self.client.detect_language(text)
            return result['language']
        except Exception as e:
            return None

# services/speech_service.py
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from django.core.files.base import ContentFile

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def speech_to_text(self, audio_file, language='fr-FR'):
        """Convert speech to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Audio non reconnu"
        except sr.RequestError as e:
            return f"Erreur du service: {str(e)}"
    
    def text_to_speech(self, text, language='fr'):
        """Convert text to speech"""
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            with open(temp_file.name, 'rb') as f:
                audio_content = f.read()
            
            os.unlink(temp_file.name)
            return ContentFile(audio_content, name=f'tts_{hash(text)}.mp3')
        except Exception as e:
            return None

# services/gamification_service.py
from django.utils import timezone
from rewards.models import Badge, UserBadge, XPTransaction
from progress.models import LearningProgress

class GamificationService:
    def __init__(self, user):
        self.user = user
    
    def award_xp(self, activity_type, amount, description, reference_id=None):
        """Award XP to user and update total"""
        transaction = XPTransaction.objects.create(
            user=self.user,
            activity_type=activity_type,
            xp_amount=amount,
            description=description,
            reference_id=reference_id
        )
        
        self.user.total_xp += amount
        self.user.save()
        
        self._check_for_new_badges()
        return transaction
    
    def check_conversation_badges(self, conversation_count):
        """Check if user earned conversation-related badges"""
        conversation_badges = [
            (1, 'first_conversation'),
            (10, 'conversation_starter'),
            (50, 'chatterbox'),
            (100, 'conversation_master'),
        ]
        
        for count, badge_name in conversation_badges:
            if conversation_count == count:
                self._award_badge(badge_name)
    
    def update_streak(self):
        """Update user's learning streak"""
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        # Check if user studied yesterday
        yesterday_progress = LearningProgress.objects.filter(
            user=self.user, date=yesterday
        ).first()
        
        if yesterday_progress and yesterday_progress.study_time_minutes > 0:
            self.user.current_streak += 1
        else:
            self.user.current_streak = 1
        
        if self.user.current_streak > self.user.best_streak:
            self.user.best_streak = self.user.current_streak
        
        self.user.save()
        self._check_streak_badges()
    
    def _check_streak_badges(self):
        """Check for streak-related badges"""
        streak_badges = [
            (3, 'three_day_streak'),
            (7, 'week_warrior'),
            (30, 'monthly_master'),
            (100, 'century_streak'),
        ]
        
        for days, badge_name in streak_badges:
            if self.user.current_streak == days:
                self._award_badge(badge_name)
    
    def _award_badge(self, badge_name):
        """Award a badge to the user"""
        try:
            badge = Badge.objects.get(name=badge_name)
            user_badge, created = UserBadge.objects.get_or_create(
                user=self.user, badge=badge
            )
            if created:
                self.award_xp('badge', badge.xp_reward, f'Badge: {badge.name}', badge.id)
        except Badge.DoesNotExist:
            pass
    
    def _check_for_new_badges(self):
        """Check if user qualifies for any new badges based on XP"""
        xp_badges = [
            (100, 'xp_collector'),
            (500, 'xp_hunter'),
            (1000, 'xp_master'),
            (5000, 'xp_legend'),
        ]
        
        for xp_threshold, badge_name in xp_badges:
            if self.user.total_xp >= xp_threshold:
                try:
                    badge = Badge.objects.get(name=badge_name)
                    if not UserBadge.objects.filter(user=self.user, badge=badge).exists():
                        self._award_badge(badge_name)
                except Badge.DoesNotExist:
                    pass

# ========================
# 5. VIEWS (API)
# ========================

# accounts/views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer, UserPreferencesSerializer
from .models import UserPreferences

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserPreferencesView(generics.RetrieveUpdateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# conversations/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from services.ai_service import AIConversationService
from services.translation_service import TranslationService
from services.speech_service import SpeechService
from services.gamification_service import GamificationService

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user_message = request.data.get('message', '')
    audio_file = request.FILES.get('audio')
    
    # Handle audio input
    if audio_file:
        speech_service = SpeechService()
        user_message = speech_service.speech_to_text(audio_file, 
                                                   f"{request.user.target_language}-{request.user.target_language.upper()}")
    
    if not user_message:
        return Response({'error': 'Message or audio required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save user message
    translation_service = TranslationService()
    translated_message = translation_service.translate_text(
        user_message, request.user.native_language, request.user.target_language
    )
    
    user_msg = Message.objects.create(
        conversation=conversation,
        message_type='user',
        original_text=user_message,
        translated_text=translated_message
    )
    
    # Generate AI response
    ai_service = AIConversationService()
    conversation_history = conversation.messages.all()
    
    ai_response = ai_service.generate_response(
        user_message, conversation_history, 
        request.user.current_level, request.user.target_language
    )
    
    # Translate AI response
    ai_translated = translation_service.translate_text(
        ai_response, request.user.native_language, request.user.target_language
    )
    
    # Generate audio for AI response
    speech_service = SpeechService()
    audio_file = speech_service.text_to_speech(ai_response, request.user.target_language)
    
    ai_msg = Message.objects.create(
        conversation=conversation,
        message_type='ai',
        original_text=ai_response,
        translated_text=ai_translated,
        audio_file=audio_file
    )
    
    # Award XP for conversation
    gamification = GamificationService(request.user)
    gamification.award_xp('conversation', 10, 'Message envoyé', conversation.id)
    
    return Response({
        'user_message': MessageSerializer(user_msg).data,
        'ai_message': MessageSerializer(ai_msg).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_conversation(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    conversation.status = 'completed'
    conversation.completed_at = timezone.now()
    conversation.duration_seconds = request.data.get('duration', 0)
    
    # Calculate XP based on duration and message count
    base_xp = 20
    duration_bonus = min(conversation.duration_seconds // 60, 10) * 5  # 5 XP per minute, max 10 minutes
    message_bonus = conversation.messages.filter(message_type='user').count() * 2
    
    total_xp = base_xp + duration_bonus + message_bonus
    conversation.xp_earned = total_xp
    conversation.save()
    
    # Award XP and check badges
    gamification = GamificationService(request.user)
    gamification.award_xp('conversation', total_xp, 'Conversation terminée', conversation.id)
    
    # Update progress
    from progress.models import LearningProgress
    today = timezone.now().date()
    progress, created = LearningProgress.objects.get_or_create(
        user=request.user, date=today,
        defaults={'conversations_count': 0, 'study_time_minutes': 0, 'xp_earned': 0}
    )
    progress.conversations_count += 1
    progress.study_time_minutes += conversation.duration_seconds // 60
    progress.xp_earned += total_xp
    progress.save()
    
    # Check conversation badges
    total_conversations = Conversation.objects.filter(
        user=request.user, status='completed'
    ).count()
    gamification.check_conversation_badges(total_conversations)
    
    return Response(ConversationSerializer(conversation).data)

# rewards/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Badge, UserBadge, XPTransaction
from .serializers import BadgeSerializer, UserBadgeSerializer, XPTransactionSerializer

class UserBadgesView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user).order_by('-earned_at')

class AvailableBadgesView(generics.ListAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Badge.objects.filter(is_active=True)

class XPHistoryView(generics.ListAPIView):
    serializer_class = XPTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return XPTransaction.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    user = request.user
    today = timezone.now().date()
    
    # Get today's progress
    from progress.models import LearningProgress
    today_progress = LearningProgress.objects.filter(
        user=user, date=today
    ).first()
    
    # Get weekly progress
    week_start = today - timezone.timedelta(days=today.weekday())
    weekly_progress = LearningProgress.objects.filter(
        user=user, date__gte=week_start
    ).aggregate(
        total_xp=models.Sum('xp_earned'),
        total_time=models.Sum('study_time_minutes'),
        total_conversations=models.Sum('conversations_count')
    )
    
    stats = {
        'total_xp': user.total_xp,
        'current_streak': user.current_streak,
        'best_streak': user.best_streak,
        'badges_count': UserBadge.objects.filter(user=user).count(),
        'today': {
            'xp_earned': today_progress.xp_earned if today_progress else 0,
            'study_time': today_progress.study_time_minutes if today_progress else 0,
            'conversations': today_progress.conversations_count if today_progress else 0,
        },
        'this_week': {
            'xp_earned': weekly_progress['total_xp'] or 0,
            'study_time': weekly_progress['total_time'] or 0,
            'conversations': weekly_progress['total_conversations'] or 0,
        }
    }
    
    return Response(stats)

# challenges/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import DailyChallenge, UserChallenge
from .serializers import DailyChallengeSerializer, UserChallengeSerializer

class DailyChallengesView(generics.ListAPIView):
    serializer_class = UserChallengeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        today = timezone.now().date()
        return UserChallenge.objects.filter(
            user=self.request.user,
            assigned_at__date=today
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_daily_challenges(request):
    """Assign daily challenges to user"""
    user = request.user
    today = timezone.now().date()
    
    # Check if challenges already assigned today
    existing_challenges = UserChallenge.objects.filter(
        user=user, assigned_at__date=today
    ).count()
    
    if existing_challenges > 0:
        return Response({'message': 'Challenges already assigned for today'})
    
    # Get appropriate challenges based on user level and language
    available_challenges = DailyChallenge.objects.filter(
        is_active=True,
        target_language=user.target_language
    )
    
    # Select 3 challenges of different types
    challenge_types = ['conversation', 'vocabulary', 'pronunciation']
    assigned_challenges = []
    
    for challenge_type in challenge_types:
        challenge = available_challenges.filter(
            challenge_type=challenge_type
        ).order_by('?').first()
        
        if challenge:
            user_challenge = UserChallenge.objects.create(
                user=user,
                challenge=challenge
            )
            assigned_challenges.append(user_challenge)
    
    return Response(UserChallengeSerializer(assigned_challenges, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_challenge(request, challenge_id):
    try:
        user_challenge = UserChallenge.objects.get(
            id=challenge_id, user=request.user
        )
    except UserChallenge.DoesNotExist:
        return Response({'error': 'Challenge not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user_challenge.status == 'completed':
        return Response({'error': 'Challenge already completed'})
    
    user_challenge.status = 'completed'
    user_challenge.completed_at = timezone.now()
    user_challenge.progress = 100
    user_challenge.save()
    
    # Award XP
    from services.gamification_service import GamificationService
    gamification = GamificationService(request.user)
    gamification.award_xp(
        'challenge', 
        user_challenge.challenge.xp_reward,
        f'Défi terminé: {user_challenge.challenge.title}',
        user_challenge.id
    )
    
    # Update daily progress
    from progress.models import LearningProgress
    today = timezone.now().date()
    progress, created = LearningProgress.objects.get_or_create(
        user=request.user, date=today,
        defaults={'challenges_completed': 0}
    )
    progress.challenges_completed += 1
    progress.save()
    
    return Response(UserChallengeSerializer(user_challenge).data)

# progress/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum, Avg
from .models import LearningProgress, Vocabulary
from .serializers import LearningProgressSerializer, VocabularySerializer

class ProgressHistoryView(generics.ListAPIView):
    serializer_class = LearningProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        days = int(self.request.query_params.get('days', 30))
        start_date = timezone.now().date() - timezone.timedelta(days=days)
        return LearningProgress.objects.filter(
            user=self.request.user,
            date__gte=start_date
        ).order_by('date')

class VocabularyView(generics.ListCreateAPIView):
    serializer_class = VocabularySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Vocabulary.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    
    # Get last 30 days progress
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    recent_progress = LearningProgress.objects.filter(
        user=user, date__gte=thirty_days_ago
    )
    
    stats = recent_progress.aggregate(
        total_xp=Sum('xp_earned'),
        total_study_time=Sum('study_time_minutes'),
        total_conversations=Sum('conversations_count'),
        avg_daily_xp=Avg('xp_earned')
    )
    
    # Get vocabulary stats
    vocabulary_stats = Vocabulary.objects.filter(user=user).aggregate(
        total_words=models.Count('id'),
        mastered_words=models.Count('id', filter=models.Q(times_correct__gte=5))
    )
    
    # Get weekly progress for chart
    weekly_progress = []
    for i in range(7):
        date = timezone.now().date() - timezone.timedelta(days=i)
        day_progress = LearningProgress.objects.filter(
            user=user, date=date
        ).first()
        
        weekly_progress.append({
            'date': date.isoformat(),
            'xp_earned': day_progress.xp_earned if day_progress else 0,
            'study_time': day_progress.study_time_minutes if day_progress else 0
        })
    
    return Response({
        'monthly_stats': stats,
        'vocabulary_stats': vocabulary_stats,
        'weekly_progress': list(reversed(weekly_progress)),
        'current_level': user.current_level,
        'next_level_xp': _calculate_next_level_xp(user.total_xp)
    })

def _calculate_next_level_xp(current_xp):
    """Calculate XP needed for next level"""
    level_thresholds = [0, 100, 300, 600, 1000, 1500, 2500, 4000, 6000, 10000]
    for threshold in level_thresholds:
        if current_xp < threshold:
            return threshold - current_xp
    return 0

# cultural_content/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CulturalContent, UserContentInteraction
from .serializers import CulturalContentSerializer, UserContentInteractionSerializer

class CulturalContentView(generics.ListAPIView):
    serializer_class = CulturalContentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = CulturalContent.objects.filter(
            language=user.target_language
        )
        
        # Filter by premium status
        if not user.is_premium:
            queryset = queryset.filter(is_premium=False)
        
        # Filter by content type if specified
        content_type = self.request.query_params.get('type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        return queryset.order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interact_with_content(request, content_id):
    try:
        content = CulturalContent.objects.get(id=content_id)
    except CulturalContent.DoesNotExist:
        return Response({'error': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
    
    interaction, created = UserContentInteraction.objects.get_or_create(
        user=request.user,
        content=content
    )
    
    # Update interaction based on action
    action = request.data.get('action')
    if action == 'like':
        interaction.liked = not interaction.liked
    elif action == 'bookmark':
        interaction.bookmarked = not interaction.bookmarked
    
    interaction.save()
    
    return Response(UserContentInteractionSerializer(interaction).data)

# ========================
# 6. SERIALIZERS COMPLETS
# ========================

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

# ========================
# 7. URLS CONFIGURATION
# ========================

# linguachat/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/conversations/', include('conversations.urls')),
    path('api/rewards/', include('rewards.urls')),
    path('api/challenges/', include('challenges.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/cultural/', include('cultural_content.urls')),
    path('api/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('preferences/', views.UserPreferencesView.as_view(), name='user-preferences'),
    path('login/', views.login_view, name='login'),
]

# conversations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationListCreateView.as_view(), name='conversation-list'),
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('<int:conversation_id>/message/', views.send_message, name='send-message'),
    path('<int:conversation_id>/complete/', views.complete_conversation, name='complete-conversation'),
]

# rewards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('badges/', views.UserBadgesView.as_view(), name='user-badges'),
    path('badges/available/', views.AvailableBadgesView.as_view(), name='available-badges'),
    path('xp/history/', views.XPHistoryView.as_view(), name='xp-history'),
    path('stats/', views.user_stats, name='user-stats'),
]

# challenges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.DailyChallengesView.as_view(), name='daily-challenges'),
    path('assign/', views.assign_daily_challenges, name='assign-challenges'),
    path('<int:challenge_id>/complete/', views.complete_challenge, name='complete-challenge'),
]

# progress/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.ProgressHistoryView.as_view(), name='progress-history'),
    path('vocabulary/', views.VocabularyView.as_view(), name='vocabulary'),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
]

# cultural_content/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CulturalContentView.as_view(), name='cultural-content'),
    path('<int:content_id>/interact/', views.interact_with_content, name='interact-content'),
]

# ========================
# 8. WEBSOCKET CONSUMERS
# ========================

# conversations/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from services.ai_service import AIConversationService
from services.translation_service import TranslationService

User = get_user_model()

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'conversation_{self.conversation_id}'
        
        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'chat_message':
            await self.handle_chat_message(text_data_json)
        elif message_type == 'typing':
            await self.handle_typing(text_data_json)
    
    async def handle_chat_message(self, data):
        message = data['message']
        user = self.scope['user']
        
        # Save user message to database
        user_message = await self.save_message(
            self.conversation_id, user, 'user', message
        )
        
        # Get AI response
        ai_response = await self.get_ai_response(message, user)
        
        # Save AI message to database
        ai_message = await self.save_message(
            self.conversation_id, user, 'ai', ai_response
        )
        
        # Send messages to group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'user_message': {
                    'id': user_message.id,
                    'text': user_message.original_text,
                    'translation': user_message.translated_text,
                    'timestamp': user_message.timestamp.isoformat()
                },
                'ai_message': {
                    'id': ai_message.id,
                    'text': ai_message.original_text,
                    'translation': ai_message.translated_text,
                    'timestamp': ai_message.timestamp.isoformat()
                }
            }
        )
    
    async def handle_typing(self, data):
        # Broadcast typing indicator
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'typing_indicator',
                'is_typing': data['is_typing']
            }
        )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'user_message': event['user_message'],
            'ai_message': event['ai_message']
        }))
    
    async def typing_indicator(self, event):
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing_indicator',
            'is_typing': event['is_typing']
        }))
    
    @database_sync_to_async
    def save_message(self, conversation_id, user, message_type, text):
        conversation = Conversation.objects.get(id=conversation_id)
        
        # Translate message
        translation_service = TranslationService()
        if message_type == 'user':
            translated_text = translation_service.translate_text(
                text, user.native_language, user.target_language
            )
        else:
            translated_text = translation_service.translate_text(
                text, user.native_language, user.target_language
            )
        
        return Message.objects.create(
            conversation=conversation,
            message_type=message_type,
            original_text=text,
            translated_text=translated_text
        )
    
    @database_sync_to_async
    def get_ai_response(self, user_message, user):
        ai_service = AIConversationService()
        conversation = Conversation.objects.get(id=self.conversation_id)
        conversation_history = list(conversation.messages.all())
        
        return ai_service.generate_response(
            user_message, conversation_history,
            user.current_level, user.target_language
        )

# ========================
# 9. ADMIN CONFIGURATION
# ========================

# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPreferences

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'native_language', 'target_language', 
                   'current_level', 'total_xp', 'is_premium', 'date_joined']
    list_filter = ['native_language', 'target_language', 'current_level', 'is_premium']
    search_fields = ['username', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Language Learning', {
            'fields': ('native_language', 'target_language', 'current_level', 
                      'total_xp', 'current_streak', 'best_streak')
        }),
        ('Premium', {
            'fields': ('is_premium', 'premium_expires_at')
        }),
    )

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ['user', 'notifications_enabled', 'reminder_time', 'dark_mode']
    list_filter = ['notifications_enabled', 'dark_mode']

# conversations/admin.py
from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'status', 'duration_seconds', 
                   'xp_earned', 'started_at']
    list_filter = ['status', 'started_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['started_at', 'completed_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'message_type', 'original_text', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['original_text', 'conversation__user__username']

# rewards/admin.py
from django.contrib import admin
from .models import Badge, UserBadge, XPTransaction

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'requirement_value', 'xp_reward', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge__category', 'earned_at']
    search_fields = ['user__username', 'badge__name']

@admin.register(XPTransaction)
class XPTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'xp_amount', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']

# ========================
# 10. MANAGEMENT COMMANDS
# ========================

# accounts/management/commands/create_badges.py
from django.core.management.base import BaseCommand
from rewards.models import Badge

class Command(BaseCommand):
    help = 'Create initial badges for the application'
    
    def handle(self, *args, **options):
        badges_data = [
            # Conversation badges
            {'name': 'first_conversation', 'description': 'Première conversation terminée', 
             'category': 'conversation', 'icon': '🗣️', 'requirement_value': 1, 'xp_reward': 25},
            {'name': 'conversation_starter', 'description': '10 conversations terminées', 
             'category': 'conversation', 'icon': '💬', 'requirement_value': 10, 'xp_reward': 50},
            {'name': 'chatterbox', 'description': '50 conversations terminées', 
             'category': 'conversation', 'icon': '🎪', 'requirement_value': 50, 'xp_reward': 100},
            
            # Streak badges
            {'name': 'three_day_streak', 'description': '3 jours consécutifs', 
             'category': 'streak', 'icon': '🔥', 'requirement_value': 3, 'xp_reward': 30},
            {'name': 'week_warrior', 'description': '7 jours consécutifs', 
             'category': 'streak', 'icon': '⚡', 'requirement_value': 7, 'xp_reward': 75},
            {'name': 'monthly_master', 'description': '30 jours consécutifs', 
             'category': 'streak', 'icon': '👑', 'requirement_value': 30, 'xp_reward': 200},
            
            # XP badges
            {'name': 'xp_collector', 'description': '100 XP gagnés', 
             'category': 'achievement', 'icon': '⭐', 'requirement_value': 100, 'xp_reward': 25},
            {'name': 'xp_hunter', 'description': '500 XP gagnés', 
             'category': 'achievement', 'icon': '🌟', 'requirement_value': 500, 'xp_reward': 50},
            {'name': 'xp_master', 'description': '1000 XP gagnés', 
             'category': 'achievement', 'icon': '💫', 'requirement_value': 1000, 'xp_reward': 100},
        ]
        
        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Badge créé: {badge.name}')
                )
            else:
                self.stdout.write(f'Badge existe déjà: {badge.name}')

# challenges/management/commands/create_challenges.py
from django.core.management.base import BaseCommand
from challenges.models import DailyChallenge

class Command(BaseCommand):
    help = 'Create initial daily challenges'
    
    def handle(self, *args, **options):
        challenges_data = [
            # Conversation challenges
            {
                'title': 'Conversation de 5 minutes',
                'description': 'Avoir une conversation de 5 minutes avec l\'IA',
                'challenge_type': 'conversation',
                'difficulty': 'easy',
                'target_language': 'en',
                'xp_reward': 30,
                'estimated_duration': 5
            },
            {
                'title': 'Discussion sur un sujet spécifique',
                'description': 'Discuter d\'un sujet de votre choix pendant 10 minutes',
                'challenge_type': 'conversation',
                'difficulty': 'medium',
                'target_language': 'en',
                'xp_reward': 50,
                'estimated_duration': 10
            },
            
            # Vocabulary challenges
            {
                'title': 'Apprendre 5 nouveaux mots',
                'description': 'Découvrir et utiliser 5 nouveaux mots en conversation',
                'challenge_type': 'vocabulary',
                'difficulty': 'easy',
                'target_language': 'en',
                'xp_reward': 25,
                'estimated_duration': 10
            },
            
            # Pronunciation challenges
            {
                'title': 'Améliorer la prononciation',
                'description': 'Pratiquer la prononciation de phrases complexes',
                'challenge_type': 'pronunciation',
                'difficulty': 'medium',
                'target_language': 'en',
                'xp_reward': 40,
                'estimated_duration': 15
            }
        ]
        
        for challenge_data in challenges_data:
            challenge, created = DailyChallenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults=challenge_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Défi créé: {challenge.title}')
                )

# ========================
# 11. CELERY TASKS
# ========================

# tasks.py
from celery import shared_task
from django.utils import timezone
from django.contrib.auth import get_user_model
from challenges.models import DailyChallenge, UserChallenge
from notifications.models import Notification
from services.gamification_service import GamificationService
import random

User = get_user_model()

@shared_task
def assign_daily_challenges():
    """Assign daily challenges to all active users"""
    users = User.objects.filter(is_active=True)
    today = timezone.now().date()
    
    for user in users:
        # Check if challenges already assigned
        existing = UserChallenge.objects.filter(
            user=user, assigned_at__date=today
        ).exists()
        
        if not existing:
            # Get appropriate challenges
            challenges = DailyChallenge.objects.filter(
                is_active=True,
                target_language=user.target_language
            )
            
            # Select 3 random challenges
            selected_challenges = random.sample(list(challenges), min(3, len(challenges)))
            
            for challenge in selected_challenges:
                UserChallenge.objects.create(
                    user=user,
                    challenge=challenge
                )
            
            # Send notification
            Notification.objects.create(
                user=user,
                notification_type='challenge',
                title='Nouveaux défis disponibles !',
                message=f'Vous avez {len(selected_challenges)} nouveaux défis à relever aujourd\'hui.'
            )

@shared_task
def send_learning_reminders():
    """Send learning reminders to users"""
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    users_to_remind = User.objects.filter(
        is_active=True,
        preferences__notifications_enabled=True,
        preferences__reminder_time__lte=now.time()
    )
    
    for user in users_to_remind:
        # Check if user studied today
        today = now.date()
        from progress.models import LearningProgress
        today_progress = LearningProgress.objects.filter(
            user=user, date=today
        ).first()
        
        if not today_progress or today_progress.study_time_minutes == 0:
            # Send reminder
            Notification.objects.create(
                user=user,
                notification_type='reminder',
                title='Il est temps d\'apprendre !',
                message='N\'oubliez pas votre session d\'apprentissage quotidienne.',
                scheduled_for=now
            )

@shared_task
def update_user_streaks():
    """Update user learning streaks daily"""
    users = User.objects.filter(is_active=True)
    
    for user in users:
        gamification = GamificationService(user)
        gamification.update_streak()

@shared_task
def cleanup_old_conversations():
    """Clean up old completed conversations (keep only text, remove audio)"""
    from conversations.models import Message
    from django.utils import timezone
    from datetime import timedelta
    
    # Remove audio files from messages older than 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    old_messages = Message.objects.filter(
        timestamp__lt=thirty_days_ago,
        audio_file__isnull=False
    )
    
    for message in old_messages:
        if message.audio_file:
            message.audio_file.delete()
            message.audio_file = None
            message.save()

# ========================
# 12. WEBSOCKET ROUTING
# ========================

# linguachat/routing.py
from django.urls import re_path
from conversations import consumers

websocket_urlpatterns = [
    re_path(r'ws/conversation/(?P<conversation_id>\d+)/, consumers.ConversationConsumer.as_asgi()),
]

# linguachat/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguachat.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})

# ========================
# 13. CELERY CONFIGURATION
# ========================

# linguachat/celery.py
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linguachat.settings')

app = Celery('linguachat')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'assign-daily-challenges': {
        'task': 'tasks.assign_daily_challenges',
        'schedule': 60.0 * 60.0 * 24.0,  # Daily at midnight
    },
    'send-learning-reminders': {
        'task': 'tasks.send_learning_reminders',
        'schedule': 60.0 * 60.0,  # Every hour
    },
    'update-user-streaks': {
        'task': 'tasks.update_user_streaks',
        'schedule': 60.0 * 60.0 * 24.0,  # Daily
    },
    'cleanup-old-conversations': {
        'task': 'tasks.cleanup_old_conversations',
        'schedule': 60.0 * 60.0 * 24.0 * 7.0,  # Weekly
    },
}

app.conf.timezone = 'UTC'

# ========================
# 14. NOTIFICATIONS SYSTEM
# ========================

# notifications/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id, user=request.user
        )
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user, is_read=False
    ).update(is_read=True)
    return Response({'status': 'success'})

# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:notification_id>/read/', views.mark_notification_read, name='mark-read'),
    path('mark-all-read/', views.mark_all_read, name='mark-all-read'),
]

# ========================
# 15. REQUIREMENTS.TXT
# ========================

# requirements.txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
channels==4.0.0
channels-redis==4.1.0
celery==5.3.4
redis==5.0.1
psycopg2-binary==2.9.9
python-decouple==3.8
Pillow==10.1.0
openai==1.3.7
google-cloud-translate==3.12.1
google-cloud-speech==2.21.0
gtts==2.4.0
SpeechRecognition==3.10.0
pydub==0.25.1
requests==2.31.0

# ========================
# 16. DOCKER CONFIGURATION
# ========================

# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - media_volume:/app/media
    environment:
      - DEBUG=1
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=linguachat
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A linguachat worker -l info
    volumes:
      - .:/app
    environment:
      - DEBUG=1
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  celery-beat:
    build: .
    command: celery -A linguachat beat -l info
    volumes:
      - .:/app
    environment:
      - DEBUG=1
      - DB_HOST=db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  media_volume:

# ========================
# 17. CONFIGURATION FILES
# ========================

# .env.example
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=linguachat
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# APIs
OPENAI_API_KEY=your-openai-key
GOOGLE_TRANSLATE_KEY=your-google-translate-key
GOOGLE_TTS_KEY=your-google-tts-key
ELEVEN_LABS_API_KEY=your-elevenlabs-key

# Redis
REDIS_URL=redis://localhost:6379

# Celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379

# .gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Media files
media/

# Static files
staticfiles/

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# ========================
# 18. INSTALLATION ET DÉPLOIEMENT
# ========================

# install.sh
#!/bin/bash

echo "Installation de LinguaChat AI..."

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier de configuration
cp .env.example .env
echo "Veuillez configurer vos clés API dans le fichier .env"

# Créer la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Créer les badges et défis initiaux
python manage.py create_badges
python manage.py create_challenges

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

echo "Installation terminée !"
echo "Lancez le serveur avec: python manage.py runserver"
echo "N'oubliez pas de démarrer Redis et Celery en parallèle :"
echo "- Redis: redis-server"
echo "- Celery Worker: celery -A linguachat worker -l info"
echo "- Celery Beat: celery -A linguachat beat -l info"

# deploy.sh
#!/bin/bash

echo "Déploiement de LinguaChat AI..."

# Mise à jour du code
git pull origin main

# Activation de l'environnement virtuel
source venv/bin/activate

# Installation des nouvelles dépendances
pip install -r requirements.txt

# Migrations de base de données
python manage.py makemigrations
python manage.py migrate

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Redémarrage des services
sudo systemctl restart linguachat
sudo systemctl restart linguachat-celery
sudo systemctl restart linguachat-celery-beat

echo "Déploiement terminé !"

# ========================
# 19. TESTS UNITAIRES
# ========================

# tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from conversations.models import Conversation, Message
from rewards.models import Badge, UserBadge, XPTransaction
from services.gamification_service import GamificationService

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.total_xp, 0)
        self.assertEqual(self.user.current_streak, 0)

class ConversationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.conversation = Conversation.objects.create(
            user=self.user,
            title='Test Conversation'
        )
    
    def test_conversation_creation(self):
        self.assertEqual(self.conversation.user, self.user)
        self.assertEqual(self.conversation.status, 'active')

class GamificationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.badge = Badge.objects.create(
            name='test_badge',
            description='Test Badge',
            category='achievement',
            icon='🏆',
            requirement_value=100,
            xp_reward=50
        )
    
    def test_award_xp(self):
        gamification = GamificationService(self.user)
        transaction = gamification.award_xp('conversation', 25, 'Test XP')
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.total_xp, 25)
        self.assertEqual(transaction.xp_amount, 25)

# tests/test_api.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class ConversationAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_conversation(self):
        url = reverse('conversation-list')
        data = {'title': 'Test Conversation'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Conversation')

# ========================
# 20. DOCUMENTATION API
# ========================

# API Documentation (README_API.md)
"""
# LinguaChat AI - Documentation API

## Authentification

Toutes les API nécessitent une authentification par token.
Header requis: `Authorization: Token your-token-here`

## Endpoints Principaux

### Authentification
- `POST /api/accounts/login/` - Connexion utilisateur
- `GET /api/accounts/profile/` - Profil utilisateur
- `PUT /api/accounts/profile/` - Mise à jour du profil

### Conversations
- `GET /api/conversations/` - Liste des conversations
- `POST /api/conversations/` - Créer une conversation
- `GET /api/conversations/{id}/` - Détail d'une conversation
- `POST /api/conversations/{id}/message/` - Envoyer un message
- `POST /api/conversations/{id}/complete/` - Terminer une conversation

### Récompenses
- `GET /api/rewards/badges/` - Badges de l'utilisateur
- `GET /api/rewards/badges/available/` - Badges disponibles
- `GET /api/rewards/stats/` - Statistiques utilisateur

### Défis
- `GET /api/challenges/daily/` - Défis du jour
- `POST /api/challenges/assign/` - Assigner des défis
- `POST /api/challenges/{id}/complete/` - Terminer un défi

### Progression
- `GET /api/progress/history/` - Historique de progression
- `GET /api/progress/dashboard/` - Statistiques du tableau de bord
- `GET /api/progress/vocabulary/` - Vocabulaire appris

### Contenu Culturel
- `GET /api/cultural/` - Contenu culturel disponible
- `POST /api/cultural/{id}/interact/` - Interagir avec le contenu

## WebSocket

Connexion WebSocket pour les conversations en temps réel :
`ws://localhost:8000/ws/conversation/{conversation_id}/`

### Messages WebSocket

Envoyer un message :
```json
{
    "type": "chat_message",
    "message": "Hello, how are you?"
}
```

Indicateur de frappe :
```json
{
    "type": "typing",
    "is_typing": true
}
```

## Codes d'erreur

- `400` - Données invalides
- `401` - Non authentifié
- `403` - Accès interdit
- `404` - Ressource non trouvée
- `500` - Erreur serveur
"""

# ========================
# FIN DU CODE DJANGO
# ========================