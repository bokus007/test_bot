import telebot
from decouple import config
import time

bot = telebot.TeleBot(config('bot_token'))

wait_type = 0   # тип состояния ожидания
                # 1-сумма для пересчета валюты


def send_kb_main(message, txt="Выберите что-нибудь ⬇"):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Меню 2")
    item2 = telebot.types.KeyboardButton("Пересчет валюты")
    item3 = telebot.types.KeyboardButton("Дата и время ?")
    kb.add(item1, item2, item3)
    bot.send_message(message.chat.id, txt, reply_markup=kb)


def send_kb1(message, txt="Выберите что-нибудь ⬇"):
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("кнопка4")
    item2 = telebot.types.KeyboardButton("кнопка5")
    item3 = telebot.types.KeyboardButton("кнопка6")
    kb.add(item1, item2, item3)
    bot.send_message(message.chat.id, txt, reply_markup=kb)


def send_inline_kb_valuta1(message):
    kb = telebot.types.InlineKeyboardMarkup(row_width=5)
    item1 = telebot.types.InlineKeyboardButton("BYN", callback_data='1-1')
    item2 = telebot.types.InlineKeyboardButton("USD", callback_data='1-2')
    item3 = telebot.types.InlineKeyboardButton("EURO", callback_data='1-3')
    item4 = telebot.types.InlineKeyboardButton("RUB", callback_data='1-4')
    item5 = telebot.types.InlineKeyboardButton("PLN", callback_data='1-5')
    item6 = telebot.types.InlineKeyboardButton("ОТМЕНА", callback_data='1-6')
    kb.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, 'Выбери валюту из....', reply_markup=kb)


def send_inline_kb_valuta2(message):
    kb = telebot.types.InlineKeyboardMarkup(row_width=5)
    item1 = telebot.types.InlineKeyboardButton("BYN", callback_data='2-1')
    item2 = telebot.types.InlineKeyboardButton("USD", callback_data='2-2')
    item3 = telebot.types.InlineKeyboardButton("EURO", callback_data='2-3')
    item4 = telebot.types.InlineKeyboardButton("RUB", callback_data='2-4')
    item5 = telebot.types.InlineKeyboardButton("PLN", callback_data='2-5')
    item6 = telebot.types.InlineKeyboardButton("ОТМЕНА", callback_data='2-6')
    kb.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(message.chat.id, 'Выбери валюту в ....', reply_markup=kb)


@bot.message_handler(commands=['start'])
def welcom_user(message):
    bot.send_message(message.chat.id, f"Хелоооооу {message.from_user.first_name} !!!")
    send_kb_main(message)


@bot.message_handler(commands=['погода'])
def welcom_user(message):
    bot.send_message(message.chat.id, "брр...")


@bot.message_handler(content_types=['text'])
def some_text(message):
    global wait_type
    text = message.text.lower()

    # сначала проверяем тип ожидания
    # если тип ожидания равен 1 - значит бот запросил сумму и ждет только цифры
    if wait_type == 1:
        try:
            val_summa = float(text.replace(",", "."))  # если пользователь прислал не цифры тут будет ошибка
            bot.send_message(message.chat.id, f"пересчет из {val1} в {val2} - {val_summa * 2}")
            wait_type = 0  # обнуляем состояние ожидания и выходим из функции
            return
        except:

            bot.send_message(message.chat.id, "не корректная сумма")
            return

    if text in ['привет', 'hi', 'hello']:
        bot.send_message(message.chat.id, "и тебе привет))")
    elif text == "меню 2":
        send_kb1(message)  # отправляем пользователю клавиатуру номер2
    elif text == "пересчет валюты":
        send_inline_kb_valuta1(message)  # отправляем инлайн-клавиатуру для выбора валюты
    elif text == "дата и время ?":
        bot.send_message(message.chat.id, time.strftime('%d.%m.%Y - %H:%M:%S'))
    elif text in ['кнопка4', 'кнопка5', 'кнопка6']:
        bot.send_message(message.chat.id, f"нажата {text}")
        send_kb_main(message)
    else:
        bot.send_message(message.chat.id, 'вот так могу - ' + text[::-1])
        send_kb_main(message)


@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    bot.send_message(message.chat.id, 'красивый стикер👍')


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    # эта функция ловит и обрабатывает колбэки от кнопок инлайн-клавиатур

    global val1
    global val2
    global wait_type
    try:
        if call.message:
            text = call.data
            if text == '1-1':  # Если нажата кнопка 1 на клавиатуре 1
                # редактируем прежнее сообщение и удаляем из него клавиатуру
                bot.edit_message_text("Вы выбрали из ... бел рубли", call.message.chat.id, call.message.message_id,
                                      reply_markup=None)
                val1 = 'byn'
                send_inline_kb_valuta2(call.message)
            elif text == '2-1':  # Если нажата кнопка 1 на клавиатуре 2
                # редактируем прежнее сообщение и удаляем из него клавиатуру
                bot.edit_message_text("Вы выбрали в ... бел рубли", call.message.chat.id, call.message.message_id,
                                      reply_markup=None)
                val2 = 'byn'
                wait_type = 1  # включаем режим ожидания и ждем сумму
                bot.send_message(call.message.chat.id, "сумма?")

            else:
                bot.edit_message_text("Вы выбрали - " + text, call.message.chat.id, call.message.message_id,
                                      reply_markup=None)
    except:
        pass


while True:
    try:
        print("Бот запущен -> " + time.strftime('%H:%M:%S'))
        bot.polling(none_stop=True, skip_pending=True)
        # skip_pending = True  - не отвечать на старые сообщения которые прислали пока бот не работал
    except:
        print("Возникли ошибки. Перезапуск через 2 сек....")
        time.sleep(2)
