# challenges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.DailyChallengesView.as_view(), name='daily-challenges'),
    path('assign/', views.assign_daily_challenges, name='assign-challenges'),
    path('<int:challenge_id>/complete/', views.complete_challenge, name='complete-challenge'),
]
