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
