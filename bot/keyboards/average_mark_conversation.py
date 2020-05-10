import enum
import logging

from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters

from bot.keyboards.base_keyboard import get_menu_keyboard
from bot.localization.localization import get_localize
from bot.main import menu
from bot.user import User

logger = logging.getLogger(__name__)


class States(enum.Enum):
    (FACULTY,
     YEAR,
     SPECIALITY,
     SUBJECT) = range(4)

    def __repr__(self):
        return self.name


def start(update: Update, context: CallbackContext):
    context.user_data["last_state"] = States.FACULTY
    logger.info("Starting the conversation with user {user_id}".format(user_id=update.effective_user.id))
    next_message(update, context)
    return States.FACULTY


def faculty_handler(update: Update, context: CallbackContext):
    context.user_data[States.FACULTY] = update.message.text
    context.user_data["last_state"] = States.YEAR
    logger.info("faculty_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                       data=context.user_data))
    next_message(update, context)
    return States.YEAR


def year_handler(update: Update, context: CallbackContext):
    context.user_data[States.YEAR] = update.message.text
    context.user_data["last_state"] = States.SPECIALITY
    logger.info("year_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                    data=context.user_data))
    next_message(update, context)
    return States.SPECIALITY


def speciality_handler(update: Update, context: CallbackContext):
    context.user_data[States.SPECIALITY] = update.message.text
    context.user_data["last_state"] = States.SUBJECT
    logger.info(
        "speciality_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                  data=context.user_data))
    next_message(update, context)
    return States.SUBJECT


def subject_handler(update: Update, context: CallbackContext):
    context.user_data[States.SUBJECT] = update.message.text
    logger.info("subject_handler function call (user: {user_id}, data: {data})".format(user_id=update.effective_user.id,
                                                                                       data=context.user_data))
    strings = get_localize(User().get_lang())
    update.message.reply_text(
        text="\n".join(['%s: %s' % (k, v) for k, v in context.user_data.items()]),
        reply_markup=get_menu_keyboard()
    )
    context.user_data.clear()
    return ConversationHandler.END


def back_handler(update: Update, context: CallbackContext):
    last_state: States = context.user_data["last_state"]
    logger.info("back_handler function call (user: {user_id}, last state: {last_state})".format(
        user_id=update.effective_user.id,
        last_state=last_state))

    if last_state.value == 0:
        strings = get_localize(User().get_lang())
        update.message.reply_text(
            text=strings.use_keyb,
            reply_markup=get_menu_keyboard()
        )
        context.user_data.clear()
        return ConversationHandler.END
    else:
        context.user_data["last_state"] = States(last_state.value - 1)
        next_message(update, context)
        return context.user_data["last_state"]


def exit_handler(update: Update, context: CallbackContext):
    logger.info("user {user_id} exit from conversation".format(user_id=update.effective_user.id))
    context.user_data.clear()
    strings = get_localize(User().get_lang())
    update.message.reply_text(
        text=strings.use_keyb,
        reply_markup=get_menu_keyboard()
    )
    return ConversationHandler.END


def next_message(update: Update, context: CallbackContext):
    state: States = context.user_data["last_state"]
    bot = context.bot
    strings = get_localize(User().get_lang())

    if state == States.FACULTY:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Faculty: ",
            reply_markup=ReplyKeyboardMarkup([[strings.back], [strings.exit]], resize_keyboard=True)
        )
    elif state == States.YEAR:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Year: ",
            reply_markup=ReplyKeyboardMarkup([[strings.back], [strings.exit]], resize_keyboard=True)
        )
    elif state == States.SPECIALITY:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Speciality: ",
            reply_markup=ReplyKeyboardMarkup([[strings.back], [strings.exit]], resize_keyboard=True)
        )
    elif state == States.SUBJECT:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Subject: ",
            reply_markup=ReplyKeyboardMarkup([[strings.back], [strings.exit]], resize_keyboard=True)
        )


def get_handler() -> ConversationHandler:
    back_ukr = get_localize("ukr").back
    back_eng = get_localize("eng").back
    back_names = [back_ukr, back_eng]

    exit_ukr = get_localize("ukr").exit
    exit_eng = get_localize("eng").exit
    exit_names = [exit_ukr, exit_eng]

    conv_handl = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.text, menu)
        ],
        states={
            States.FACULTY: [
                MessageHandler(Filters.text(back_names), back_handler, pass_user_data=True),
                # Filter is temporary and have to be replaced with list of reply keyboard buttons
                MessageHandler(Filters.text('f'), faculty_handler, pass_user_data=True)
            ],
            States.YEAR: [
                MessageHandler(Filters.text(back_names), back_handler, pass_user_data=True),
                # Filter is temporary and have to be replaced with list of reply keyboard buttons
                MessageHandler(Filters.text('y'), year_handler, pass_user_data=True)
            ],
            States.SPECIALITY: [
                MessageHandler(Filters.text(back_names), back_handler, pass_user_data=True),
                # Filter is temporary and have to be replaced with list of reply keyboard buttons
                MessageHandler(Filters.text('sp'), speciality_handler, pass_user_data=True)
            ],
            States.SUBJECT: [
                MessageHandler(Filters.text(back_names), back_handler, pass_user_data=True),
                # Filter is temporary and have to be replaced with list of reply keyboard buttons
                MessageHandler(Filters.text('sb'), subject_handler, pass_user_data=True)
            ]
        },
        fallbacks=[
            MessageHandler(Filters.text(exit_names), exit_handler, pass_user_data=True)
        ]
    )
    return conv_handl


if __name__ == '__main__':
    print(States.CALC)
