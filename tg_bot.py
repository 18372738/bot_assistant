import logging

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from dialogflow import detect_intent_texts


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        'Здравствуйте\!',
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def response(update: Update, context: CallbackContext) -> None:
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    text = update.message.text
    session_id = update.message.chat_id
    fulfillment_text, is_fallback = detect_intent_texts(project_id, session_id, text)
    update.message.reply_text(fulfillment_text)


def main() -> None:
    """Start the bot."""
    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, response))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
