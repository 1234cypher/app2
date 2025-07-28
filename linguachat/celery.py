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