import json
import logging
from urllib.request import urlopen

import telegram
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext

from flask import Flask, request

from bot.constants import BOT_TOKEN, WEBHOOK_URL

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

app = Flask(__name__)
bot = telegram.Bot(BOT_TOKEN)


def setup():
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

    # Registering handlers here #
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)

    # Registering commands handlers here #
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    return dispatcher


def start():
    pass


def echo(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=update.message.text
    )


@app.route("/", methods=["GET", "HEAD"])
def index():
    return '<h1>Telegram Bot by <a href="tg://user?id=386151408">Vlad Synytsyn</a></h1>'


@app.route('/', methods=['Post'])
def webhook():
    json_request = request.get_json()
    dispatcher = setup()
    update = telegram.Update.de_json(json_request, dispatcher.bot)
    dispatcher.process_update(update)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    urlopen(f'https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}')
    # Check, if bot correctly connect to Telegram API
    info = bot.get_me()
    print(f'Bot info: {info}')
    print(bot.get_webhook_info())
    app.run()
