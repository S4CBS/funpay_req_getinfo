from info.req import get_info, site_status, get_rating, getAvatar
import telebot
import os
import schedule
import threading, time
counter = 0
os.system("cls")
try:
    with open("config_tg.cfg", 'r') as file:
        tk = file.read()
        tk = tk.replace("token=", '')
except FileNotFoundError:
    tk = input("Введите ваш токен телеграм бота: ")
    with open("config_tg.cfg", 'w') as file:
        file.write("token="+tk)
        file.close()
bot = telebot.TeleBot(token=tk)
start_message = """Доступные команды:
/status - Статус сайта
/info - Полная информация
..."""
def fetch_info():
    try:
        chat, trade, name, lang, balance, orders, href, valuta = get_info("ru")
    except:
        try:
            chat, trade, name, lang, balance, orders, href, valuta = get_info("en")
        except:
            chat, trade, name, lang, balance, orders, href, valuta = get_info("uk")
    rating, reg_date, rating_full_count = get_rating()
    avatar = getAvatar()
    edit_chat = ''.join([x for x in chat if x.isdigit()])
    edit_trades = ''.join([x for x in trade if x.isdigit()])
    edit_balance = ''.join([x for x in balance if x.isdigit()])
    edit_orders = ''.join([x for x in orders if x.isdigit()])
    return edit_chat, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count, valuta, avatar
@bot.message_handler(commands=['status'])
def check_status(message):
    status = site_status()
    bot.send_message(message.chat.id, status)
@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id, start_message)
@bot.message_handler(commands=['info'])
def info_cm(message):
    edit_chat, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count, valuta, avatar = fetch_info()
    bot.send_message(message.chat.id, f"Имя пользователя: {name}\nСсылка на профиль: {href}\nАватар: {avatar}\nПродажи: {edit_trades}\nСообщения: {edit_chat}\nЯзык: {lang}\nФинансы: {edit_balance} - Валюта {valuta}\nПокупки: {edit_orders}\nРейтинг: {rating}\nДата регистрации: \n{reg_date}\nКоличество отзывов: {rating_full_count}\n")
#Проверка на новые сообщения
def newMes():
    global counter
    edit_chat, *_ = fetch_info()
    edit_chat = int(edit_chat)

    if edit_chat > counter: # 1 0
        bot.send_message(chat_id="YOUR CHATID", text="У вас новое сообщение!")
        counter = edit_chat # 1 1
    else:
        counter = edit_chat
    

def polling_thread():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка в работе бота: {e}")
            time.sleep(10)
# Запуск бота в отдельном потоке
bot_thread = threading.Thread(target=polling_thread)
bot_thread.daemon = True
bot_thread.start()
# Запуск планировщика для выполнения функции newMes каждую минуту
schedule.every(15).seconds.do(newMes)
print("Бот запущен!")
# Бесконечный цикл для выполнения планировщика
while True:
    schedule.run_pending()
    time.sleep(1)  # Ждем 1 секунду между проверками планировщика
