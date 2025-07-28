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
