def replace_in_file(replacing, after, file):
    l = open_file(f"{file}")
    f = open(f"{file}.txt", "w")
    for i in range(0, len(l)):
        if i != l.index(after) + 1:
            f.write(l[i] + "\n")
        else:
            f.write(replacing + "\n")
    f.close()


def open_file(file):
    f = open(f"{file}.txt", "r+")
    f_ = f.readlines()
    f_a = [i[:len(i) - 1] for i in f_]
    f.close()
    return f_a


def clear_file(f):
    file = open(f"{f}", 'r+')

    m = file.readlines()
    ma = []
    file.close()
    for i in range(0, len(m)):
        if m[i] != '':
            ma.append(m[i][:len(m[i]) - 1])
        else:
            ma.append('')
    return ma


def add_to_file(text, file):
    f = open(f"{file}", "a")
    f.write(text)
    f.close()


def send_info_about_lesson(lesson):
    l = clear_file("Domashka.txt")
    l.append('')
    if l[l.index(lesson) + 1] == "-":
        if lesson in photos:
            f = open("photos/photos.txt", "r+")
            li = f.readlines()
            li = [i[:len(i) - 1] for i in li]
            f.close()
            if lesson in li:
                return "фото\n"
            else:
                return "не заполнено"
        else:
            return "не заполнено"
    else:
        return f"{l[l.index(lesson) + 1]} \n"


def ob(base, text, bot):
    for i in range(0, len(base)):
        if i % 2 == 0:
            try:
                bot.send_message(base[i], text)
            except:
                pass


def ob_photo(base, bot):
    for i in range(0, len(base)):
        if i % 2 == 0:
            try:
                photo = open(f"ob.png", "rb")
                bot.send_photo(base[i], photo)
            except:
                pass


token = '6353183402:AAGcx4MYwwHUgEm4OQvUBBWvh_dCywBkYBc'
real_key = 'key_from_using_the_bot_do_not_share_that'
security_key = "key_from_bot_7b_1488"

lessons_technik = ["algebra", "phisic", "lit_ra", "teoriya_ver", "russ_yaz", "geography", "history", "geometry", "biology", "obshestvo", "ITC", "musik", "eng_eng1", "eng_eng2", "nem_eng1", "nem_eng2", "eng_nem", "nem_nem"] #18
lessons_technik_s = ["Алгебра", "Физика", "Лит-ра", "Вероятность", "Русский язык", "География", "История", "Геометрия", "Биология", "Обществознание", "Информатика", "Музыка",
                     "Англ.яз группа 1", "Англ.яз группа 2", "Нем.яз группа 1", "Нем.яз группа 2", "Англ.яз немцы", "Нем.яз немцы"] #18

lessons = ["algebra", "phisic", "lit_ra", "teoriya_ver", "russ_yaz", "geography", "history", "geometry", "biology", "obshestvo", "ITC", "musik", "eng", "nem"]
lessons_s = ["Алгебра 🟰", "Физика 🧑‍🔬", "Лит-ра 📖", "Вероятность 🎲", "Русский язык 🖋️", "География 🌍", "История ⏳", "Геометрия 📐", "Биология 🦠", "Обществознание", "Информатика 💻", "Музыка 🎶", "Англ.яз", "Нем.яз"]

groups_s = ["Английский язык группа 1 (Храмова)", "Английский язык группа 2 (Любовь Борисовна)", "Немецкий язык"]
groups = ["eng1", "eng2", "nem"]

photos = ["algebra", "phisic", "teoriya_ver", "russ_yaz", "geography", "geometry", "nem_nem", "eng_nem", "lit_ra", "eng_eng1", "eng_eng2", "nem_eng1", "nem_eng2"]

rasp = "Понедельник:\n" \
       "Ин.яз. 1\n" \
       "Разговоры о важном\n" \
       "Ин.яз. 1\n" \
       "Алгебра\n" \
       "Физика\n" \
       "Технология\n" \
       "Физ-ра\n\n" \
       "Вторник:\n" \
       "Ин.яз. 1\n" \
       "Лит-ра\n" \
       "Теория вероятности\n" \
       "Русский язык\n" \
       "Алгебра\n" \
       "Ин.яз. 2\n" \
       "Физика\n\n" \
       "Среда:\n" \
       "География\n" \
       "Технология\n" \
       "ИЗО\n" \
       "Русский язык\n" \
       "Ин.яз 2\n" \
       "История\n\n" \
       "Четверг:\n" \
       "Алгебра\n" \
       "Геометрия\n" \
       "Биология\n" \
       "Общество\n" \
       "Физ-ра\n" \
       "Ин.яз. 1\n" \
       "Проф. ориент.\n\n" \
       "Пятница:\n" \
       "Лит-ра\n" \
       "Русский язык\n" \
       "История\n" \
       "Информатика\n" \
       "Ин.яз. 1\n\n" \
       "Суббота:\n" \
       "Русский язык\n" \
       "Геометрия\n" \
       "Музыка\n" \
       "Алгебра\n" \
       "География"
