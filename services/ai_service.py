# services/ai_service.py
import openai
from django.conf import settings
import json

class AIConversationService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            openai.api_key = None
    
    def generate_response(self, user_message, conversation_history, user_level, target_language):
        """Generate AI response for conversation"""
        if not openai.api_key:
            return "Désolé, le service IA n'est pas configuré pour le moment."
            
        system_prompt = self._build_system_prompt(user_level, target_language)
        messages = self._build_message_history(conversation_history, system_prompt)
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Désolé, je ne peux pas répondre pour le moment. Erreur: {str(e)}"
    
    def _build_system_prompt(self, user_level, target_language):
        return f"""Tu es un assistant IA pour l'apprentissage du {target_language}. 
        L'utilisateur a un niveau {user_level}. Adapte tes réponses à son niveau:
        - Utilise un vocabulaire approprié
        - Corrige gentiment les erreurs
        - Encourage l'apprentissage
        - Reste conversationnel et engageant"""
    
    def _build_message_history(self, conversation_history, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        for msg in conversation_history[-10:]:  # Garde les 10 derniers messages
            role = "user" if msg.message_type == "user" else "assistant"
            messages.append({"role": role, "content": msg.original_text})
        return messages