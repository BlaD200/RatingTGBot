import json
import logging

import telegram
from flask import Flask, request
from telegram import Update
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, Dispatcher, CallbackContext

from bot.constants import BOT_TOKEN
from bot.keyboards import average_mark_conversation
from bot.keyboards.base_keyboard import get_menu_keyboard
from bot.localization.localization import get_localize
from bot.user import User

logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)

app = Flask(__name__)

# Registering the dispatcher
dispatcher: Dispatcher = None

# Registering logger here
logger: logging.Logger = logging.getLogger(__name__)


def setup():
    global dispatcher
    updater = Updater(BOT_TOKEN, use_context=True)
    if dispatcher is None:
        dispatcher = updater.dispatcher

    # Registering commands handlers here #

    # Registering conversation handlers here
    calculate_rating_handler = average_mark_conversation.get_handler()

    dispatcher.add_handler(calculate_rating_handler)

    # Registering handlers here #
    menu_handler = MessageHandler(Filters.all, menu)

    dispatcher.add_handler(menu_handler)

    return updater


def menu(update: Update, context: CallbackContext):
    logger.info("menu function call")
    strings = get_localize(User().get_lang())
    if update.message.text == strings.calculate_rating:
        return average_mark_conversation.start(update, context)
    elif update.message.text == strings.get_states:
        update.message.reply_text(
            text=strings.not_impl,
            reply_markup=get_menu_keyboard()
        )
    elif update.message.text == strings.settings:
        update.message.reply_text(
            text=strings.not_impl,
            reply_markup=get_menu_keyboard()
        )
    elif update.message.text == strings.edit:
        update.message.reply_text(
            text=strings.not_impl,
            reply_markup=get_menu_keyboard()
        )
    else:
        update.message.reply_text(
            text=strings.use_keyb,
            reply_markup=get_menu_keyboard()
        )


@app.route("/", methods=["GET", "HEAD"])
def index():
    return '<h1>Telegram Bot by <a href="tg://user?id=386151408">Vlad Synytsyn</a></h1>'


@app.route('/', methods=['Post'])
def webhook():
    json_request = request.get_json()
    update = telegram.Update.de_json(json_request, dispatcher.bot)
    dispatcher.process_update(update)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    # urlopen(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')
    # Check, if bot correctly connect to Telegram API
    bot = telegram.Bot(BOT_TOKEN)
    info = bot.get_me()
    print(f'Bot info: {info}')
    # print(bot.get_webhook_info())
    # setup()

    # Do not use it in a production deployment. Use webhook instead. #
    updater: Updater = setup()
    updater.start_polling()
    updater.idle()

    # app.debug = True
    # app.run()
