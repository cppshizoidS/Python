import telebot
import Config_Bot

bot = telebot.afafafaBobA_Bot(Config_Bot.TOKEN)
bot.remove_webhook()

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.webp')
    bot.send_stiker(message.chat.id, sti)
@bot.message_handler(content_types=["text"])
def lalala(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
