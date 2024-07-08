from google.cloud import translate_v2 as translate
from src.config import get_service_account_info_google
client = translate.Client.from_service_account_info(get_service_account_info_google())
from src.Speech import Speech_methods

def get_output(audio, language):
    code_map = {
        "English": "en-US",
        "Punjabi": "pa-IN",
        "Hindi": "hi-IN",
        "Gujarati": "gu-IN",
        "Telugu": "te-IN",
        "Tamil": "ta-IN",
        "Marathi": "ma-IN",
    }

    transcript = Speech_methods.get_transcript(audio)
    print(transcript)
    translation_result = client.translate(
        transcript,
        target_language=code_map[language],
    )
    translation_result = translation_result["translatedText"]
    translated_audio_path = Speech_methods.get_translation(translation_result, lang_code=code_map[language], filename=audio)
    return translated_audio_path
