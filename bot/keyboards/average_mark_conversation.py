import enum
import logging

from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters

from bot.keyboards.base_keyboard import get_menu_keyboard
from bot.main import menu

logger = logging.getLogger()


class States(enum.Enum):
    (FACULTY,
     YEAR,
     SPECIALITY,
     SUBJECT) = range(4)


def start(update: Update, context: CallbackContext):
    logger.info("Starting the conversation with user {user_id}".format(user_id=update.effective_user.id))
    update.message.reply_text(
        text="Faculty: ",
        reply_markup=ReplyKeyboardRemove()
    )
    return States.FACULTY


def faculty_handler(update: Update, context: CallbackContext):
    context.user_data[States.FACULTY] = update.message.text
    logger.info("faculty_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                       data=context.user_data))
    update.message.reply_text(
        text="Year: "
    )
    return States.YEAR


def year_handler(update: Update, context: CallbackContext):
    context.user_data[States.YEAR] = update.message.text
    logger.info("year_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                    data=context.user_data))
    update.message.reply_text(
        text="Speciality: "
    )
    return States.SPECIALITY


def speciality_handler(update: Update, context: CallbackContext):
    context.user_data[States.SPECIALITY] = update.message.text
    logger.info(
        "speciality_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                  data=context.user_data))
    update.message.reply_text(
        text="Subject: "
    )
    return States.SUBJECT


def subject_handler(update: Update, context: CallbackContext):
    context.user_data[States.SUBJECT] = update.message.text
    logger.info("subject_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                       data=context.user_data))
    update.message.reply_text(
        text="\n".join(['%s: %s' % (k, v) for k, v in context.user_data.items()]),
        reply_markup=get_menu_keyboard()
    )
    return ConversationHandler.END


def get_handler() -> ConversationHandler:
    conv_handl = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.all, menu)
        ],
        states={
            States.FACULTY: [
                MessageHandler(Filters.all, faculty_handler, pass_user_data=True)
            ],
            States.YEAR: [
                MessageHandler(Filters.all, year_handler, pass_user_data=True)
            ],
            States.SPECIALITY: [
                MessageHandler(Filters.all, speciality_handler, pass_user_data=True)
            ],
            States.SUBJECT: [
                MessageHandler(Filters.all, subject_handler, pass_user_data=True)
            ]
        },
        fallbacks=[]
    )
    return conv_handl


if __name__ == '__main__':
    print(States.CALC)
