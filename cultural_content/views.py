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
