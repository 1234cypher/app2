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
