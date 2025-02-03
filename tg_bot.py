import logging
from functools import partial

from environs import Env
from time import sleep
from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts
from error_logging import TelegramLogsHandler


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_text(
        'Я бот-помощник.Задавайте любые вопросы'
    )


def show_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def handle_tg_message(project_id: str, update: Update, context: CallbackContext) -> None:
    try:
        text = update.message.text
        session_id = f"tg{update.message.chat_id}"
        fulfillment_text, is_fallback = detect_intent_texts(project_id, session_id, text)
        update.message.reply_text(fulfillment_text)
    except requests.ReadTimeout:
        return
    except requests.ConnectionError:
        logger.warning("Нет интернет соединения.")
        time.sleep(10)
    except Exception as error:
        logger.error(f'Бот упал с ошибкой:\n{error}')
        raise


def main() -> None:
    env = Env()
    env.read_env()

    logging.basicConfig(format="%(process)d %(levelname)s %(message)s")
    logger = logging.getLogger('telegram_logger')
    logger.setLevel(logging.INFO)

    telegram_token = env.str('TELEGRAM_TOKEN')
    telegram_logger = env.str('TELEGRAM_LOGGER')
    chat_id = env.str('CHAT_ID')
    project_id = env.str('PROJECT_ID')
    bot = Bot(token=telegram_logger)

    updater = Updater(telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["env"] = env
    dispatcher.bot_data["logger"] = logger
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", show_help))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, partial(handle_tg_message, project_id)))

    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info("Телеграм бот запущен.")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
