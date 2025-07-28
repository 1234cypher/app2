# services/translation_service.py
from google.cloud import translate_v2 as translate
from django.conf import settings

class TranslationService:
    def __init__(self):
        if settings.GOOGLE_TRANSLATE_KEY:
            self.client = translate.Client(api_key=settings.GOOGLE_TRANSLATE_KEY)
        else:
            self.client = None
    
    def translate_text(self, text, target_language, source_language=None):
        """Translate text using Google Translate API"""
        if not self.client:
            return text  # Return original text if no API key
            
        try:
            result = self.client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            return result['translatedText']
        except Exception as e:
            return f"Erreur de traduction: {str(e)}"
    
    def detect_language(self, text):
        """Detect the language of given text"""
        if not self.client:
            return None
            
        try:
            result = self.client.detect_language(text)
            return result['language']
        except Exception as e:
            return None