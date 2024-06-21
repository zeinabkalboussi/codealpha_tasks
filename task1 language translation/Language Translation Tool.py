from googletrans import Translator
import speech_recognition as sr

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Now...")
        audio = recognizer.listen(source)
        try:
            print("Voice recognition in progress..")
            text = recognizer.recognize_google(audio, language='fr-FR')  
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand the audio.")
        except sr.RequestError:
            print("Sorry, voice recognition service is not available.")
    return ""

if __name__ == "__main__":
    languages = {'fr': 'French', 'en': 'English', 'es': 'Spanish', 'de': 'German', 'it': 'Italian', 'ar': 'Arabic'}

    print("Languages ​​available:")
    for lang_code, lang_name in languages.items():
        print(f"{lang_code}: {lang_name}")

    source_language = input("Enter the source language code : ").strip()
    destination_language = input("Enter the destination language code: ").strip()

    use_voice_input = input("Do you want to enter text by voice? (Yes / No): ").strip().lower()
    if use_voice_input == 'yes':
        text_to_translate = get_audio_input()
    else:
        text_to_translate = input("Enter the text to translate: ").strip()

    if text_to_translate:
        translated_text = translate_text(text_to_translate, source_language, destination_language)
        print(f"Translated text: {translated_text}")
    else:
        print("No text to translate. ")

