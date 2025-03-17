import os
import io
from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
from serverless_wsgi import handle_request

# Set the template folder path relative to the project root.
# os.getcwd() should be the project root on Vercel.
template_dir = os.path.join(os.getcwd(), 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def index():
    return render_template('index.html')

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
        return jsonify({'error': str(e)}), 500

# Vercel uses this handler to invoke your Flask app.
def handler(event, context):
    return handle_request(app, event, context)
