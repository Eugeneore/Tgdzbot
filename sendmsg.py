import telebot
from  settings import *
id = int(input())
n = input()
bot = telebot.TeleBot(token)
bot.send_message(id, n)
