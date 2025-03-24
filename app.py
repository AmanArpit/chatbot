from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
DID_API_KEY = os.getenv("DID_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = Flask(__name__)

# ✅ Home route to avoid 404 error
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Human-like Chatbot!"})

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")

    # Mock chatbot response
    chatbot_response = f"You said: {user_input}"

    # ➡️ Text-to-Speech (ElevenLabs)
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech"
    tts_headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    tts_payload = {
        "text": chatbot_response,
        "voice": "Rachel"  # Choose your preferred voice
    }
    tts_response = requests.post(tts_url, json=tts_payload, headers=tts_headers)

    if tts_response.status_code != 200:
        return jsonify({"error": "TTS API failed"}), 500

    audio_url = tts_response.json().get("url")

    # ➡️ Talking Face (D-ID)
    did_url = "https://api.d-id.com/talks"
    did_headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    did_payload = {
        "script": {
            "type": "text",
            "input": chatbot_response
        },
        "voice": {
            "url": audio_url
        }
    }

    did_response = requests.post(did_url, json=did_payload, headers=did_headers)

    if did_response.status_code != 200:
        return jsonify({"error": "D-ID API failed"}), 500

    face_url = did_response.json().get("result_url")

    return jsonify({
        "face_url": face_url,
        "audio_url": audio_url
    })


if __name__ == '__main__':
    app.run(debug=True)
