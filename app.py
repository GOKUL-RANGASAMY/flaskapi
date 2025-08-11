from flask import Flask, request, jsonify
import os
import getpass
import json
from langchain.chat_models import init_chat_model

# Initialize Flask app
app = Flask(__name__)

# Set your Google API key (ask once at startup if not set)
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDq5fHiaxRfzgOaVO8SF4bCvqKykM1UAi4"

# Initialize Gemini model
model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

@app.route("/extract", methods=["POST"])
def extract_hiring_info():
    """
    Accepts a JSON body with 'input' key and returns structured hiring info JSON.
    Example:
    POST /extract
    {
        "input": "I want to hire Gokul as Developer-I-Engineer in the Software Team"
    }
    """
    try:
        # Get input text
        data = request.get_json()
        user_input = data.get("input", "").strip()

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Prompt for Gemini
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

        # Call model
        response = model.invoke(prompt)
        output_str = response.content.strip()

        # Attempt to parse JSON directly from model output
        try:
            # Sometimes model wraps JSON in code fences
            if output_str.startswith("```"):
                output_str = "\n".join(
                    line for line in output_str.splitlines() if not line.strip().startswith("```")
                )
            output_json = json.loads(output_str)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse JSON from model output", "raw_output": output_str}), 500

        return jsonify(output_json)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5050)
