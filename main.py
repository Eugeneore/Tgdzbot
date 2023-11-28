import telebot
from telebot import types
from settings import ob


def replace_last_msg_id(chat_id, msg):
    l = clear_file("last_msg_by_id_by_bot.txt")
    file = open("last_msg_by_id_by_bot.txt", "w")
    for i in range(0, len(l)):
        if i != l.index(chat_id) + 1:
            file.write(l[i] + "\n")
        else:
            file.write(msg + "\n")
    file.close()


def replace_dz(dz, lesson):
    l = clear_file("Domashka.txt")
    f = open("Domashka.txt", "w", encoding=("utf-8"))
    for i in range(0, len(l)):
        if i != l.index(lesson) + 1:
            f.write(l[i] + "\n")
        else:
            f.write(dz + "\n")
    f.close()


def send_info_about_lesson(lesson):
    l = clear_file("Domashka.txt")
    if l[l.index(lesson) + 1] == "-":
        if lesson in photos:
            f = open("photos/photos.txt", "r+")
            li = f.readlines()
            li = [i[:len(i) - 1] for i in li]
            f.close()
            if lesson in li:
                return "фото"
            else:
                return "не заполнено"
        else:
            return "не заполнено"
    else:
        return f"{l[l.index(lesson) + 1]} \n"


def clear_file(f):
    file = open(f"{f}", 'r+', encoding=("utf-8"))

    m = file.readlines()
    ma = []
    file.close()
    for i in range(0, len(m)):
        if m[i] != '':
            ma.append(m[i][:len(m[i]) - 1])
        else:
            ma.append('')
    return ma


def open_file(file):
    f = open(f"{file}.txt", "r+")
    f_ = f.readlines()
    f_a = [i[:len(i) - 1] for i in f_]
    f.close()
    return f_a


token = '6353183402:AAGcx4MYwwHUgEm4OQvUBBWvh_dCywBkYBc'

was_sended = False
pon = None
waiting_lesson = False
choosen_lesson = None
waiting_key = False
waiting_security_key = False
waiting_ob = False
changing = False

key = None
real_key = 'key_from_using_the_bot_do_not_share_that'

bot = telebot.TeleBot(token)

lessons = ["langs", "algebra", "phisic", "lit_ra", "teoriya_ver", "russ_yaz", "geography",
           "history", "geometry", "biology", "obshestvo", "ITC", "musik"]

languages = ["eng_eng1", "eng_eng2", "nem_eng1", "nem_eng2", "eng_nem", "nem_nem"]
languages_s = ["Англ.яз группа 1", "Англ.яз группа2 ", "Нем.яз группа 1", "Нем.яз группа 2", "Англ.яз", "Нем.яз"]

lessons_s = ["Языки 🌐","Алгебра 🟰", "Физика 🧑‍🔬", "Лит-ра 📖", "Вероятность 🎲", "Русский язык 🖋️", "География 🌍",
             "История ⏳", "Геометрия 📐", "Биология 🦠", "Обществознание", "Информатика 💻", "Музыка 🎶"]

photos = ["algebra", "phisic", "teoriya_ver", "russ_yaz", "geography", "geometry", "nem_nem", "eng_nem", "lit_ra", "eng_eng1", "eng_eng2", "nem_eng1", "nem_eng2"]

security_key = "key_from_bot_7b_1488"

@bot.message_handler(commands=["start"])
def start(message):
    base_all = open_file("base")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Пон")
    markup.add(button)

    if str(message.chat.id) not in base_all:
        bot.send_message(message.chat.id, "Так введи ключ от бота 🔑")
        global waiting_security_key
        waiting_security_key = True
    else:
        bot.send_message(message.chat.id, "Дз каждый день!", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choose(message):

    base_all = open_file("base")
    can_change_all = open_file("can_change")
    lang_base = open_file("lang_base")

    global name
    global waiting_security_key
    global pon
    global msg
    global waiting_ob

    if str(message.chat.id) not in base_all:
        if not waiting_security_key:
            if message.text not in lessons_s and message.text not in languages_s and message.text != "Домашнее задание📖" and message.text != "Изменение домашки🔐" and message.text != "В меню 🔙" and message.text != real_key:
                pon = True
                name = message.text
                print(name)
                base = open('base.txt', "a")
                base.write(str(message.chat.id) + '\n')
                base.write(name + "\n")
                base.close()
                choose(message)
            else:
                bot.send_message(message.chat.id, "Ошибка: введите имя")

        else:
            global security_key
            if message.text == security_key:
                bot.send_message(message.chat.id, "Теперь напиши пожалуйста имя")
                waiting_security_key = False
            else:
                bot.send_message(message.chat.id, "Мне кажется ты перепутал 😑")

    elif str(message.chat.id) not in lang_base:
        if message.text in ["Англ.яз группа 1", "Англ.яз группа 2 (Любовь Борисовна)", "Немец.яз"]:
            f = open("lang_base.txt", "a")
            f.write(str(message.chat.id) + "\n")
            m = ["eng1", "eng2", "nem"]
            m2 = ["Англ.яз группа 1", "Англ.яз группа 2 (Любовь Борисовна)", "Немец.яз"]
            f.write(m[m2.index(message.text)] + "\n")
            f.close()
            pon = True
            choose(message)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            gr1 = types.KeyboardButton("Англ.яз группа 1")
            gr2 = types.KeyboardButton("Англ.яз группа 2 (Любовь Борисовна)")
            gr3 = types.KeyboardButton("Немец.яз ")
            markup.row(gr1, gr2)
            markup.add(gr3)

            bot.send_message(message.chat.id, "Пожалуйста выберете группу/основной язык", reply_markup=markup)

    elif message.text == "Пон" or pon == True:
        pon = False
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Домашнее задание📖")
        button2 = types.KeyboardButton("Изменение домашки🔐")
        button3 = types.KeyboardButton("Объявление 📢")
        markup.add(button)
        markup.add(button2)
        markup.add(button3)

        bot.send_message(message.chat.id, "Теперь ты можешь получать новое дз 🙂", reply_markup=markup)

    elif message.text == "Объявление 📢":
        if str(message.chat.id) in can_change_all:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Отмена")
            markup.add(button)
            bot.send_message(message.chat.id, "Отправьте объявление", reply_markup=markup)
            waiting_ob = True
        else:
            bot.send_message(message.chat.id, "Тебе нельзя")
            pon = True
            choose(message)

    elif waiting_ob:
        ob(base_all, message.text, bot)
        bot.send_message(message.chat.id, "Объявление отправлено!")
        pon = True
        choose(message)
        waiting_ob = False

    elif message.text == "Домашнее задание📖":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Языки 🌐")
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

        # lang1 = types.KeyboardButton("Англ.яз")
        # lang2 = types.KeyboardButton("Нем.яз")

        markup.add(button, button_exit)
        # markup.row(lang1, lang2)
        markup.row(button2, button3, button4)
        markup.row(button5, button6, button7)
        markup.row(button8, button9, button10)
        markup.row(button11, button12, button13)

        bot.send_message(message.chat.id, "Какой вам нужен урок?", reply_markup=markup)

    elif message.text == "Изменение домашки🔐":
        if str(message.chat.id) in can_change_all:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Языки 🌐")
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
            markup.add(button, button_exit)
            markup.row(button2, button3, button4)
            markup.row(button5, button6, button7)
            markup.row(button8, button9, button10)
            markup.row(button11, button12, button13)

            bot.send_message(message.chat.id, "Какой урок вы хотите изменить языки будут изменяться под выбранную группу: ", reply_markup=markup)
            global waiting_lesson
            waiting_lesson = True
        else:
            bot.send_message(message.chat.id, "Введи ключ!")
            global waiting_key
            waiting_key = True

    elif message.text == "Отмена" or message.text == "В меню 🔙":
        waiting_ob = False
        waiting_lesson = False
        pon = True
        choose(message)

    elif message.text == "Да":
        if str(message.chat.id) in can_change_all:
            global changing
            bot.send_message(message.chat.id, "Напишите дз")
            changing = True
            waiting_lesson = False

    elif message.text == "Добавить фото":
        global choosen_lesson
        if choosen_lesson in photos:
            bot.send_message(message.chat.id, "Отправьте фото")
        else:
            bot.send_message(message.chat.id, "Этот предмет не поддерживает фото, попросите добавить его в список!")

    elif message.text == "Удалить фото":
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
            bot.send_message(message.chat.id, "Нет предмета в списке с фото")

    elif message.text == "Удалить письменное дз":
        if send_info_about_lesson(choosen_lesson) != "не заполнено":
            f = open("Domashka.txt", "r+")
            li = f.readlines()
            li = [i[:len(i) - 1] for i in li]
            f.close()
            f = open("Domashka.txt", 'w')
            for i in range(0, len(li)):
                if i != li.index(choosen_lesson) + 1:
                    f.write(li[i] + "\n")
                else:
                    f.write("-" + "\n")
            f.close()
            bot.send_message(message.chat.id, "Дз удалено")
            pon = True
        else:
            bot.send_message(message.chat.id, "Дз и так не заполнено")

    elif message.text in languages_s:
        if waiting_lesson:
            choosen_lesson = languages[languages_s.index(message.text)]
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Да")
            button1 = types.KeyboardButton("Отмена")
            button2 = types.KeyboardButton("Удалить письменное дз")
            ph = types.KeyboardButton("Добавить фото")
            del_ph = types.KeyboardButton("Удалить фото")

            if choosen_lesson in photos:
                f = open("photos/photos.txt", "r+")
                b = f.readlines()
                l = [i[:len(i) - 1] for i in b]
                f.close()
                if choosen_lesson in l:
                    photo = open(f"{choosen_lesson}.png", "rb")
                    bot.send_photo(message.chat.id, photo)
            markup.row(button, button1)
            markup.add(button2)
            markup.add(ph, del_ph)

            bot.send_message(message.chat.id, f"Дз по предмету: {send_info_about_lesson(choosen_lesson)} хотите изменить?", reply_markup=markup)
        else:
            choosen_lesson = languages[languages_s.index(message.text)]
            if choosen_lesson in photos:
                f = open("photos/photos.txt", "r+")
                b = f.readlines()
                l = [i[:len(i) - 1] for i in b]
                f.close()
                if choosen_lesson in l:
                    photo = open(f"photos/{choosen_lesson}.png", "rb")
                    bot.send_photo(message.chat.id, photo)
            if send_info_about_lesson(choosen_lesson) != "не заполнено":
                bot.send_message(message.chat.id, f"По этому предмету задано:\n{send_info_about_lesson(choosen_lesson)}")
            else:
                bot.send_message(message.chat.id, "Нет информации. Либо урок не заполнен, либо ничего не задано")

    else:
        if waiting_key:
            key = message.text
            if key == real_key:
                change = open("can_change.txt", "a")
                change.write(str(message.chat.id) + "\n")
                change.close()
                bot.send_message(message.chat.id, "Ключ принят ✅")
            else:
                bot.send_message(message.chat.id, "Неверно ⛔")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("Домашнее задание📖")
            button2 = types.KeyboardButton("Изменение домашки🔐")
            markup.add(button)
            markup.add(button2)
            bot.send_message(message.chat.id, "Теперь ты можешь получать новое дз 🙂", reply_markup=markup)
            waiting_key = False
        elif waiting_lesson:
            if message.text in lessons_s:
                if message.text != "Языки 🌐":
                    choosen_lesson = lessons[lessons_s.index(message.text)]
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button = types.KeyboardButton("Да")
                    button1 = types.KeyboardButton("Отмена")
                    button2 = types.KeyboardButton("Удалить письменное дз")
                    ph = types.KeyboardButton("Добавить фото")
                    del_ph = types.KeyboardButton("Удалить фото")
                    markup.row(button, button1)
                    markup.add(button2)
                    markup.add(ph, del_ph)
                    bot.send_message(message.chat.id, f"Дз по предмету: {send_info_about_lesson(choosen_lesson)} хотите изменить?", reply_markup=markup)
                    if choosen_lesson in photos:
                        f = open("photos/photos.txt", "r+")
                        b = f.readlines()
                        l = [i[:len(i) - 1] for i in b]
                        f.close()
                        if choosen_lesson in l:
                            photo = open(f"photos/{choosen_lesson}.png", "rb")
                            bot.send_photo(message.chat.id, photo)
                    waiting_lesson = False
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    ang = types.KeyboardButton("ОСНОВНОЙ АНГЛИЙСКИЙ")
                    exitm = types.KeyboardButton("В меню 🔙")
                    markup.row(ang, exitm)
                    button = types.KeyboardButton("Нем.яз группа 1")
                    button2 = types.KeyboardButton("Нем.яз группа 2")
                    button3 = types.KeyboardButton("Англ.яз группа 1")
                    button4 = types.KeyboardButton("Англ.яз группа 2")
                    markup.row(button, button2, button3, button4)
                    nem = types.KeyboardButton("ОСНОВНОЙ НЕМЕЦКИЙ")
                    markup.add(nem)
                    button5 = types.KeyboardButton("Нем.яз")
                    button6 = types.KeyboardButton("Англ.яз")
                    markup.row(button5, button6)
                    bot.send_message(message.chat.id, "Языки", reply_markup=markup)
                    waiting_lesson = True

        elif changing:
            if choosen_lesson != None:
                replace_dz(message.text, choosen_lesson)
                print(choosen_lesson)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button = types.KeyboardButton("ОК")
                markup.add(button)
                bot.send_message(message.chat.id, "Дз заполнено", reply_markup=markup)
                pon = True
            else:
                bot.send_message(message.chat.id, "Не выбран предмет")
            changing = False

        else:
            if message.text in lessons_s:
                if message.text != "Языки 🌐":
                    choosen_lesson = lessons[lessons_s.index(message.text)]
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
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    ang = types.KeyboardButton("ОСНОВНОЙ АНГЛИЙСКИЙ")
                    exitm = types.KeyboardButton("В меню 🔙")
                    markup.add(exitm)
                    markup.add(ang)
                    button = types.KeyboardButton("Нем.яз группа 1")
                    button2 = types.KeyboardButton("Нем.яз группа 2")
                    button3 = types.KeyboardButton("Англ.яз группа 1")
                    button4 = types.KeyboardButton("Англ.яз группа 2")
                    markup.row(button, button2, button3, button4)
                    nem = types.KeyboardButton("ОСНОВНОЙ НЕМЕЦКИЙ")
                    markup.add(nem)
                    button5 = types.KeyboardButton("Нем.яз")
                    button6 = types.KeyboardButton("Англ.яз")
                    markup.row(button5, button6)
                    bot.send_message(message.chat.id, "Языки", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def photo(message):
    global msg
    global choosen_lesson
    if choosen_lesson in photos:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = '/Users/EI/PycharmProjects/tgdzbot/' + f"{choosen_lesson}.png"
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
        print(choosen_lesson)
    else:
        bot.send_message(message.chat.id, "пж не нада так делать")


bot.infinity_polling()
