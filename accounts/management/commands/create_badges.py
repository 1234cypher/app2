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
