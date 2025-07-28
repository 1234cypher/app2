# cultural_content/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CulturalContentView.as_view(), name='cultural-content'),
    path('<int:content_id>/interact/', views.interact_with_content, name='interact-content'),
]
