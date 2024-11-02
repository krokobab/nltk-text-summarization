# Импортируем библиотеку для создания телеграм-бота, модуль суммаризации, файл settings.py, содержащий api-ключ бота
import telebot
from telebot import types
import summarization

# Подключаем токен бота, объявляем переменные для хранения данных, передаваемых в функцию суммаризации
bot = telebot.TeleBot("ВАШ API-КЛЮЧ")
compression_parameter = .0
text = ""


# Объявляем слушателя текстовых сообщений и метод их обработки
@bot.message_handler(content_types=['text'])
def start_bot(message):
    # В случае отправки пользователем комманды /start бот отправит приветственное сообщение
    if message.text == "/start":
        bot.send_message(message.chat.id, "Привет! Я бот-суммаризатор! Отправь текст и выбери степень сжатия, "
                                          "чтобы получить сокращённый текст. Для начала отправь текст.")
        bot.register_next_step_handler(message, get_text)
    # Иначе, попросит пользователя отправить эту комманду
    else:
        bot.send_message(message.chat.id, "Напиши /start.")


# Объявляем метод получения текста, который требуется суммаризировать
def get_text(message):
    # Получаем текст из сообщения и записываем в глобальную переменную
    global text
    text = message.text
    # Создаём кнопки для более удобного выбора степени сжатия
    keyboard = types.InlineKeyboardMarkup()
    key_strongly = types.InlineKeyboardButton(text='Сильно', callback_data='strongly')
    keyboard.add(key_strongly)
    key_weakly = types.InlineKeyboardButton(text='Слабо', callback_data='weakly')
    keyboard.add(key_weakly)
    # Отправляем сообщение с запросом на выбор степени сжатия и созданными ранее кнопками
    bot.send_message(message.chat.id, text="Отлично! Как сжать текст: сильно или слабо?", reply_markup=keyboard)


# Объявляем метод для обработки нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global compression_parameter, text
    # В зависимости от выбранной степени сжатия, присваиваем соответствующее значение параметра сжатия
    if call.data == 'strongly':
        compression_parameter = 2
    else:
        compression_parameter = 1.1
    # Отправляем сообщение с готовым резюме, обращаясь к модулю суммаризации
    bot.send_message(call.message.chat.id, text=summarization.summarize(text, compression_parameter))


# Бот непрерывно слушает сообщения
bot.polling(none_stop=True, interval=0)
