from info.req import get_info, site_status
import telebot

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
/messages - Сообщения {количество}
/trades - Продажи {количество}
/info - Полная информация
..."""

def fetch_info():
    try:
        chat, trade, name, lang = get_info("ru")
    except:
        try:
            chat, trade, name, lang = get_info("en")
        except:
            chat, trade, name, lang = get_info("uk")

    edit_chat = ''.join([x for x in chat if x.isdigit()])
    edit_trades = ''.join([x for x in trade if x.isdigit()])

    return edit_chat, edit_trades, name, lang

@bot.message_handler(commands=['status'])
def check_status(message):
    status = site_status()
    bot.send_message(message.chat.id, status)

@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id, start_message)

@bot.message_handler(commands=['messages'])
def messages_cm(message):
    edit_chat, _, _, _ = fetch_info()
    bot.send_message(message.chat.id, f"Сообщения: {edit_chat}")

@bot.message_handler(commands=['trades'])
def trades_cm(message):
    _, edit_trades, _, _ = fetch_info()
    bot.send_message(message.chat.id, f"Продажи: {edit_trades}")

@bot.message_handler(commands=['info'])
def info_cm(message):
    edit_chat, edit_trades, name, lang = fetch_info()
    bot.send_message(message.chat.id, f"Имя пользователя: {name}\nПродажи: {edit_trades}\nСообщения: {edit_chat}\nЯзык: {lang}")

bot.polling(True)



    
