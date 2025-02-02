import random
import logging

import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Update, ForceReply, Bot
from environs import Env

from dialogflow import detect_intent_texts
from error_logging import TelegramLogsHandler


def handle_vk_message(event, vk_client, project_id):
    text = event.text
    session_id = f"vk{user_id=event.user_id}",
    fulfillment_text, is_fallback = detect_intent_texts(project_id, session_id, text)
    if is_fallback:
        return

    vk_client.messages.send(
        user_id=event.user_id,
        message=fulfillment_text,
        random_id=random.randint(1,1000000)
    )


def main():
    env = Env()
    env.read_env()

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger('telegram_logger')
    logger.setLevel(logging.INFO)

    telegram_logger = env.str('TELEGRAM_LOGGER')
    chat_id = env.str('CHAT_ID')
    project_id = env.str('PROJECT_ID')
    vk_token = env.str("VK_TOKEN")

    bot = Bot(token=telegram_logger)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info("Бот Вконтакте запущен.")

    vk_session = vk_api.VkApi(token=vk_token)
    vk_client = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_vk_message(event, vk_client, project_id)
    except requests.ReadTimeout:
        raise
    except requests.ConnectionError:
        logger.warning("Нет интернет соединения.")
        time.sleep(10)
    except Exception as error:
        logger.error(f'Бот упал с ошибкой:\n{error}')
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
