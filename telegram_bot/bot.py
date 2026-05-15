import os
import django
import requests
from humanize import intcomma

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()


# from digital_store.utils import get_order_history


from dotenv import load_dotenv
from telebot import TeleBot




load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')
# CHAT_ID = '505523351' Mine
CHAT_ID = '-5212504342' # Group

bot = TeleBot(BOT_TOKEN)
def get_bot(text):
    bot.send_message(CHAT_ID, text)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет')


# @bot.message_handler(commands=['history'])
# def send_history(message):
#     text = get_order_history()
#     for t in text:
#         bot.send_message(message.chat.id, t)


@bot.message_handler(commands=['history'])
def send_history(message):
    response = requests.get('http://127.0.0.1:8000/api/orders',)
    orders = response.json()
    for order in orders:
        text = f'''
        Пользователь: {order['user']}
    
        Номер телефона: {order['phone']}
    
        Номер заказа: #{order['order_id']}
    
        Цена заказа: {intcomma(order['price'])}
        --------------------------------------------------------------
        Заказ создан: {order['created_at']}
        '''
        bot.send_message(message.chat.id, text)
bot.polling()
