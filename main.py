from info.req import get_info, site_status, get_rating, getAvatar, chat_new_notif, get_start_info, get_tc_status
import telebot
import os
import schedule
import threading, time
try:
    with open("blacklist.cfg", 'r', encoding='utf-8') as f:
        blacklist = f.readline().split(" ")
except FileNotFoundError as e:
    with open("blacklist.cfg", 'w', encoding="utf-8") as f:
        f.write("Записывать на первой строке через пробел все ненеужные заказы, Пример ##MCMK8JGA #MCMK8JGA #MCMK8JGA")
tk, chat_id, _ = get_start_info()
mess_check = set()
tc_order_check = set()
os.system("cls")
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
    mess, results = chat_new_notif()
    res_list = get_tc_status()
    edit_chat = ''.join([x for x in chat if x.isdigit()])
    edit_trades = ''.join([x for x in trade if x.isdigit()])
    edit_balance = ''.join([x for x in balance if x.isdigit()])
    edit_orders = ''.join([x for x in orders if x.isdigit()])
    try:
        if edit_balance == "":
            edit_balance = 0
        else:
            pass
    except:
        pass
    return edit_chat, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count, valuta, avatar, mess, results, res_list
@bot.message_handler(commands=['status'])
def check_status(message):
    status = site_status()
    bot.send_message(message.chat.id, status)
@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id, start_message)
@bot.message_handler(commands=['info'])
def info_cm(message):
    _, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count, valuta, avatar, mess, _, _ = fetch_info()
    bot.send_message(message.chat.id, f"Имя пользователя: {name}\nСсылка на профиль: {href}\nАватар: {avatar}\nПродажи: {edit_trades}\nСообщения: {mess}\nЯзык: {lang}\nФинансы: {edit_balance} - Валюта {valuta}\nПокупки: {edit_orders}\nРейтинг: {rating}\nДата регистрации: \n{reg_date}\nКоличество отзывов: {rating_full_count}\n")
#Проверка на новые сообщения
def newMes():
    global mess_check
    global tc_order_check
    global blacklist
    *_, mess, res, res_list = fetch_info()
    for user_name,message,time, data_node_msg in res:
        if data_node_msg not in mess_check:
            try:
                bot.send_message(chat_id=chat_id, text=f"У вас новое сообщение!\nUsername: {user_name}\nMessage: {message}\nTime: {time}")
                mess_check.add(data_node_msg)
            except Exception as e:
                print(e)
    for href, tc_date_time, tc_order, tc_user, tc_status in res_list:
        if tc_order not in tc_order_check and tc_order not in blacklist:
            try:
                bot.send_message(chat_id=chat_id, text=f"У вас новый заказ!\nСсылка: {href}\nНомер заказа: {tc_order}\nВремя: {tc_date_time}\nПользователь: {tc_user}\nСтатус: {tc_status}")
                tc_order_check.add(tc_order)
            except Exception as e:
                print(e)
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
schedule.every(20).seconds.do(newMes)
print("Бот запущен!")
# Бесконечный цикл для выполнения планировщика
while True:
    schedule.run_pending()
    time.sleep(1)  # Ждем 1 секунду между проверками планировщика
