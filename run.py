from scripts.chat import Chat
import json

if __name__ == '__main__':

    questions_path = "questions/player.txt"
    with open(questions_path, "r") as file:
        questions = file.readlines()

    chat = Chat(
        sql_data_path="/nba_players.sqlite",
        sql_coder_dir="/models/sqlcoder",
        llm_path="/models/Meta-Llama-3-8B-Instruct.gguf",
        llm_prompt_structure_path="prompt_structure/sql/1.txt",
        llm_prompt_structure_path="prompt_structure/llm/1.txt"
    )

    responses = {}
    for question in questions:
        responses[question] = chat.answer(question)

    answer_path = "answers/player.json"
    with open(answer_path, "w") as json_file:
        json.dump(responses, json_file, indent=4)
    