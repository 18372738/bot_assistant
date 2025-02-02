import logging

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


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def handle_tg_message(update: Update, context: CallbackContext) -> None:
    env = context.bot_data["env"]
    project_id = env.str("PROJECT_ID")
    logger = context.bot_data["logger"]
    try:
        text = update.message.text
        session_id = update.message.chat_id
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
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_tg_message))

    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info("Телеграм бот запущен.")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
