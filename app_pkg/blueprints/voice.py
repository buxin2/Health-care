import threading
from flask import Blueprint, jsonify, request
from ..services.voice import process_voice, get_ai_response, speak_text


voice_bp = Blueprint('voice', __name__)


@voice_bp.route('/voice')
def voice():
    text = process_voice()
    return jsonify({"recognized_text": text})


@voice_bp.route('/ai_response', methods=['POST'])
def ai_response():
    data = request.get_json()
    user_text = data.get('text', '')
    response_text = get_ai_response(user_text)
    threading.Thread(target=speak_text, args=(response_text,)).start()
    return jsonify({"response": response_text})



