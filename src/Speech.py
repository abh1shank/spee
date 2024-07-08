import os
import tempfile
import time
import google.oauth2 as go
from google.cloud import texttospeech, storage
from src.config import get_assembly, get_service_account_info_google
credentials = go.service_account.Credentials.from_service_account_info(get_service_account_info_google())
import assemblyai as aai
aai.settings.api_key = get_assembly()
class Speech_methods:
    @staticmethod
    def get_transcript(audio_file):
        credentials = go.service_account.Credentials.from_service_account_info(get_service_account_info_google())
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket('speech2speechbucket')
        blob = bucket.blob(audio_file)
        exp = int(time.time() + 3600)
        audio_url = blob.generate_signed_url(expiration=exp)
        #print(audio_url)
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_url)
        return transcript.text

    @staticmethod
    def get_translation(transcript, lang_code, filename):
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        synthesis_input = texttospeech.SynthesisInput(text=transcript)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        storage_client = storage.Client()
        bucket = storage_client.bucket('speech2speechbucket')
        processed_blob = bucket.blob('processed_' + filename)
        processed_blob.upload_from_string(response.audio_content, content_type='audio/mp3')

        return processed_blob.public_url
