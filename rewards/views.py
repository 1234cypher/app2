# rewards/views.py
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Sum
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
        total_xp=Sum('xp_earned'),
        total_time=Sum('study_time_minutes'),
        total_conversations=Sum('conversations_count')
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