
"""
test version of conversation bot for NDP party virtual 2020
to begin: python3 ndpBot_v1.py
send /start to initiate the conversation
to leave venv: deactivate
to terminate: CTRL-C (not command!)

"""

import logging
from uuid import uuid4

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

AGREE, NAME, GENDER, AGE = range(4)

"""
the functions defined below are callback functions passed to Handlers. Arguments for
different classes of Handler can be found in docs.

some_fun(update, context) is the standard callback signature for the context based API
"""

rules =     """
    We want to keep our Telegram page an open chat, but we are also a “family-friendly” page,
    so please keep comments and wall posts clean. \n

    We want you to tell us what’s on your mind or provide a platform for likeminded individuals
    to connect through their interests, but if it falls into any of the categories below,
    we want to let you know beforehand that we will have to remove it:\n

    1. We do not allow graphic, obscene, explicit or racial comments or
    submissions nor do we allow comments that are abusive, hateful or intended
    to defame anyone or any organization. \n

    2. We do not allow third-party solicitations or advertisements.
    This includes promotion or endorsement of any financial, commercial or non-governmental agency.
    Similarly, we do not allow attempts to defame or defraud any financial,
    commercial or non-governmental agency. \n

    3. We do not allow comments that support or encourage illegal activity. \n

    Let’s make this a safe space for everyone! :D
    """


def start(update, context):
    reply_keyboard = [['Yes', 'No']]

    #sends starting message
    update.message.reply_text(
        ('Hello!\n' + rules),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    #changes state of conv_handler
    return AGREE


def agree(update, context):
    user = update.message.from_user
    logger.info("Agree?: %s", update.message.text)

    #get name
    update.message.reply_text('Great! Your name please')

    #changes state of conv_handler
    return NAME


def name(update, context):
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)

    #store user's name in dict (accessed through context.user_data)
    context.user_data['name'] = update.message.text

    #define next state for conversation
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Ah boy, ah girl, others?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER



def gender(update, context):
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)

    #store user's gender in dict (accessed through context.user_data)
    context.user_data['gender'] = update.message.text

    update.message.reply_text('You how old?')

    return AGE



def age(update, context):
    user = update.message.from_user
    logger.info("Age of %s: %s", user.first_name, update.message.text)

    #store user's age in dict (accessed through context.user_data)
    context.user_data['age'] = update.message.text

    update.message.reply_text('OK ready')

    return ConversationHandler.END



def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



"""
functions below are just to check that data storage is working
"""

def getmyinfo(update, context):
    """Usage: /getmyinfo uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    # Load value
    try:
        value = context.user_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')


def contact(update, context):
    #might be useful for the last step of the bot
    contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
    reply_markup = ReplyKeyboardMarkup(contact_keyboard, one_time_keyboard=True)



def main():
    updater = Updater("1089985624:AAHp-olImnu1Q_i8wRJZlYNQb5B5dwG6vag", use_context=True)
    dp = updater.dispatcher

    #add conversation handler with states defined earlier
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            AGREE: [MessageHandler(Filters.all, agree)],
            NAME: [MessageHandler(Filters.text, name)],
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
            AGE: [MessageHandler(Filters.text, age)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('getmyinfo', getmyinfo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
