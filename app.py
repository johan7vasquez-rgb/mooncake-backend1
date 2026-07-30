import os
from flask import Flask, jsonify, request
import google.generativeai as genai

app = Flask(__name__)

# Render guardará la API Key de forma segura en las variables de entorno
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Eres Mooncake, un asistente virtual carismático, divertido y súper inteligente. "
        "Tu usuario y creador es Johan. Responde siempre de forma amigable, clara y fluida."
    ),
)


@app.route("/", methods=["GET"])
def home():
    return "¡Servidor en Render funcionando con Gemini! 🚀", 200


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Envía un mensaje válido."}), 400

        # En Render la llamada estándar de la librería funciona 100% perfecto
        response = model.generate_content(user_message)
        return jsonify({"response": response.text.strip()}), 200

    except Exception as e:
        return jsonify({"response": f"Error en la IA: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))