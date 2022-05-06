from typing import Union, List

from sqlalchemy import select
from sqlalchemy.engine import Row
from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

import database.db as db


def send_msg(update: Union[Update, CallbackQuery], context: CallbackContext, text, keyboard=None, parse_mode=''):
    if parse_mode == 'md':
        parse_mode = 'MarkdownV2'
    context.bot.send_message(chat_id=update.message.chat_id,
                             reply_markup=keyboard,
                             text=text,
                             parse_mode=parse_mode)


def prep_for_md(text: str, ignore=None) -> str:

    symbols = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    if ignore:
        for s in ignore:
            symbols.remove(s)

    for s in symbols:
        # print(f'{s}', '\{}'.format(s))
        text = text.replace(f'{s}', '\{}'.format(s))
    return text


def get_entries_by_chat_id(chat_id: int, database=db.Users) -> List[Union[db.Users]]:

    # get entries from entered database
    session = db.open_session()
    statement: List[Row] = select(database).where(database.chat_id == chat_id)

    # extract entry objects from row objects
    entries = [e[0] for e in session.execute(statement).all()]
    return entries


def get_help_text() -> str:
    """:return: central help text in markdown style"""
    return prep_for_md("This is the place for *your custom help text*.\n\nThanks for using my template btw!\n_chris_",
                       ignore=['_', '*'])
