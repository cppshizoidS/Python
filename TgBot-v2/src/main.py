import logging
import os

from telegram import Bot
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

import commands.commands as cmd
import commands.handle_callback as clb
import commands.on_message as on_msg

formatter = logging.Formatter("[{asctime}] [{levelname}] [{name}] {message}", style="{")

file_logger = logging.FileHandler('data/events.log')
file_logger.setLevel(logging.INFO)  # everything into the logging file
file_logger.setFormatter(formatter)

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.WARNING)  

logger = logging.getLogger('my-bot')
logger.setLevel(logging.INFO)

logger.addHandler(file_logger)
logger.addHandler(console_logger)


API_Key = os.environ["API_KEY"]

updater = Updater(API_Key, use_context=True)
dispatcher = updater.dispatcher

bot = Bot(token=API_Key)

dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), on_msg.handle_message))

dispatcher.add_handler(CommandHandler(['start'], cmd.start))

dispatcher.add_handler(CommandHandler(['help', 'h'], cmd.send_help))

dispatcher.add_handler(CallbackQueryHandler(clb.handle_callback))

updater.start_polling()
updater.idle()
