import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY", "SUA_CHAVE_AQUI")

@app.route('/')
def home():
    return "Jarvis Magrinho esta online!"

@app.route('/chat', methods=['POST'])
def chat():
    dados = request.json
    mensagem_usuario = dados.get("mensagem", "")

    if not mensagem_usuario:
        return jsonify({"erro": "Mensagem vazia"}), 400

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    payload = {
        "contents": [{
            "parts": [{"text": mensagem_usuario}]
        }]
    }
    
    try:
        resposta = requests.post(url, json=payload, timeout=10)
        dados_resposta = resposta.json()
        texto_jarvis = dados_resposta['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"resposta": texto_jarvis})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    porta = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=porta)