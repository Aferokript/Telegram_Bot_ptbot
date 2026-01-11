import ptbot
import os
import random
import dotenv
from dotenv import load_dotenv
import pytimeparse

load_dotenv()

TG_TOKEN = os.environ['TOKEN']
bot = ptbot.Bot(TG_TOKEN)
TG_CHAT_ID = 7280963930

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def notify_progress(chat_id,seconds, message_id, secs_left):
    bot.update_message(chat_id, message_id, f'Осталось {render_progressbar(secs_left, seconds)}')

def handle_message(chat_id, text):
    seconds = pytimeparse.parse(text)

    message_id = bot.send_message(chat_id, f"Таймер установлен на {seconds} секунд...")

    def wait():
        bot.update_message(chat_id, message_id, f" Время вышло! Вы устанавливали: '{text}'")

    def progress_callback(secs_left):
        notify_progress(chat_id, message_id, secs_left, seconds)

    bot.create_countdown(seconds, progress_callback)
    bot.create_timer(seconds, wait)


bot.reply_on_message(handle_message)
bot.run_bot()
