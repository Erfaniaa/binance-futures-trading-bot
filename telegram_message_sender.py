import telegram
from credentials import TELEGRAM_API_KEY, TELEGRAM_USER_ID
from config import SEND_TELEGRAM_MESSAGE
import logging


if SEND_TELEGRAM_MESSAGE:
    telegram_bot = telegram.Bot(token=TELEGRAM_API_KEY)


def send_new_order_message(symbol, side, quantity):
    send_message(f"new order created [{str(symbol)},{side},{str(quantity)}]")


def send_open_long_position_message(order_id):
    send_message(f"long position with order_id {str(order_id)} opened.")


def send_open_short_position_message(order_id):
    send_message(f"short position with order_id {str(order_id)} opened.")


def send_cancel_order_message(order_id):
    send_message(f"order with id {str(order_id)} canceled.")


def send_cancel_open_orders_for_symbol_message(symbol):
    send_message(f"order with id {str(symbol)} canceled.")


def send_message(message):
    if not SEND_TELEGRAM_MESSAGE:
        return

    try:
        telegram_bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
    except telegram.error.TelegramError:
        logging.error("ERROR in sending message to telegram")
