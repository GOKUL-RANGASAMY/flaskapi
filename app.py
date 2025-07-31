from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage (for demonstration)
data_storage = []

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_storage), 200

@app.route('/data', methods=['POST'])
def post_data():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    data_storage.append(data)
    return jsonify({"message": "Data added", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5050)
 
