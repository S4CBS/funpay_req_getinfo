import requests
from bs4 import BeautifulSoup
import re

def site_status():
    try:
        with open("config.cfg", 'r') as file:
            golden_key = file.read()
            golden_key = golden_key.replace("golden_key=", '')
    except FileNotFoundError:
        pass

    url = "https://funpay.com/orders/trade"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }

    response = requests.get(url, headers=headers)

    return response.status_code

def get_info(language):
    try:
        with open("config.cfg", 'r') as file:
            golden_key = file.read()
            golden_key = golden_key.replace("golden_key=", '')
    except FileNotFoundError:
        golden_key = input("Введите ваш golden_key: ")
        with open("config.cfg", 'w') as file:
            file.write("golden_key="+golden_key)
            file.close()
        
    if language != 'ru':
        url = f"https://funpay.com/{language}/orders/trade" if language else "https://funpay.com/orders/trade"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
            "Cookie": f"golden_key={golden_key}"
        }
    else:
        url = "https://funpay.com/orders/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
            "Cookie": f"golden_key={golden_key}"
        }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        menu_item_chat = soup.find("a", class_="menu-item-chat")
        menu_item_trade = soup.find("a", class_="menu-item-trade")
        user_link_name = soup.find("div", class_="user-link-name")
        menu_item_langs = soup.find("a", class_="menu-item-langs")
        menu_item_balance = soup.find("a", class_="menu-item-balance")
        menu_item_orders = soup.find("a", class_="menu-item-orders")
        # Достаем ссылку на профиль
        user_link_dropdown = soup.find("a", class_="user-link-dropdown", href=True)
        href = user_link_dropdown["href"]

        if menu_item_chat:
            chat = menu_item_chat.text.strip()

        if menu_item_trade:
            trade = menu_item_trade.text.strip()
        
        if user_link_name:
            name = user_link_name.text.strip()
        
        if menu_item_langs:
            lang = menu_item_langs.text.strip()
        
        if menu_item_balance:
            balance = menu_item_balance.text.strip()
        
        if menu_item_orders:
            orders = menu_item_orders.text.strip()
    
    return chat, trade, name, lang, balance, orders, href

def get_href_url():
    try:
        href_url = get_info("ru")
        href_url = [x for x in href_url if "https" in x]
    except:
        try:
            href_url = get_info("en")
            href_url = [x for x in href_url if "https" in x]
        except:
            href_url = get_info("uk")
            href_url = [x for x in href_url if "https" in x]
    
    return href_url[0]

def get_rating(href=get_href_url()):
    try:
        with open("config.cfg", 'r') as file:
            golden_key = file.read()
            golden_key = golden_key.replace("golden_key=", '')
    except FileNotFoundError:
        golden_key = input("Введите ваш golden_key: ")
        with open("config.cfg", 'w') as file:
            file.write("golden_key="+golden_key)
            file.close()

    url = href
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        big = soup.find("span", class_="big")
        text_nowrap = soup.find("div", class_="text-nowrap")
        rating_full_count = soup.find("div", class_="rating-full-count")
        # tc_item = soup.find("div", class_="tc-desc-text") Предметы на продаже
    
        if big:
            rating = big.text.strip()

        if text_nowrap:
            reg_date = text_nowrap.text.strip().replace("  ", "")

        if rating_full_count:
            rating_full_count = rating_full_count.text.split()
            rating_full_count = [x for x in rating_full_count if x.isdigit()][0]
        
    return rating, reg_date, rating_full_count