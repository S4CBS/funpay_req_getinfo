import os
from info.req import get_info, site_status, get_rating, getAvatar, chat_new_notif, get_start_info, get_tc_status
import telebot
import schedule
import threading, time
from FunPayAPI import Account
from io import BytesIO
import requests
from PIL import Image
#import sys
#homepath = sys.argv[0].replace(os.path.basename(sys.argv[0]),"")
def seen_try():
    try:
        with open("seen.cfg", 'r', encoding="utf-8") as f:
            temp_seen = f.readlines()
            seen = {x.replace("\n", "") for x in temp_seen}
    except FileNotFoundError:
        seen = {}
    return seen
st_start = "Уведомления о заказах=True\nУведомление о новых сообщениях=True"
try:
    with open("settings.cfg", 'r', encoding='utf-8') as f:
        settings_list = f.readlines()
        try:
            order_message = settings_list[1].split("=")[1].split("\n")[0]
            order_message = bool(order_message)
        except:
            pass
        try:
            new_messages = settings_list[2].split("=")[1].split("\n")[0]
            new_messages = bool(new_messages)
        except:
            pass
except FileNotFoundError as e:
    with open("settings.cfg", 'w', encoding="utf-8") as f:
        f.write(st_start)
tk, chat_id, golden_key = get_start_info()
mess_check = set()
tc_order_check = set()
bot = telebot.TeleBot(token=tk)
start_message = """Доступные команды:
/status - Статус сайта
/info - Полная информация
/send_message [chat_id] сообщение
/send_image [chat_id] - нажимаем enter, загружаем картинку.
/seen [Номер заказа](Пример: /seen #FMZXXXXX) - добавляет заказ в базу прочитаных сообщений.
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
@bot.message_handler(commands=['send_message'])
def send_message_cm(message):
    command = message.text.split()
    if len(command) < 3:
        bot.send_message(message.chat.id, "Неправильный формат команды. Используйте /send_message [chat_id] сообщение")
    user_id = command[1]
    text = ' '.join(command[2:])
    try:
        acc = Account(golden_key).get()
        acc.send_message(chat_id=user_id, text=text)
    except:
        pass
@bot.message_handler(commands=['send_image'])
def send_image_cm(message):
    command_parts = message.text.split()
    if len(command_parts) < 2:
        bot.reply_to(message, "Укажите chat_id для отправки изображения.")
        return
    chat_id_img = command_parts[1]
    bot.send_message(message.chat.id, "Загрузите картинку.")
    @bot.message_handler(content_types=['photo'])
    def handle_received_photo(message):
        largest_photo = message.photo[-1]
        file_id = largest_photo.file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{tk}/{file_info.file_path}"
        response = requests.get(file_url)
        if response.status_code == 200:
            image_data = Image.open(BytesIO(response.content))
            image_byte_array = BytesIO()
            image_data.save(image_byte_array, format='JPEG')
            image_byte_array.seek(0)
            try:
                acc = Account(golden_key=golden_key).get()
                acc.send_image(chat_id=chat_id_img, image=image_byte_array)
                bot.send_message(message.chat.id, "Изображение успешно отправлено.")
            except Exception as e:
                bot.send_message(message.chat.id, f"Ошибка при отправке изображения: {e}")
        else:
            bot.send_message(message.chat.id, "Ошибка при загрузке изображения.")
@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id, start_message)
@bot.message_handler(commands=['info'])
def info_cm(message):
    _, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count, valuta, avatar, mess, _, _ = fetch_info()
    bot.send_message(message.chat.id, f"Имя пользователя: {name}\nСсылка на профиль: {href}\nАватар: {avatar}\nПродажи: {edit_trades}\nСообщения: {mess}\nЯзык: {lang}\nФинансы: {edit_balance} - Валюта {valuta}\nПокупки: {edit_orders}\nРейтинг: {rating}\nДата регистрации: \n{reg_date}\nКоличество отзывов: {rating_full_count}\n")
@bot.message_handler(commands=['seen'])
def seen_order_cm(message):
    command = message.text.split()
    if len(command) < 2:
        print("Неверный формат команды. Используйте /seen [Номер заказа]")
    sn_order = command[1]
    sn_check = seen_try()
    with open("seen.cfg", "a", encoding="utf-8") as f:
        if sn_order not in sn_check:
            f.write(sn_order+"\n")
    if sn_order not in sn_check:
        bot.send_message(message.chat.id, text=f"Теперь номер заказа {sn_order} в списке прочитанных.")
    else:
        bot.send_message(message.chat.id, text=f"Номер заказа {sn_order} уже в списке прочитанных.")
    seen_try()
#Проверка на новые сообщения и продажи
def newMes():
    global mess_check
    global tc_order_check
    global new_messages
    global order_message
    seen = seen_try()
    *_, res, res_list = fetch_info()
    for user_name,message,time, data_node_msg, id_chat in res:
        if data_node_msg not in mess_check:
            try:
                if new_messages is True:
                    bot.send_message(chat_id=chat_id, text=f"У вас новое сообщение!\nUsername: {user_name}\nMessage: {message}\nTime: {time}\nChat_id: {id_chat}")
                    mess_check.add(data_node_msg)
                elif new_messages is False:
                    pass
            except Exception as e:
                print(e)
    for href, tc_date_time, tc_order, tc_user, tc_status, id_chat_ord in res_list:
        if tc_order not in tc_order_check and tc_order not in seen:
            try:
                if order_message is True:
                    bot.send_message(chat_id=chat_id, text=f"У вас новый заказ!\nСсылка: {href}\nНомер заказа: {tc_order}\nВремя: {tc_date_time}\nПользователь: {tc_user}\nСтатус: {tc_status}\nChat_id: {id_chat_ord}")
                    tc_order_check.add(tc_order)
                elif order_message is False:
                    pass
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
