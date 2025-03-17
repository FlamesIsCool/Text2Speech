import os
import io
import logging
from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
from serverless_wsgi import handle_request

# Set up logging for debugging (these messages will show in Vercel logs)
logging.basicConfig(level=logging.DEBUG)

# Calculate the absolute path to the templates folder.
# Since this file is in the "api" folder, we go one directory up.
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
logging.debug("Template directory set to: %s", template_dir)

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error("Error rendering template: %s", e)
        return "Error rendering template", 500

@app.route('/convert', methods=['POST'])
def convert_audio():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype="audio/mpeg")
    except Exception as e:
        logging.error("Error in convert_audio: %s", e)
        return jsonify({'error': str(e)}), 500

@app.route('/save-audio', methods=['POST'])
def save_audio():
    data = request.get_json()
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    try:
        tts = gTTS(text=text, lang='en')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        return send_file(mp3_fp, mimetype="audio/mpeg", as_attachment=True, download_name="output.mp3")
    except Exception as e:
        logging.error("Error in save_audio: %s", e)
        return jsonify({'error': str(e)}), 500

# Vercel requires a handler function to pass events to the Flask app.
def handler(event, context):
    return handle_request(app, event, context)
