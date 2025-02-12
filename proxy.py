import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Charger la clé API depuis les variables d'environnement
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Vérification de la clé API
if not ANTHROPIC_API_KEY:
    raise ValueError("❌ ERREUR : La clé API d'Anthropic est absente.")

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes externes

# URL de l'API d'Anthropic
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

@app.route("/claude", methods=["POST"])
def get_claude_response():
    """Fait une requête à l'API Claude et retourne la réponse."""
    data = request.json
    headers = {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
        "Anthropic-Version": "2023-06-01"
    }

    # Correction du format JSON attendu par Anthropic
    payload = {
        "model": data.get("model", "claude-2"),
        "max_tokens": data.get("max_tokens", 200),
        "messages": [
            {"role": "user", "content": data.get("prompt", "Bonjour")}
        ]
    }

    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
