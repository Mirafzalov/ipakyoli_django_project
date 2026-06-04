import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
# django.setup()

from dotenv import load_dotenv
from telebot import TeleBot




import requests
from humanize import intcomma
from telebot.types import InlineKeyboardMarkup
from telegram import InlineKeyboardButton

# from digital_store.utils import get_url

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
# CHAT_ID = '505523351' Mine
CHAT_ID = '-5212504342' # Group

bot = TeleBot(BOT_TOKEN)
# def get_bot(text):
#     bot.send_message(CHAT_ID, text)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')


#
# def get_order(page):
#     orders = Order.objects.all().order_by('-id')
#     paginator = Paginator(orders, 3)
#     page_obj = paginator.get_page(page)
#     return page_obj

def get_order_api(page):
    response = requests.get(
        'http://127.0.0.1:8000/api/orders/history/',
        params={'page': page}
    )
    return response.json()


def get_buttons(data):
    markup = InlineKeyboardMarkup()
    row = []
    if data['has_previous']:
        row.append(
            InlineKeyboardButton('<', callback_data=f"page {data['previous_page']}")
        )

    row.append(
        InlineKeyboardButton(text=f"{data['page']}/{data['total']}", callback_data='null')
    )

    if data['has_next']:
        row.append(
            InlineKeyboardButton('>', callback_data=f"page {data['next_page']}")
        )
    markup.row(*row)
    return markup


@bot.message_handler(commands=['history'])
def send_history(message):
    data = get_order_api(1)
    markup = get_buttons(data)
    text = ''
    for order in data['orders']:
        text += f'''
Пользователь: {order['user']}

Номер телефона: {order['phone']}

Номер заказа: #{order['id']}

Цена заказа: {intcomma(order['price'])}

Заказ создан: {order['created_at']}
--------------------------------------------------------------
'''
    bot.send_message(message.chat.id,  text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def paginate_buttons(call):
    if call.data == 'null':
        return
    if call.data.split()[0] == 'page':
        page = int(call.data.split()[1])
        data = get_order_api(page)
        markup = get_buttons(data)
        text = ''
        for order in data['orders']:
            text += f'''
Пользователь: {order['user']}

Номер телефона: {order['phone']}

Номер заказа: #{order['id']}

Цена заказа: {intcomma(order['price'])}

Заказ создан: {order['created_at']}
--------------------------------------------------------------
            '''
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)


# @bot.message_handler(commands=['history'])
# def send_history(message):
#     response = requests.get(get_url())
#     orders = response.json()
#     for order in orders:
#         text = f'''
#         Пользователь: {order['user']}
#
#         Номер телефона: {order['phone']}
#
#         Номер заказа: #{order['order_id']}
#
#         Цена заказа: {intcomma(order['price'])}
#         --------------------------------------------------------------
#         Заказ создан: {order['created_at']}
#         '''
#         bot.send_message(message.chat.id, text, reply_markup=markup)

bot.polling()

