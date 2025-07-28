# conversations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationListCreateView.as_view(), name='conversation-list'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('<int:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('<int:conversation_id>/message/', views.send_message, name='send-message'),
    path('<int:conversation_id>/complete/', views.complete_conversation, name='complete-conversation'),
]
