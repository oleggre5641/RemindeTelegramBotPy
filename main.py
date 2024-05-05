import telebot
import os
import time
import threading


from func import check_date_format, check_time_format, add_reminde_database, remember, check_internet_connection

# Получаем токен из переменной окружения
API_TOKEN = os.environ.get('API_TOKEN')
print(API_TOKEN)
bot = telebot.TeleBot(token=API_TOKEN)

t1 = threading.Thread(target=remember, args=(bot,))
t1.start()


@bot.message_handler(content_types=['text'])
def rem_create(message):
    """
    Функция для создания напоминания
    :param message:
    """
    message_text = message.text
    if message_text == "/create":
        msg = bot.send_message(message.from_user.id, text="Привет! 👋\nНапишите текст вашего напоминания")
        bot.register_next_step_handler(msg, text_enter)
    elif message_text == "/watch":
        msg = bot.send_message(message.from_user.id, text="Последние напоминания")
    elif message_text == "/help":
        msg = bot.send_message(message.from_user.id, text="Команды")

def text_enter(message):
    """
    Фунция принимает текст напоминания + просит ввести дату
    :param message: Текст напоминания
    """
    reminde_text = message.text
    msg = bot.send_message(message.from_user.id, text="Далее напиши дату в таком формате:\n15.06")
    bot.register_next_step_handler(msg, date_enter, reminde_text)

def date_enter(message, reminde_text):
    """
    Функция принимает дату + проверяет её
    :param message: Дата
    """
    check_date_result = check_date_format(message.text)
    if check_date_result == True:
        date_text = message.text
        msg = bot.send_message(message.from_user.id, text="Теперь напиши время в таком формате:\n12.00")
        bot.register_next_step_handler(msg, time_enter,reminde_text, date_text)
    else:
       bot.send_message(message.from_user.id, text="Вы ввели дату неправильного формата!\nНачните сначала нажав на команду \n'/create'")


def time_enter(message, reminde_text, date_text):
    """
    Функция для получения времени напоминания + проверяет его
    :param message:
    :param reminde_text: Текст напоминания
    """
    check_time_result = check_time_format(message.text)
    if check_time_result == True:
        time_text = message.text
        result_create_reminde = add_reminde_database(message.from_user.id ,reminde_text, date_text, time_text)
        if result_create_reminde == True:
            bot.send_message(message.from_user.id, text="Напоминание успешно создано ✅")
        else:
            bot.send_message(message.from_user.id, text="Напоминание не было создано ❌")
    else:
        bot.send_message(message.from_user.id, text="Вы ввели время неправильного формата!\nНачните сначала нажав на команду \n'/create'")


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print('Ошибка доступа к API телеграмм')
        print(f"Произошло исключение: {e}")
        # Ожидание перед следующей попыткой перезапуска
        time.sleep(1)
        # Проверка доступности интернета
        if check_internet_connection():
            print("Подключение восстановленно")
            continue  # Перезапустить цикл и повторить попытку подключения