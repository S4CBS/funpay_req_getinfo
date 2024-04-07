from info.req import get_info, site_status, get_rating
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
/info - Полная информация
..."""

def fetch_info():
    try:
        chat, trade, name, lang, balance, orders, href = get_info("ru")
    except:
        try:
            chat, trade, name, lang, balance, orders, href = get_info("en")
        except:
            chat, trade, name, lang, balance, orders, href = get_info("uk")

    rating, reg_date, rating_full_count = get_rating()

    edit_chat = ''.join([x for x in chat if x.isdigit()])
    edit_trades = ''.join([x for x in trade if x.isdigit()])
    edit_balance = ''.join([x for x in balance if x.isdigit()])
    edit_orders = ''.join([x for x in orders if x.isdigit()])

    return edit_chat, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count

@bot.message_handler(commands=['status'])
def check_status(message):
    status = site_status()
    bot.send_message(message.chat.id, status)

@bot.message_handler(commands=['start'])
def start_cm(message):
    bot.send_message(message.chat.id, start_message)

@bot.message_handler(commands=['info'])
def info_cm(message):
    edit_chat, edit_trades, name, lang, edit_balance, edit_orders, href, rating, reg_date, rating_full_count = fetch_info()
    bot.send_message(message.chat.id, f"Имя пользователя: {name}\nСсылка на профиль: {href}\nПродажи: {edit_trades}\nСообщения: {edit_chat}\nЯзык: {lang}\nФинансы: {edit_balance}\nПокупки: {edit_orders}\nРейтинг: {rating}\nДата регистрации: \n{reg_date}\nКоличество отзывов: {rating_full_count}")

bot.polling(True)



    
