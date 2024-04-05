from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/request', methods=['POST'])
def process_string():
    data = request.get_json()

    time.sleep(2)

    if 'message' in data:
        input_string = data['message']
        # Process the input string here, you can replace this with any processing logic you want
        response_message = f"Received string: {input_string}. Processing completed."
        return jsonify({'response': response_message})
    else:
        return jsonify({'error': 'Invalid request, no string provided.'}), 400


if __name__ == '__main__':
    app.run()

