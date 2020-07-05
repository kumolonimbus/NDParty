
"""
test version of conversation bot for NDP party virtual 2020
to enter venv: source env/bin/activate
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

RULES, INTRO, NAME, GENDER, AGE = range(3)

"""
the functions defined below are callback functions passed to Handlers. Arguments for
different classes of Handler can be found in docs.

some_fun(update, context) is the standard callback signature for the context based API
"""

def start(update, context):

    #sends starting message and request password
    update.message.reply_text("""
    Welcome to Better To(gather)'s party-matching bot!
    We'll match you with other attendees with similar hobbies or interests. Exciting hor? \n

    You shall not pass...without a password! Please enter:
    """
    )

    #changes state of conv_handler
    return RULES


def rules(update, context):
    user = update.message.from_user
    logger.info("User %s 's password: %s", user.first_name, update.message.text)

    #set reply_keyboard
    reply_keyboard = [["OK, can"]]

    update.message.reply_text(
        """
        OK very nice. Hello!
        This is an open chat, but we are also a “family-friendly” page, so please keep comments and wall posts clean.\n

        We want you to tell us what’s on your mind and provide a platform for likeminded individuals to connect through their interests,
        but please note that content falling into any of the categories below will be removed: \n

        1. We do not allow graphic, obscene, explicit or racial comments or submissions
        nor do we allow comments that are abusive, hateful or intended to defame anyone or any organization. \n

        2.We do not allow third-party solicitations or advertisements.
        This includes promotion or endorsement of any financial, commercial or non-governmental agency.
        Similarly, we do not allow attempts to defame or defraud any financial, commercial or non-governmental agency. \n

        3. We do not allow comments that support or encourage illegal activity. \n

         Let’s make this a safe space for everyone! :-D
        """
    )

    return INTRO


def intro(update, context):
    user = update.message.from_user
    logger.info("User %s says: %s", user.first_name, update.message.text)

    update.message.reply_text('Great! Your name please:')

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

    update.message.reply_text('Okay you want talk to who:')

    return ConversationHandler.END


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



def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END



def main():
    updater = Updater("1089985624:AAHp-olImnu1Q_i8wRJZlYNQb5B5dwG6vag", use_context=True)
    dp = updater.dispatcher

    #add conversation handler with states defined earlier
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            RULES: [MessageHandler(Filters.regex('^password$'), rules)],
            INTRO: [MessageHandler(Filters.text, intro)],
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
