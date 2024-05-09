import requests
from bs4 import BeautifulSoup
import re
import os
def get_start_info():
    try:
        with open("config.cfg", "r", encoding="utf-8") as f:
            temp = f.readlines()
            try:
                temp_1=temp[0].split("=")
                tk = temp_1[1].replace("\n", "")
            except:
                pass
            try:
                temp_2 = temp[1].split("=")
                chat_id = temp_2[1].replace("\n", "")
            except:
                pass
            try:
                temp_3 = temp[2].split("=")
                golden_key = temp_3[1].replace("\n", "")
            except:
                pass
    except FileNotFoundError as e:
        tk = input("Введите ваш токен телеграм бота: ")
        chat_id = input("Введите ваш chat_id телеграмм: ")
        golden_key = input("Введите ваш golden_key с сайта funpay.com: ")
        with open("config.cfg", "w", encoding="utf-8") as f:
            f.write(f"""token={tk}\nchat_id={chat_id}\ngolden_key={golden_key}""")
    os.system("cls")
    return tk, chat_id, golden_key
*_, golden_key = get_start_info()
def site_status():
    url = "https://funpay.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }
    response = requests.get(url, headers=headers)
    return response.status_code
def get_info(language):
    if language != 'ru':
        url = f"https://funpay.com/{language}/orders/trade" if language else "https://funpay.com/orders/trade"
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
        # Валюта
        menu_item_currencies = soup.find("a", class_="menu-item-currencies")
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
        if menu_item_currencies:
            valuta = menu_item_currencies.text.strip()
    return chat, trade, name, lang, balance, orders, href, valuta
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
        rating_full_count = soup.find("div", class_="mb5")
        if big:
            rating = big.text.strip()
        if text_nowrap:
            reg_date = text_nowrap.text.strip().replace("  ", "")
        if rating_full_count:
            rating_full_count = rating_full_count.text.split()
            rating_full_count = [x for x in rating_full_count if x.isdigit()][0]
    return rating, reg_date, rating_full_count
def getAvatar(href=get_href_url()):
    url = href
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        avatar_photo = soup.find("div", class_="avatar-photo")
        if avatar_photo:
            # Получаем значение атрибута style
            style = avatar_photo.get("style")
            if style:
                # Используем регулярное выражение для извлечения URL из атрибута style
                pattern = r"url\((.*?)\)"
                matches = re.search(pattern, style)
                if matches:
                    # Извлекаем ссылку из найденного совпадения
                    avatar_url = matches.group(1)
    return avatar_url
def chat_url(language):
    if language == "ru":
        url = "https://funpay.com/chat/"
    elif language == "en":
        url = "https://funpay.com/en/chat/"
    elif language == "uk":
        url = "https://funpay.com/uk/chat/"
    return url
def chat_new_notif():
    results = []
    try:
        url = chat_url("ru")
    except:
        try:
            url = chat_url("en")
        except:
            url = chat_url("uk")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        unread = soup.find_all("a", class_="unread")
        for item in unread:
            user_name_elem = item.find(class_="media-user-name")
            message_elem = item.find(class_="contact-item-message")
            time_elem = item.find(class_="contact-item-time")
            data_node_msg = item.get("data-node-msg")
            data_id = item.get("data-id")
            if user_name_elem and message_elem and time_elem:
                user_name = user_name_elem.get_text(strip=True)
                message = message_elem.get_text(strip=True)
                time = time_elem.get_text(strip=True)
                results.append((user_name,message,time, data_node_msg, data_id))
        if unread != []:
            return len(unread), results
        else:
            return 0, results
def tc_url(language):
    if language == "ru":
        url = "https://funpay.com/orders/trade?id=&buyer=&state=paid&game="
    elif language == "en":
        url = "https://funpay.com/en/orders/trade?id=&buyer=&state=paid&game="
    elif language == "uk":
        url = "https://funpay.com/uk/orders/trade?id=&buyer=&state=paid&game="
    return url
def get_tc_status():
    try:
        url = tc_url("ru")
    except:
        try:
            url = tc_url("en")
        except:
            url = tc_url('uk')
    res_list = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
        "Cookie": f"golden_key={golden_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        tc_item = soup.find_all("a", class_="tc-item")
        for item in tc_item:
            href = item['href']
            tc_date_time = item.find(class_="tc-date-time").text.strip()
            tc_order = item.find(class_="tc-order").text.strip()
            tc_user = item.find(class_="tc-user").text.strip().replace("\n\n", " ")
            tc_status = item.find(class_="tc-status").text.strip()
            try:
                order_response = requests.get(href, headers=headers)
                if order_response.status_code == 200:
                    order_soup = BeautifulSoup(order_response.content, "html.parser")
                    chat_msg_text = order_soup.find_all("div",class_="chat-msg-text")
                    chat_div = order_soup.find("div", class_="chat")
                    try:
                        for x in chat_msg_text:
                            if "оплатил заказ" in x.text:
                                last_order_count = x
                    except:
                        pass
                    if chat_msg_text:
                        ssoup = BeautifulSoup(str(last_order_count), "html.parser")
                        div_element = ssoup.find('div', class_='chat-msg-text')
                        if div_element:
                            text_content = div_element.get_text().strip()
                            parts = text_content.split(',')
                            quantity_part = None
                            for part in parts:
                                if 'шт.' in part:
                                    quantity_part = part.strip().split(".")[0]
                                    break
                                if quantity_part is None or "":
                                    quantity_part = "1"
                    if chat_div:
                        chat_id = chat_div['data-id']
                    else:
                        chat_id = None
            except Exception as e:
                print(f"Ошибка при получении chat_id для заказа {tc_order}: {e}")
                chat_id = None
            if href and tc_date_time and tc_order and tc_user and tc_status and quantity_part:
                res_list.append((href, tc_date_time, tc_order, tc_user, tc_status, chat_id, quantity_part))
    return res_list