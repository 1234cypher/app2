# linguachat/routing.py
from django.urls import re_path
from conversations import consumers

websocket_urlpatterns = [
    re_path(r'ws/conversation/(?P<conversation_id>\d+)/$', consumers.ConversationConsumer.as_asgi()),
]