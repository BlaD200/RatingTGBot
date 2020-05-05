import json
import logging
from urllib.request import urlopen

import telegram
from flask import Flask, request
from telegram import Update
from telegram.ext import Updater, CallbackContext
from telegram.ext import MessageHandler, Filters, CommandHandler, ConversationHandler

from bot.constants import BOT_TOKEN, WEBHOOK_URL
from bot.keyboards.base_keyboard import get_base_reply_keyboard
from bot.localization.localization import get_localize
from bot.keyboards import average_mark_conversation

logging.basicConfig(format='%(levelname)s %(name)s | %(asctime)s | %(message)s',
                    level=logging.INFO)

app = Flask(__name__)

# Registering the dispatcher
dispatcher = None


def setup():
    global dispatcher
    if dispatcher is None:
        updater = Updater(BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher

    # Registering commands handlers here #

    # Conversation handlers here
    calculate_rating_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.all, menu)
        ],
        states={
            average_mark_conversation.States.FACULTY: [
                MessageHandler(Filters.all, average_mark_conversation.faculty_handler, pass_user_data=True)
            ],
            average_mark_conversation.States.YEAR: [
                MessageHandler(Filters.all, average_mark_conversation.year_handler, pass_user_data=True)
            ],
            average_mark_conversation.States.SPECIALITY: [
                MessageHandler(Filters.all, average_mark_conversation.speciality_handler, pass_user_data=True)
            ],
            average_mark_conversation.States.SUBJECT: [
                MessageHandler(Filters.all, average_mark_conversation.subject_handler, pass_user_data=True)
            ]
        },
        fallbacks=[]
    )
    dispatcher.add_handler(calculate_rating_handler)

    # Registering handlers here #
    menu_handler = MessageHandler(Filters.all, menu)
    dispatcher.add_handler(menu_handler)


def menu(update: Update, context: CallbackContext):
    strings = get_localize("ukr")
    if update.message.text == strings.calculate_rating:
        return average_mark_conversation.start(update, context)
    elif update.message.text == strings.get_states:
        update.message.reply_text(
            text=strings.notimpl,
            reply_markup=get_base_reply_keyboard()
        )
    elif update.message.text == strings.settings:
        update.message.reply_text(
            text=strings.notimpl,
            reply_markup=get_base_reply_keyboard()
        )
    elif update.message.text == strings.edit:
        update.message.reply_text(
            text=strings.notimpl,
            reply_markup=get_base_reply_keyboard()
        )
    else:
        update.message.reply_text(
            text=strings.use_keyb,
            reply_markup=get_base_reply_keyboard()
        )
    return ConversationHandler.END


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
    urlopen(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')
    # Check, if bot correctly connect to Telegram API
    bot = telegram.Bot(BOT_TOKEN)
    info = bot.get_me()
    print(f'Bot info: {info}')
    print(bot.get_webhook_info())
    setup()
    app.debug = True
    app.run()
