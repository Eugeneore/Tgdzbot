from settings import *
import telebot
from telebot import types

bot = telebot.TeleBot(token)

pon = False

waiting_security_key = False
waiting_name = False
waiting_group = False
waiting_key = False
waiting_lesson = False

@bot.message_handler(commands=["start"])
def start(message):
    global pon
    global waiting_security_key
    # bot.delete_message(message.chat.id, message_id=message.message_id)

    # try:
    #     msg = open_file("last_msg_by_id_by_bot.txt")[open_file("last_msg_by_id_by_bot.txt").index(str(message.chat.id)) + 1]
    # except:
    #     msg = None

    if str(message.chat.id) in open_file("../base.txt"):
        # if msg != None:
        #     standart_msg_send("Чё ты меня стартуешь я и так работаю 👺", msg, bot, message.chat.id)
        # else:
        #     msg = bot.send_message(message.chat.id, "Чё ты меня стартуешь я и так работаю 👺")
        #     add_to_file(str(message.chat.id) + "\n" + str(msg.message_id) + "\n", "last_msg_by_id_by_bot.txt")
        bot.send_message(message.chat.id, 'Чё ты меня стартуешь я и так работаю 👺')

        pon = True
        choose(message)

    else:
        # if msg != None:
        #     standart_msg_send("Введи ключ безопасности 🔑", msg, bot, message.chat.id)
        #     waiting_security_key = True
        # else:
        #     msg = bot.send_message(message.chat.id, "Введи ключ безопасности 🔑")
        #     add_to_file(str(message.chat.id) + "\n" + str(msg.message_id) + "\n", "last_msg_by_id_by_bot.txt")
        #     waiting_security_key = True
        bot.send_message(message.chat.id, "Введи ключ безопасности 🔑")


@bot.message_handler(content_types=['text'])
def choose(message):
    global pon
    global msg
    global waiting_security_key
    global waiting_name
    global waiting_group
    global waiting_key
    global waiting_lesson

    waiting_group = str(message.chat.id) not in open_file("lang_base")

    # try:
    #     msg = open_file("last_msg_by_id_by_bot.txt")[open_file("last_msg_by_id_by_bot.txt").index(str(message.chat.id)) + 1]
    # except:
    #     msg = None

    # try:
    #     # bot.delete_message(message.chat.id, message.message_id)
    # except:
    #     pass

    if waiting_security_key:
        if message.text == security_key:
            # standart_msg_send("Ну ок. Теперь напиши имя", msg, bot, message.chat.id)
            waiting_name = True
            waiting_security_key = False
        else:
            # standart_msg_send("Мне кажется ты перепутал 😑 Давай ещё раз", msg, bot, message.chat.id)
            bot.send_message(message.chat.id, "Мне кажется ты перепутал 😑 Давай ещё раз")

    elif waiting_name:
        name = message.text
        add_to_file(str(message.chat.id) + "\n" + name + "\n", "../base.txt")
        if str(message.chat.id) not in open_file("../lang_base.txt"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            gr1 = types.KeyboardButton("Англ.яз группа 1")
            gr2 = types.KeyboardButton("Англ.яз группа 2 (Любовь Борисовна)")
            gr3 = types.KeyboardButton("Немец.яз")
            markup.row(gr1, gr2)
            markup.add(gr3)
            markup_msg_send("Выбери группу", msg, bot, message.chat.id, markup)
            waiting_group = True
        else:
            pon = True
            choose(message)
        waiting_name = False

    elif waiting_group:
        if message.text in groups_s:
            add_to_file(str(message.chat.id) + "\n" + groups[groups_s.index(message.text)] + "\n", "../lang_base.txt")
            waiting_group = False
            pon = True
            choose(message)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            gr1 = types.KeyboardButton("Англ.яз группа 1")
            gr2 = types.KeyboardButton("Англ.яз группа 2 (Любовь Борисовна)")
            gr3 = types.KeyboardButton("Немец.яз")
            markup.row(gr1, gr2)
            markup.add(gr3)
            markup_msg_send("Выбери группу!", msg, bot, message.chat.id, markup)

    elif waiting_key:
        if message.text == real_key:
            add_to_file(str(message.chat.id), "../can_change.txt")
            # standart_msg_send("Окей", msg, bot, message.chat.id)
            bot.send_message(message.chat.id, "Окей")
            pon = True
            choose(message)
        else:
            # standart_msg_send("Неправильно ⛔", msg, bot, message.chat.id)
            bot.send_message(message.chat.id, "Неправильно ⛔")
            pon = True
            choose(message)

    elif message.text == "Пон" or pon:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Домашнее задание📖")
        button2 = types.KeyboardButton("Изменение домашки🔐")
        markup.add(button)
        markup.add(button2)

        # markup_msg_send("Теперь можешь смотреть дз.", msg, bot, message.chat.id, markup)
        bot.send_message(message.chat.id, "Теперь можешь смотреть дз", reply_markup=markup)

        pon = False
        choose(message)

    elif message.text == "В меню 🔙":
        waiting_lesson = False
        pon = True
        choose(message)

    elif message.text == "Домашнее задание📖":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button2 = types.KeyboardButton("Алгебра 🟰")
        button3 = types.KeyboardButton("Физика 🧑‍🔬")
        button4 = types.KeyboardButton("Лит-ра 📖")
        button5 = types.KeyboardButton("Вероятность 🎲")
        button6 = types.KeyboardButton("Русский язык 🖋️")
        button7 = types.KeyboardButton("География 🌍")
        button8 = types.KeyboardButton("История ⏳")
        button9 = types.KeyboardButton("Геометрия 📐")
        button10 = types.KeyboardButton("Биология 🦠")
        button11 = types.KeyboardButton("Обществознание")
        button12 = types.KeyboardButton("Информатика 💻")
        button13 = types.KeyboardButton("Музыка 🎶")
        button_exit = types.KeyboardButton("В меню 🔙")

        lang1 = types.KeyboardButton("Англ.яз")
        lang2 = types.KeyboardButton("Нем.яз")

        markup.add(button_exit)
        markup.row(lang1, lang2)
        markup.row(button2, button3, button4)
        markup.row(button5, button6, button7)
        markup.row(button8, button9, button10)
        markup.row(button11, button12, button13)

        # markup_msg_send("Выберите урок", msg, bot, message.chat.id, markup)
        bot.send_message(message.chat.id, "Выберите урок", reply_markup=markup)

    elif message.text == "Изменение домашки🔐":
        if str(message.chat.id) in open_file("../can_change.txt"):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button2 = types.KeyboardButton("Алгебра 🟰")
            button3 = types.KeyboardButton("Физика 🧑‍🔬")
            button4 = types.KeyboardButton("Лит-ра 📖")
            button5 = types.KeyboardButton("Вероятность 🎲")
            button6 = types.KeyboardButton("Русский язык 🖋️")
            button7 = types.KeyboardButton("География 🌍")
            button8 = types.KeyboardButton("История ⏳")
            button9 = types.KeyboardButton("Геометрия 📐")
            button10 = types.KeyboardButton("Биология 🦠")
            button11 = types.KeyboardButton("Обществознание")
            button12 = types.KeyboardButton("Информатика 💻")
            button13 = types.KeyboardButton("Музыка 🎶")
            button_exit = types.KeyboardButton("В меню 🔙")

            lang1 = types.KeyboardButton("Англ.яз")
            lang2 = types.KeyboardButton("Нем.яз")

            markup.add(button_exit)
            markup.row(lang1, lang2)
            markup.row(button2, button3, button4)
            markup.row(button5, button6, button7)
            markup.row(button8, button9, button10)
            markup.row(button11, button12, button13)

            markup_msg_send("Выберите урок, который хотите изменить", msg, bot, message.chat.id, markup)
            waiting_lesson = True
        else:
            # standart_msg_send("Код пожалуйста предъявите 🗝️", msg, bot, message.chat.id)
            bot.send_message(message.chat.id, "Код пожалуйста предъявите 🗝️")
            waiting_key = True


    elif message.text in lessons_s:
        if waiting_lesson:
            si = lessons[lessons_s.index(message.text) + 1]
            sial = send_info_about_lesson(si)
            if si in photos:
                f = open("../photos/photos.txt", "r+")
                b = f.readlines()
                l = [i[:len(i) - 1] for i in b]
                f.close()
                if si in l:
                    photo = open(f"photos/{si}.png", "rb")
                    bot.send_photo(message.chat.id, photo)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Да")
            button1 = types.KeyboardButton("Отмена")
            button2 = types.KeyboardButton("Удалить письменное дз")
            ph = types.KeyboardButton("Добавить фото")
            del_ph = types.KeyboardButton("Удалить фото")

            markup_msg_send(f"Дз по предмету: {sial} хотите изменить?", msg, bot, message.chat.id, markup)

        else:
            sial = send_info_about_lesson(lessons[lessons_s.index(message.text) + 1])
            if sial != "не заполнено":
                # standart_msg_send(f"По этому предмету задано:\n{sial}", msg, bot, message.chat.id)
                bot.send_message(message.chat.id, f"По этому предмету задано:\n{sial}")
            else:
                # standart_msg_send("Дз не заполнено", msg, bot, message.chat.id)
                bot.send_message(message.chat.id, "Дз не заполнено")




bot.infinity_polling()
