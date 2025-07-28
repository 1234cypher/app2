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
