import telebot
import Config_Bot

bot = telebot.TeleBot(Config_Bot.TOKEN)
bot.remove_webhook()


@bot.message_handler(content_types=["text"])
def lalala(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
