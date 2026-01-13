import ptbot
import os
import dotenv
from dotenv import load_dotenv
import pytimeparse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(chat_id, message_id, secs_left, total_seconds):
    progress = render_progressbar(total_seconds, total_seconds - secs_left)
    bot.update_message(chat_id, message_id, f'Осталось'
    f' {progress}')


def timer_finished(chat_id, message_id, text):
    bot.update_message(chat_id, message_id, f"Время вышло! Вы устанавливали: '{text}'")


def handle_message(chat_id, text):
    seconds = pytimeparse.parse(text)
    message_id = bot.send_message(chat_id, f"Таймер установлен на {seconds} секунд...")
    bot.create_countdown(seconds, notify_progress, chat_id, message_id, seconds)
    bot.create_timer(seconds, timer_finished, chat_id, message_id, text)


def main():
    load_dotenv()
    TG_TOKEN = os.environ['TOKEN']
    TG_CHAT_ID = os.environ['TG_CHAT_ID']
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(handle_message, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
