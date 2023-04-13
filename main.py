# Импортируем необходимые библиотеки
import telebot # для работы с Telegram API
import random # для генерации случайных чисел

# Создаем объект бота с помощью токена, полученного от @BotFather
bot = telebot.TeleBot("6248475136:AAHhK0K_Bz-o7Pr3hXG0Tm9JKd2ukwK6_Ws")

# Создаем словарь, где ключ - id пользователя, а значение - список из пола и интересов
users = {}

# Создаем функцию для проверки, подходит ли пользователь по полу и интересам
def check_match(user1, user2):
    # Если пол одинаковый и есть общие интересы, то возвращаем True
    if user1[0] == user2[0] and len(set(user1[1]) & set(user2[1])) > 0:
        return True
    # Иначе возвращаем False
    else:
        return False

# Создаем функцию для поиска случайного собеседника из словаря users
def find_random_chat(user_id):
    # Если словарь пустой или состоит из одного пользователя, то возвращаем None
    if len(users) < 2:
        return None
    # Иначе создаем список из всех id пользователей, кроме текущего
    else:
        ids = list(users.keys())
        ids.remove(user_id)
        # Пока список не пустой, выбираем случайный id из списка
        while ids:
            random_id = random.choice(ids)
            # Если пользователь подходит по полу и интересам, то возвращаем его id
            if check_match(users[user_id], users[random_id]):
                return random_id
            # Иначе удаляем его из списка и продолжаем поиск
            else:
                ids.remove(random_id)
        # Если список пустой, то возвращаем None
        return None

# Создаем функцию для обработки команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    # Отправляем приветственное сообщение и предлагаем ввести пол и интересы через запятую
    bot.send_message(message.chat.id, "Привет! Я чат-бот для знакомств. Давай познакомимся. Какой у тебя пол? М или Ж? И что тебе интересно? Введи свой пол и интересы через запятую. Например: М, спорт, кино, музыка.")
    # Добавляем пользователя в словарь users с пустым списком из пола и интересов
    users[message.chat.id] = []

# Создаем функцию для обработки текстовых сообщений
@bot.message_handler(content_types=['text'])
def text_message(message):
    # Если пользователь ввел пол и интересы через запятую
    if "," in message.text:
        # Разбиваем текст на список по запятой и удаляем пробелы
        data = message.text.split(",")
        data = [x.strip() for x in data]
        # Если первый элемент списка - М или Ж, то сохраняем его как пол пользователя
        if data[0] in ["М", "Ж"]:
            users[message.chat.id].append(data[0])
            # Если в списке есть еще элементы, то сохраняем их как интересы пользователя
            if len(data) > 1:
                users[message.chat.id][1] = data[1:]
            # Отправляем сообщение о том, что данные сохранены и предлагаем найти собеседника
            bot.send_message(message.chat.id, "Спасибо! Я сохранил твои данные. Хочешь найти собеседника? Напиши /chat.")
        # Иначе отправляем сообщение о неверном формате данных и просим повторить ввод
        else:
            bot.send_message(message.chat.id, "Извини, я не понял твой пол. Пожалуйста, введи М или Ж.")
    # Иначе если пользователь ввел команду /chat
    elif message.text == "/chat":
        # Ищем случайного собеседника из словаря users
        chat_id = find_random_chat(message.chat.id)
        # Если нашли, то отправляем сообщение о том, что собеседник найден и пересылаем его сообщение
        if chat_id:
            bot.send_message(message.chat.id, "Ура! Я нашел тебе собеседника. Вот его сообщение:")
            bot.forward_message(message.chat.id, chat_id, message.message_id)
        # Иначе отправляем сообщение о том, что собеседник не найден и предлагаем попробовать позже
        else:
            bot.send_message(message.chat.id, "К сожалению, я не нашел тебе собеседника. Попробуй позже.")
    # Иначе если пользователь ввел команду /stop
    elif message.text == "/stop":
        # Удаляем пользователя из словаря users
        if message.chat.id in users:
            users.pop(message.chat.id)
        users.pop(message.chat.id)
        # Отправляем сообщение о том, что чат завершен и предлагаем начать заново
        bot.send_message(message.chat.id, "Чат завершен. Если хочешь начать заново, напиши /start.")
    # Иначе если пользователь ввел любой другой текст
    else:
        # Отправляем сообщение о том, что я не понимаю такие сообщения и просим ввести пол и интересы или команду /chat или /stop
        bot.send_message(message.chat.id, "Извини, я не понимаю такие сообщения. Пожалуйста, введи свой пол и интересы через запятую или напиши /chat или /stop.")

# Запускаем бота
bot.polling(none_stop=True)
