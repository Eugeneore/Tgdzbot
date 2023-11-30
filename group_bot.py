import telebot
from telebot import types
from settings import *
import time

token = '6959560969:AAFPQti8yRx7ijfwPi-d17K7ydXQc5ALFlA'

bot = telebot.TeleBot(token)

key = 'Groupbotkey1488'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот работает если не знаете как пользоваться напишите /help")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start - перезапуск если сломался\n/dz - дз по всем предметам(пока не работает)\n /dzt - дз на завтра(пока не работает)\n/rasp - расписание\n/mute - замутить\n/unmute - размутить\n/kick - удалить человека\nвсё мне лень больше писать👺")


@bot.message_handler(commands=['rasp'])
def rasp1(message):
    bot.send_message(message.chat.id, rasp)


@bot.message_handler(commands=['kick'])
def kick_user(message):
    print(message)
    if message.reply_to_message or message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status
        admins = open_file('groupbotadminlist')
        if sender_status == "administrator" or sender_status == 'creator' or str(message.chat.id) in admins:
            if user_status == 'administrator' or user_status == 'creator' or message.reply_to_message.from_user.is_bot or str(message.chat.id) in admins:
                bot.reply_to(message, "Невозможно кикнуть")
            else:
                bot.kick_chat_member(chat_id, user_id)
                bot.reply_to(message, f"{message.reply_to_message.from_user.username} кикнули")
    else:
        bot.reply_to(message.chat.id, "Надо использовать пересылая сообщение чела")


@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status
        admins = open_file('groupbotadminlist')
        if sender_status == "administrator" or sender_status == 'creator' or str(message.chat.id) in admins:
            if user_status == 'creator':
                bot.reply_to(message, "Это админ...")
            else:
                duration = 60
                args = message.text.split()[1:]
                if args:
                    try:
                        duration = int(args[0])
                    except ValueError:
                        bot.reply_to(message, "Ошибка")
                        return

                    if duration < 1 or duration > 1440:
                        bot.reply_to(message, "Время должно быть положительным и не больше 1 дня")
                        return

                bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration * 60)
                bot.reply_to(message, f"Был замучен на {duration} минут")
        else:
            bot.send_message(message.chat.id, "Только админ может")
    else:
        bot.reply_to(message, "Надо использовать пересылая сообщение чела")


@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        sender_status = bot.get_chat_member(chat_id, message.from_user.id).status
        admins = open_file('groupbotadminlist')
        if sender_status == "administrator" or sender_status == 'creator' or str(message.chat.id) in admins:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
            bot.reply_to(message, f"{message.reply_to_message.from_user.username} размучен")
    else:
        bot.reply_to(message, "Надо использовать на сообщение чела")


@bot.message_handler(commands=['dz'])
def dz(message):
    msg = "Дз:\n"
    for i in range(0, len(lessons_technik)):
        if send_info_about_lesson(lessons_technik[i]) != "не заполнено":
            msg += lessons_technik_s[i] + f": {send_info_about_lesson(lessons_technik[i])}\n"
        else:
            msg += lessons_technik_s[i] + ": нет\n"
    msg += "Если написано фото посмотрите в боте"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['dzt'])
def dzt(message):
    bot.send_message(message.chat.id, "БРАВЛ СТРАС КАВНО")


@bot.message_handler(content_types=['text'])
def answer(message):
    if "Скинтье" in message.text or "скиньте" in message.text:
        bot.send_message(message.chat.id, "спрашивать для лохов")

    else:
        for i in ["пизд", "бля", "Пизд", "Бля", "БЛЯ", "хуй"]:
            if i in message.text:
                bot.send_message(message.chat.id, "Предупреждение за мат! замучу!")
                bot.delete_message(message.chat.id, message.id)


bot.infinity_polling()