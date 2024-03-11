from telebot import TeleBot


class TelegramBot:
    def __init__(self, token):
        self.bot = TeleBot(token)

    def send_message(self, chat_id, text, video_path=None):
        if video_path:
            with open(video_path, 'rb') as video_file:
                self.bot.send_video(chat_id, video_file)
        self.bot.send_message(chat_id, text)
