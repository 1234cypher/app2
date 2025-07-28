# rewards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('badges/', views.UserBadgesView.as_view(), name='user-badges'),
    path('badges/available/', views.AvailableBadgesView.as_view(), name='available-badges'),
    path('xp/history/', views.XPHistoryView.as_view(), name='xp-history'),
    path('stats/', views.user_stats, name='user-stats'),
]