import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from dialogflow import detect_intent_texts


def echo(event, vk_api):
    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')
    text = event.text
    session_id = user_id=event.user_id,
    response_text = detect_intent_texts(project_id, session_id, text)
    vk_api.messages.send(
        user_id=event.user_id,
        message=response_text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_token = env.str("VK_TOKEN")
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)
