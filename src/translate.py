import logging
from google.cloud import translate_v2 as translate
from src.config import get_credentials
from src.Speech import Speech_methods

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

credentials = get_credentials()
client = translate.Client(credentials=credentials)


def get_output(audio, language):
    code_map = {
        "English": "en-US",
        "Punjabi": "pa-IN",
        "Hindi": "hi-IN",
        "Gujarati": "gu-IN",
        "Telugu": "te-IN",
        "Tamil": "ta-IN",
        "Marathi": "mr-IN",
    }

    try:
        transcript = Speech_methods.get_transcript(audio)
        logger.info(f"Obtained transcript: {transcript[:50]}...")

        translation_result = client.translate(
            transcript,
            target_language=code_map[language],
        )
        translation_result = translation_result["translatedText"]
        logger.info(f"Translation result: {translation_result[:50]}...")
        translated_audio_path = Speech_methods.get_translation(translation_result, lang_code=code_map[language],
                                                               filename=audio)
        logger.info(f"Translated audio path: {translated_audio_path}")

        return translated_audio_path
    except Exception as e:
        logger.error(f"Error in get_output: {str(e)}")
        raise