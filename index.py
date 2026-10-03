from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Nova API Key configurada
SAMBA_API_KEY = "ed055d9f-d61c-4bd3-9b79-4b677bc5c4a0"
SAMBA_URL = "https://api.sambanova.ai/v1/chat/completions"
LOCAL_API_KEY = "LEOMODZ"

@app.route("/ask", methods=["GET"])
def ask_sambanova():
    message = request.args.get("message")
    key = request.args.get("key")
    
    if key != LOCAL_API_KEY:
        return jsonify({"error": "Chave de API inválida!"}), 401

    if not message:
        return jsonify({"error": "Parâmetro 'message' em falta!"}), 400
        
    headers = {
        "Authorization": f"Bearer {SAMBA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "Meta-Llama-3.1-8B-Instruct",
        "messages": [
            {"role": "system", "content": "Você é um gerador de contas fictícias para o jogo Free Fire."},
            {"role": "user", "content": message}
        ],
        "temperature": 0.1,
        "top_p": 0.1
    }

    try:
        response = requests.post(SAMBA_URL, headers=headers, json=payload, timeout=30)
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = f"Erro da API SambaNova: {data['error']}"
        else:
            reply = f"Resposta inesperada: {data}"

        return jsonify({
            "status": "success",
            "message": message,
            "reply": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
