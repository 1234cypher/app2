# conversations/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from services.ai_service import AIConversationService
from services.translation_service import TranslationService
from services.speech_service import SpeechService

User = get_user_model()

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.conversation_group_name = f'conversation_{self.conversation_id}'
        
        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'chat_message':
            message = text_data_json['message']
            is_voice = text_data_json.get('is_voice', False)
            
            # Process message and get AI response
            user_message, ai_message = await self.process_message(message, is_voice)
            
            # Send message to conversation group
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    'type': 'chat_message',
                    'user_message': user_message,
                    'ai_message': ai_message,
                }
            )
    
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'user_message': event['user_message'],
            'ai_message': event['ai_message'],
        }))
    
    @database_sync_to_async
    def process_message(self, message, is_voice=False):
        user = self.scope['user']
        conversation = Conversation.objects.get(id=self.conversation_id, user=user)
        
        # Save user message
        translation_service = TranslationService()
        translated_message = translation_service.translate_text(
            message, user.native_language, user.target_language
        )
        
        user_msg = Message.objects.create(
            conversation=conversation,
            message_type='user',
            original_text=message,
            translated_text=translated_message
        )
        
        # Generate AI response
        ai_service = AIConversationService()
        conversation_history = conversation.messages.all()
        
        ai_response = ai_service.generate_response(
            message, conversation_history, 
            user.current_level, user.target_language
        )
        
        # Translate AI response
        ai_translated = translation_service.translate_text(
            ai_response, user.native_language, user.target_language
        )
        
        # Generate audio for AI response
        speech_service = SpeechService()
        audio_file = speech_service.text_to_speech(ai_response, user.target_language)
        
        ai_msg = Message.objects.create(
            conversation=conversation,
            message_type='ai',
            original_text=ai_response,
            translated_text=ai_translated,
            audio_file=audio_file
        )
        
        return {
            'text': user_msg.original_text,
            'translation': user_msg.translated_text,
            'timestamp': user_msg.timestamp.isoformat()
        }, {
            'text': ai_msg.original_text,
            'translation': ai_msg.translated_text,
            'audio': ai_msg.audio_file.url if ai_msg.audio_file else None,
            'timestamp': ai_msg.timestamp.isoformat()
        }