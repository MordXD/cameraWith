

from datetime import datetime
import os

from dotenv import load_dotenv
import torch

from src.utils import CustomLogger
from src.utils.image_processor import ImageProcessor
from src.utils.openai_client import OpenAIClient
from src.utils.telegram_bot import TelegramBot
from src.utils.video_capture import VideoCapture

load_dotenv()

NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'
CYAN = '\033[96m'
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VIDEO_STREAM_URL = os.getenv('VIDEO_STREAM_URL')
IMAGES_DIR = os.getenv('IMAGES_DIR')
VIDEO_DIR = os.getenv('VIDEO_DIR')


class SecurityMonitor:
    def __init__(self):
        self.telegram_bot = TelegramBot(TELEGRAM_API_TOKEN)
        self.openai_client = OpenAIClient()
        self.image_processor = ImageProcessor("vikhyatk/moondream1", torch.device("cuda"))
        self.video_capture = VideoCapture(VIDEO_STREAM_URL, VIDEO_DIR)

    def run(self):
        while True:
            CustomLogger.logger.info("Starting loop...")
            self.image_processor.capture_frame(VIDEO_STREAM_URL)
            image_embeds = self.image_processor.process_image(IMAGES_DIR)
            if image_embeds is not None:
                person_detected = self.image_processor.detect_person(image_embeds)
                if person_detected:
                    CustomLogger.logger.info(f"{NEON_GREEN}Person detected. Starting video capture.{RESET_COLOR}")
                    video_path = self.video_capture.start_video_capture()
                    image_description = self.image_processor.describe_image(image_embeds)
                    CustomLogger.logger.info("Generating log...")
                    log = (f"Описание изображения: {image_description} \n Из описания фотографии, "
                           f"Не забывайте, что хорошо структурированный рассказ облегчает усвоение информации. "
                           f"Попробуйте ввести четкие заголовки и использовать списки"
                           f" для выделения ключевых деталей в ваших описаниях. ")
                    log_text = self.openai_client.generate_text(log)
                    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    file_path = os.path.join(VIDEO_DIR, f'{current_time}_Security_log.txt')
                    with open(file_path, 'w') as file:
                        file.write("[" + current_time + "] " + log_text)
                    CustomLogger.logger.info(f"{NEON_GREEN}[OK]{RESET_COLOR}")
                    CustomLogger.logger.info("Sending message...")
                    self.telegram_bot.send_message(, log_text, video_path)
                    CustomLogger.logger.info(f"{NEON_GREEN}[OK]{RESET_COLOR}")
            else:
                CustomLogger.logger.warning("Could not process image properly.")
