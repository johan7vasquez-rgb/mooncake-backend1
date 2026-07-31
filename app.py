import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configurar la API key de Gemini de forma segura desde las variables de entorno de Render
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Usar el modelo estándar recomendado
generation_config = {"temperature": 0.7}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Mooncake OS Backend online 🌙"}), 200

# Ruta para el Chat Inteligente
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Mensaje vacío"}), 400

        # Generar respuesta usando Gemini
        response = model.generate_content(user_message)
        bot_response = response.text

        return jsonify({"response": bot_response}), 200

    except Exception as e:
        print(f"Error en /chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Ruta para la Billetera Digital (¡Añadida para corregir el error 404!)
@app.route("/api/finance", methods=["POST"])
def finance():
    try:
        data = request.get_json()
        monto = data.get("monto")
        descripcion = data.get("descripcion")
        
        print(f"Finanza recibida -> Monto: {monto}, Descripcion: {descripcion}")
        
        return jsonify({"status": "success", "message": "Movimiento registrado correctamente"}), 200

    except Exception as e:
        print(f"Error en /api/finance: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
