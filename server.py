from flask import Flask, request, jsonify
from flask_cors import CORS
from scripts.chat import Chat

app = Flask(__name__)
CORS(app)

chat = Chat(
    sql_data_path="/nba_players.sqlite",
    sql_coder_dir="/models/sqlcoder",
    llm_path="/models/Meta-Llama-3-8B-Instruct.gguf",
    llm_prompt_structure_path="prompt_structure/sql/1.txt",
    llm_prompt_structure_path="prompt_structure/llm/1.txt"
)


@app.route('/request', methods=['POST'])
def process_request():
    data = request.get_json()

    if 'message' in data:
        question = data['message']
        print(f"Received string: {question}. Processing ...")
        
        answer = chat.answer(question, print_prompts=True)
        return jsonify({'response': answer})
    else:
        return jsonify({'error': 'Invalid request, no string provided.'}), 400


if __name__ == '__main__':
    app.run()
