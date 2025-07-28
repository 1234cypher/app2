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
