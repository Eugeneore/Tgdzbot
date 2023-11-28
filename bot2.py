import telebot
from telebot import types
from settings import *

bot = telebot.TeleBot(token)

menu = False
key_accepted = False
waiting_ob = False
changing_lesson = False
waiting_sr = False
choosen_lesson = None

@bot.message_handler(commands=['start'])
def start(message):
    global choosen_lesson
    choosen_lesson = None

    base = open_file('base')
    if str(message.chat.id) in base:
        bot.send_message(message.chat.id, "Бот работает")
        global menu
        menu = True
        choose(message)
    else:
        bot.send_message(message.chat.id, "Введи ключ")


@bot.message_handler(content_types=['text'])
def choose(message):
    global menu
    global key_accepted
    global waiting_ob
    global waiting_sr
    global changing_lesson
    global choosen_lesson

    base = open_file('base')
    lang_base = open_file('lang_base')
    can_cange_all = open_file('can_change')

    if str(message.chat.id) not in base and not key_accepted:
        if message.text == security_key:
            bot.send_message(message.chat.id, "Ключ принят✅\nТеперь напиши имя")
            menu = True
            key_accepted = True
        else:
            bot.send_message(message.chat.id, "Ключ не верный⛔")

    elif str(message.chat.id) not in base and key_accepted:
        add_to_file(f"{message.chat.id}\n{message.text}\n", 'base.txt')
        bot.send_message(message.chat.id, "Дальше")
        choose(message)

    elif str(message.chat.id) not in lang_base and message.text not in groups_s:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Английский язык группа 1 (Храмова)")
        button2 = types.KeyboardButton("Английский язык группа 2 (Любовь Борисовна)")
        button3 = types.KeyboardButton("Немецкий язык")
        markup.row(button1, button2)
        markup.add(button3)
        bot.send_message(message.chat.id, "Выбери кто ты:", reply_markup=markup)

    elif str(message.chat.id) not in lang_base and message.text in groups_s:
        add_to_file(f'{message.chat.id}\n{groups[groups_s.index(message.text)]}\n', "lang_base.txt")
        bot.send_message(message.chat.id, "Теперь можешь пользоваться ботом 🙂")
        menu = True
        choose(message)

    elif str(message.chat.id) not in lang_base:
        bot.send_message(message.chat.id, "Ты чё-то не то послал")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Английский язык группа 1 (Храмова)")
        button2 = types.KeyboardButton("Английский язык группа 2 (Любовь Борисовна)")
        button3 = types.KeyboardButton("Немецкий язык")
        markup.row(button1, button2)
        markup.add(button3)
        bot.send_message(message.chat.id, "Выбери кто ты:", reply_markup=markup)

    elif waiting_sr:
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("В меню")
            markup.add(button1)

            l = [int(i) for i in message.text.split()]
            bot.send_message(message.chat.id, f"{sum(l) / len(l)}", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "Что-то не так")
            menu = True
            waiting_sr = False
            choose(message)

    elif menu:
        menu = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Домашнее задание📖")
        button2 = types.KeyboardButton("Изменение домашки🔐")
        button3 = types.KeyboardButton("Объявление 📢")
        button4 = types.KeyboardButton("Разное")
        markup.add(button)
        markup.add(button2)
        markup.add(button3)
        markup.row(button4)
        bot.send_message(message.chat.id, "Выбери что тебе нужно:", reply_markup=markup)

    elif message.text == "Разное":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        ex = types.KeyboardButton("В меню")
        button = types.KeyboardButton("Расписание 📋")
        button1 = types.KeyboardButton("Среднее арифметическое")
        button2 = types.KeyboardButton("Информация о четверти")
        markup.add(ex)
        markup.row(button, button2)
        markup.add(button1)
        bot.send_message(message.chat.id, "Выбери что тебе нужно:",reply_markup=markup)

    elif message.text == "Информация о четверти":
        che = open("chet_info.txt", "r+", encoding=("utf-8"))
        chet = che.readlines()
        chet = [i[:len(i) - 1] for i in chet]
        che.close()

        bot.send_message(message.chat.id, f"Четверть:{chet[0]}\nНачало:{chet[4]}, {chet[5]}\nКонец через +-{chet[1]} дня(рабочих), +-{chet[2]} в {chet[3]}")

    elif message.text == "Среднее арифметическое":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Отмена")
        markup.add(button1)

        bot.send_message(message.chat.id, "Отправьте числа через пробел", reply_markup=markup)
        waiting_sr = True

    elif message.text == "Расписание 📋":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("В меню")
        button2 = types.KeyboardButton("Изменить расписание 🔐(пока не работает)")
        markup.add(button1)
        markup.add(button2)
        bot.send_message(message.chat.id, f"{rasp}", reply_markup=markup)

    elif message.text == "В меню" or message.text == "Отмена":
        menu = True
        waiting_ob = False
        waiting_sr = False
        choosen_lesson = None
        choose(message)

    elif message.text == "Изменить расписание 🔐(пока не работает)":
        bot.send_message(message.chat.id, "Пока не работает")
        menu = True
        choose(message)

    elif message.text == "Объявление 📢":
        if str(message.chat.id) in can_cange_all:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Отмена")
            bot.send_message(message.chat.id, "Отправьте объявление", reply_markup=markup)
            waiting_ob = True
        else:
            bot.send_message(message.chat.id, "Эээ куда лезем")
            menu = True
            choose(message)

    elif waiting_ob:
        ob(base, message.text, bot)
        bot.send_message(message.chat.id, "Объявление объявлено, хз не шарю за русский")
        waiting_ob = False
        menu = True
        choose(message)

    elif message.text == "Домашнее задание📖" or message.text == "Изменение домашки🔐":
        if message.text == "Изменение домашки🔐" and str(message.chat.id) in can_cange_all:
            changing_lesson = True

        msg = "Дз:\n"
        for i in range(0, len(lessons_technik)):
            if send_info_about_lesson(lessons_technik[i]) != "не заполнено":
                msg += lessons_technik_s[i] + ": есть\n"
            else:
                msg += lessons_technik_s[i] + ": нет\n"
        bot.send_message(message.chat.id, msg)

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
        button_exit = types.KeyboardButton("В меню")

        lang1 = types.KeyboardButton("Англ.яз")
        lang2 = types.KeyboardButton("Нем.яз")

        markup.add(button_exit)
        markup.row(lang1, lang2)
        markup.row(button2, button3, button4)
        markup.row(button5, button6, button7)
        markup.row(button8, button9, button10)
        markup.row(button11, button12, button13)

        bot.send_message(message.chat.id, "Какой вам нужен урок?", reply_markup=markup)

    elif message.text in lessons_s:
        if not changing_lesson:
            if message.text not in ["Англ.яз", "Нем.яз"]:
                choosen_lesson = lessons[lessons_s.index(message.text)]
            else:
                lang = open_file("lang_base")
                choosen_lesson = ["eng_", "nem_"][["Англ.яз", "Нем.яз"].index(message.text)] + lang[lang.index(f"{message.chat.id}") + 1]

            if send_info_about_lesson(choosen_lesson) != "не заполнено":
                bot.send_message(message.chat.id, f"По этому предмету задано:\n{send_info_about_lesson(choosen_lesson)}")
                if choosen_lesson in photos:
                    f = open("photos/photos.txt", "r+")
                    b = f.readlines()
                    l = [i[:len(i) - 1] for i in b]
                    f.close()
                    if choosen_lesson in l:
                        photo = open(f"photos/{choosen_lesson}.png", "rb")
                        bot.send_photo(message.chat.id, photo)
            else:
                bot.send_message(message.chat.id, "Нет информации. Либо урок не заполнен, либо ничего не задано")

        else:
            if message.text not in ["Англ.яз", "Нем.яз"]:
                choosen_lesson = lessons[lessons_s.index(message.text)]
            else:
                lang = open_file("lang_base")
                choosen_lesson = ["eng_", "nem_"][["Англ.яз", "Нем.яз"].index(message.text)] + lang[lang.index(f"{message.chat.id}") + 1]

            changing_lesson = False

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Да")
            button1 = types.KeyboardButton("Отмена")
            button2 = types.KeyboardButton("Удалить письменное дз")
            ph = types.KeyboardButton("Добавить фото")
            del_ph = types.KeyboardButton("Удалить фото")
            markup.row(button, button1)
            markup.add(button2)
            markup.add(ph, del_ph)

            if message.text not in ["Англ.яз", "Нем.яз"]:
                choosen_lesson = lessons[lessons_s.index(message.text)]
            else:
                lang = open_file("lang_base")
                choosen_lesson = ["eng_", "nem_"][["Англ.яз", "Нем.яз"].index(message.text)] + lang[lang.index(f"{message.chat.id}") + 1]

            if send_info_about_lesson(choosen_lesson) != "не заполнено":
                bot.send_message(message.chat.id, f"По этому предмету задано:\n{send_info_about_lesson(choosen_lesson)}хотите изменить?", reply_markup=markup)
                if choosen_lesson in photos:
                    f = open("photos/photos.txt", "r+")
                    b = f.readlines()
                    l = [i[:len(i) - 1] for i in b]
                    f.close()
                    if choosen_lesson in l:
                        photo = open(f"photos/{choosen_lesson}.png", "rb")
                        bot.send_photo(message.chat.id, photo)
            else:
                bot.send_message(message.chat.id, "Урок не заполнен", reply_markup=markup)

    elif message.text == "Да" and str(message.chat.id) in can_cange_all and choosen_lesson != None:
        bot.send_message(message.chat.id, "Отправьте новое дз")

    elif message.text == "Удалить письменное дз" and str(message.chat.id) in can_cange_all and choosen_lesson != None:
        replace_in_file("-", f"{choosen_lesson}", "Domashka")
        bot.send_message(message.chat.id, "Дз удалено!")
        print(choosen_lesson, message.chat.id)


    elif str(message.chat.id) in can_cange_all and message.text == "Удалить фото" and choosen_lesson != None:
        if choosen_lesson in photos:
            f = open('photos/photos.txt', 'r+')
            l = f.readlines()
            f.close()
            f = open("photos/photos.txt", "w")
            for i in range(0, len(l)):
                if l[i][:len(l[i]) - 1] != choosen_lesson:
                    f.write(l[i])
                else:
                    continue
            bot.send_message(message.chat.id, "Фото удалено!")

        else:
            bot.send_message(message.chat.id, "Фото не может быть удалено, так как оно не может быть добавлено!")

    elif message.text == "Добавить фото" and str(message.chat.id) in can_cange_all:
        if choosen_lesson in photos:
            bot.send_message(message.chat.id, "Отправьте фото")
        else:
            bot.send_message(message.chat.id, "Этот предмет не поддерживает фото, попросите добавить его в список!")

    elif str(message.chat.id) in can_cange_all and choosen_lesson != None:
        replace_in_file(message.text, choosen_lesson, "Domashka")
        bot.send_message(message.chat.id, "Дз заменено!")
        print(choosen_lesson, message.chat.id)

    else:
        bot.send_message(message.chat.id, "Возможно меня перезапускали или ещё чё. Короче я не понял чё от меня хотят давай всё заново если чё пиши @Zhenka103201")


@bot.message_handler(content_types=['photo'])
def photo(message):
    global choosen_lesson
    global menu
    global waiting_ob

    can_cange_all = open_file('can_change')

    if not waiting_ob:
        if choosen_lesson in photos and str(message.chat.id) in can_cange_all:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = '/Users/EI/PycharmProjects/tgdzbot/photos/' + f"{choosen_lesson}.png"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            f = open("photos/photos.txt", "r+")
            l = f.readlines()
            f.close()
            f = open("photos/photos.txt", "w+")
            f.write(choosen_lesson + "\n")
            for i in range(0, len(l)):
                if l[i][:len(l[i]) - 1] != choosen_lesson:
                    f.write(l[i])
                else:
                    continue
            bot.send_message(message.chat.id, "Фото добавлено!")
            print(choosen_lesson, message.chat.id)

        else:
            bot.send_message(message.chat.id, "пж не нада так делать")
    else:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = '/Users/EI/PycharmProjects/tgdzbot/' + f"ob.png"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        base = open_file('base')
        ob_photo(base, bot)
        bot.send_message(message.chat.id, "Фото отправлено!")


bot.infinity_polling()
