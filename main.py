from flask import Flask, render_template, request, jsonify
from gtts import gTTS
from googletrans import Translator
import os
import time

app = Flask(__name__)
translator = Translator()

# Supported languages for both translation and speech
SAFE_LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'French': 'fr',
    'German': 'de',
    'Spanish': 'es',
    'Japanese': 'ja',
    'Chinese': 'zh-cn',
    'Arabic': 'ar',
    'Russian': 'ru'
}

@app.route('/')
def index():
    return render_template('index.html', languages=list(SAFE_LANGUAGES.keys()))

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    input_text = data.get('text', '')
    target_lang = data.get('target_lang', 'English')

    if not input_text:
        return jsonify({'error': 'No input text provided.'})

    try:
        target_code = SAFE_LANGUAGES.get(target_lang, 'en')
        translated = translator.translate(input_text, dest=target_code)
        return jsonify({'translated_text': translated.text})
    except Exception as e:
        print(f"[Translation Error] {e}")
        return jsonify({'error': f"Translation failed: {str(e)}"})

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.get_json()
    text = data.get('text', '')
    lang = data.get('lang', 'en')

    if not text:
        return jsonify({'error': 'No text to speak.'})

    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"static/audio_{int(time.time())}.mp3"
        tts.save(filename)
        return jsonify({'audio_file': filename})
    except Exception as e:
        print(f"[TTS Error] {e}")
        return jsonify({'error': 'Text-to-speech failed.'})

if __name__ == '__main__':
    app.run(debug=True)
