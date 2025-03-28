from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ API Keys
DID_API_KEY = os.getenv("DID_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

app = Flask(__name__)

# ✅ Home route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Human-like Chatbot!"})

# ✅ Chat route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # ➡️ Text-to-Speech (ElevenLabs)
    tts_url = "https://api.elevenlabs.io/v1/text-to-speech/{YOUR_VOICE_ID}/stream"
    tts_headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    tts_payload = {
        "text": user_input,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }

    tts_response = requests.post(tts_url, json=tts_payload, headers=tts_headers)

    if tts_response.status_code != 200:
        return jsonify({"error": "Failed to generate audio"}), 500

    audio_url = tts_response.json().get("audio_url")

    # ➡️ Talking Face (D-ID)
    did_url = "https://api.d-id.com/talks"
    did_headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    did_payload = {
        "script": {
            "type": "text",
            "input": user_input
        },
        "source_url": "https://d-id.com/example_face.jpg",   # Example face image
        "voice_url": audio_url
    }

    did_response = requests.post(did_url, json=did_payload, headers=did_headers)

    if did_response.status_code != 200:
        return jsonify({"error": "Failed to generate face"}), 500

    face_url = did_response.json().get("result_url")

    return jsonify({
        "face_url": face_url,
        "audio_url": audio_url
    })

# ✅ Run the app with 0.0.0.0 and a fixed port
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
