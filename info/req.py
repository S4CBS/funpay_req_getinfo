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

        if menu_item_chat:
            chat = menu_item_chat.text.strip()

        if menu_item_trade:
            trade = menu_item_trade.text.strip()
        
        if user_link_name:
            name = user_link_name.text.strip()
        
        if menu_item_langs:
            lang = menu_item_langs.text.strip()
    
    return chat, trade, name, lang