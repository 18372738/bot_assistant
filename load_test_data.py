import json
from environs import Env

from dialogflow import create_intent


if __name__ == "__main__":

    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')

    with open("training_phrases.json", "r") as my_file:
        training_phrases_json = my_file.read()
    training_phrases = json.loads(training_phrases_json)
    for display_name, phrases in training_phrases.items():
        training_phrases_parts = phrases['questions']
        message_texts = [phrases['answer'], ]
        create_intent(
            project_id,
            display_name,
            training_phrases_parts,
            message_texts
        )
