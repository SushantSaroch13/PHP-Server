from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

FIREBASE_URL = "https://http-test-fd0cd-default-rtdb.firebaseio.com/energymeter/meter1.json"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask Firebase API. Send POST request to /postdata to push data."})

@app.route("/postdata", methods=["POST"])
def post_data():
    try:
        # Get JSON data from POST request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Send data to Firebase
        response = requests.put(FIREBASE_URL, json=data)

        if response.status_code in [200, 204]:
            return jsonify({"message": "Data sent to Firebase successfully."}), 200
        else:
            return jsonify({"error": "Failed to send to Firebase", "firebase_response": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
