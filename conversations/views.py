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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_conversation(request):
    serializer = ConversationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)