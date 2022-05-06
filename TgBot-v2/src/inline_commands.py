from telegram import CallbackQuery
from telegram.error import BadRequest

import utils.utils as utl
import commands.keyboards as kb


def foo_command(query: CallbackQuery):
    try:
        query.edit_message_text(
            utl.prep_for_md("This is *foo*", ignore=['*']),
            reply_markup=kb.main_menu,
            parse_mode='MarkdownV2')

    except BadRequest as e:
        print("Bad request")
        print(e)


def bar_command(query: CallbackQuery):
    try:
        query.edit_message_text("This is bar", reply_markup=kb.main_menu)

    except BadRequest as e:
        print("Bad request")
        print(e)

