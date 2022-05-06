import logging
import traceback

from telegram import Update, CallbackQuery, InlineKeyboardMarkup
from telegram.ext import CallbackContext

import commands.inline_commands as incmd  # place for your inline commands
import commands.keyboards as kb
import utils.utils as utl

logger = logging.getLogger('my-bot')


def handle_callback(update: Update, context: CallbackContext):
    command_switch = {
        # TODO: REGISTER INLINE COMMANDS HERE
        'foo': incmd.foo_command,
        'bar': incmd.bar_command,
    }

    query: CallbackQuery = update.callback_query
    query.answer()
    key = query.data

    if key.startswith('clear_'):
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[]]))
        key = key.replace('clear_', '')

    send_new_message = False  # to toggle a new message at the end
    if key.startswith('new_'):
        key = key.replace('new_', '')
        send_new_message = True


    try:
        command = command_switch[key]
        if command.__module__ == 'commands.inline_commands':
            command(query)

        if send_new_message:
            utl.send_msg(query, context, "What's next?", keyboard=kb.main_menu)

    except KeyError:
        logger.error(f"CAN'T FIND COMMAND {key} IN COMMAND_SWITCH\n{traceback.format_exc()}")
        print(f'{key} was NOT listed!')
