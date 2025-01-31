import random
import logging

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from telegram import Update, ForceReply, Bot
from environs import Env

from dialogflow import detect_intent_texts


class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def echo(event, vk_api):
    env = Env()
    env.read_env()

    project_id = env.str('PROJECT_ID')
    text = event.text
    session_id = user_id=event.user_id,
    fulfillment_text, is_fallback = detect_intent_texts(project_id, session_id, text)
    if is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=fulfillment_text,
        random_id=random.randint(1,1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger('telegram_logger')
    logger.setLevel(logging.INFO)

    telegram_logger = env.str('TELEGRAM_LOGGER')
    chat_id = env.str('CHAT_ID')
    bot = Bot(token=telegram_logger)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info("Бот Вконтакте запущен.")

    vk_token = env.str("VK_TOKEN")
    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
    except requests.ReadTimeout:
        raise
    except requests.ConnectionError:
        logger.warning("Нет интернет соединения.")
        time.sleep(10)
    except Exception as error:
        logger.error(f'Бот упал с ошибкой:\n{error}')
        raise
