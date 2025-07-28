# services/speech_service.py
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from django.core.files.base import ContentFile

class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def speech_to_text(self, audio_file, language='fr-FR'):
        """Convert speech to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Audio non reconnu"
        except sr.RequestError as e:
            return f"Erreur du service: {str(e)}"
    
    def text_to_speech(self, text, language='fr'):
        """Convert text to speech"""
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            with open(temp_file.name, 'rb') as f:
                audio_content = f.read()
            
            os.unlink(temp_file.name)
            return ContentFile(audio_content, name=f'tts_{hash(text)}.mp3')
        except Exception as e:
            return None
