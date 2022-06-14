from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.helper import Helper, HelperMode, ListItem
import random

from anime import Anime_data, Jutsu

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

jutsu = Jutsu()
all_anime = jutsu.get_all() 
users_data = {}

class States(Helper):
    mode = HelperMode.snake_case
    STATE_SEARCH = ListItem()
    STATE_START = ListItem()
    STATE_SELECT = ListItem()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    search_button = KeyboardButton('найти 🔎')
    random_button = KeyboardButton('рандом 🎲')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(search_button, random_button)
    await bot.send_message(message.chat.id, 'магия ✨', reply_markup=keyboard)
    if not users_data.get(message.from_user.id):
        users_data[message.from_user.id] = Anime_data()
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[2])

@dp.message_handler(commands=['start'], state=States.STATE_START)
async def process_start_command2(message: types.Message):
    search_button = KeyboardButton('найти 🔎')
    random_button = KeyboardButton('рандом 🎲')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(search_button, random_button)
    await bot.send_message(message.chat.id, 'магия ✨', reply_markup=keyboard)
    if not users_data.get(message.from_user.id):
        users_data[message.from_user.id] = Anime_data()

@dp.message_handler(text='найти 🔎', state=States.STATE_START)
async def process_search_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Что искать будем?')
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[0])

@dp.message_handler(text='рандом 🎲', state=States.STATE_START)
async def process_random_command(message: types.Message):
    anime = all_anime[random.randint(0, len(all_anime))]
    anime_data = users_data[message.from_user.id]
    anime_data.set_data(jutsu.get_data(anime.url))
    anime_data.set_name(anime.name)
    anime_button = InlineKeyboardButton('Смотреть ✅', callback_data='anime_button')
    close_button = InlineKeyboardButton('Отмена ❌', callback_data='close_button')
    keyboard = InlineKeyboardMarkup(row_width=1).add(anime_button, close_button)
    await bot.send_photo(message.chat.id, photo=anime.image, reply_markup=keyboard, caption=anime_data.name)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[1])

@dp.message_handler(state=States.STATE_SEARCH)
async def search_state_case(message: types.Message):
    search = False
    for anime in all_anime:
        if message.text.lower() in anime.name.lower():
            search = True
            anime_data = users_data[message.from_user.id]
            anime_data.set_data(jutsu.get_data(anime.url))
            anime_data.set_name(anime.name)
            anime_button = InlineKeyboardButton('Смотреть ✅', callback_data='anime_button')
            close_button = InlineKeyboardButton('Отмена ❌', callback_data='close_button')
            keyboard = InlineKeyboardMarkup(row_width=1).add(anime_button, close_button)
            await bot.send_photo(message.chat.id, photo=anime.image, reply_markup=keyboard, caption=anime_data.name)
            state = dp.current_state(user=message.from_user.id)
            await state.set_state(States.all()[1])
            break
    if not search:
        await bot.send_message(message.chat.id, 'Не удалось найти ☔')
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(States.all()[2])
    
@dp.callback_query_handler(lambda c: c.data == 'close_button', state=States.STATE_SELECT)
async def process_callback_close_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    anime_data = users_data[callback_query.from_user.id]
    await callback_query.message.edit_caption(anime_data.name, reply_markup=None)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.all()[2])

@dp.callback_query_handler(lambda c: c.data == 'anime_button', state=States.STATE_SELECT)
async def process_callback_anime_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    anime_data = users_data[callback_query.from_user.id]
    keyboard = InlineKeyboardMarkup()
    for season in anime_data.seasons:
        keyboard.add(InlineKeyboardButton(season, callback_data=season))
    await callback_query.message.edit_caption(anime_data.name, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in users_data[c.from_user.id].seasons, state=States.STATE_SELECT)
async def process_callback_season_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    anime_data = users_data[callback_query.from_user.id]
    anime_data.select_season(callback_query.data)
    keyboard = InlineKeyboardMarkup()
    for seria in anime_data.series:
        keyboard.add(InlineKeyboardButton(seria, callback_data=seria))
    await callback_query.message.edit_caption(anime_data.name + '\n' + anime_data.season, reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in users_data[c.from_user.id].series, state=States.STATE_SELECT)
async def process_callback_seria_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    anime_data = users_data[callback_query.from_user.id]
    anime_data.select_seria(callback_query.data)
    await callback_query.message.edit_caption(anime_data.name + '\n' + anime_data.season + '\n' + anime_data.seria, reply_markup=None)
    await bot.send_message(callback_query.from_user.id, anime_data.url())
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(States.all()[2])

@dp.message_handler()
async def process_message(message: types.Message):
    await bot.send_message(message.chat.id, 'используй /start чтобы начать')

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
