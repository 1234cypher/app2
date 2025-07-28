# progress/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.ProgressHistoryView.as_view(), name='progress-history'),
    path('vocabulary/', views.VocabularyView.as_view(), name='vocabulary'),
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
]