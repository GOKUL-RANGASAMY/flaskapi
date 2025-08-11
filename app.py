from flask import Flask, request, jsonify
import os
import json
from langchain.chat_models import init_chat_model
from pyngrok import ngrok, conf

app = Flask(__name__)

# Set ngrok auth token
conf.get_default().auth_token = "2Rozyomo6nwINc5yaRzByoSL4GY_4wTUVY3cbXx1GN1qTGi8a"

# Set Google API key
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDq5fHiaxRfzgOaVO8SF4bCvqKykM1UAi4"

# Initialize Gemini model
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

@app.route("/extract", methods=["POST"])
def extract_hiring_info():
    try:
        data = request.get_json()
        user_input = data.get("input", "").strip()

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        prompt = f"""
        Extract the following information from the input and provide it as JSON with the keys:
        - supervisoryOrganization
        - position
        - hirePerson

        Input: "{user_input}"

        Output JSON example:
        {{
          "supervisoryOrganization": "Software Team",
          "position": "Developer-I-Engineer",
          "hirePerson": "Gokul"
        }}
        """


        
        response = model.invoke(prompt)
        output_str = response.content.strip()

        if output_str.startswith("```"):
            output_str = "\n".join(
                line for line in output_str.splitlines() if not line.strip().startswith("```")
            )

        output_json = json.loads(output_str)
        return jsonify(output_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    public_url = ngrok.connect(5050)
    print(" * ngrok tunnel URL:", public_url)
    app.run(debug=True, host="0.0.0.0", port=5050)
