import telebot

token = '5416555935:AAElSn2VaAIctz9ppEjNOy9iAwVwvtlOokA'

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def fdsfds(message):
    print(message.chat.id)
    bot.send_message(message.chat.id, "бравл старс говон")

bot.infinity_polling()