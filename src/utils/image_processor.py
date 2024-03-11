
from PIL import Image
from dotenv import load_dotenv
from src.utils import CustomLogger
from moondream import *
import time
import cv2
import os
from huggingface_hub import *
from transformers import (
    CodeGenTokenizerFast as Tokenizer,
)


load_dotenv()

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VIDEO_STREAM_URL = os.getenv('VIDEO_STREAM_URL')
IMAGES_DIR = os.getenv('IMAGES_DIR')
VIDEO_DIR = os.getenv('VIDEO_DIR')

NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'
CYAN = '\033[96m'


class ImageProcessor:
    def __init__(self, model_id, device):
        self.device = device
        self.dtype = detect_device()[1]
        self.tokenizer = Tokenizer.from_pretrained(model_id)
        self.moondream = Moondream.from_pretrained(model_id).to(device=device, dtype=self.dtype)
        self.moondream.eval()

    @staticmethod
    def capture_frame(stream_url):
        cap = cv2.VideoCapture(stream_url)
        if not cap.isOpened():
            CustomLogger.logger.error("Cannot open stream")
            return
        ret, frame = cap.read()
        if not ret:
            CustomLogger.logger.error("Can't receive frame. Exiting...")
        else:
            filename = os.path.join(IMAGES_DIR, f'frame_{int(time.time())}.png')
            cv2.imwrite(filename, frame)
            CustomLogger.logger.info(f'Saved {filename}')
        cap.release()

    def process_image(self, image_dir):
        images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.png')]
        if not images:
            CustomLogger.logger.warning("No Images found in the directory.")
            return None, None
        latest_image = max(images, key=os.path.getmtime)
        for image in images:
            if image != latest_image:
                os.remove(image)
                CustomLogger.logger.info(f"Removed {image}")
        image = Image.open(latest_image)
        image_embeds = self.moondream.encode_image(image)
        return image_embeds

    def detect_person(self, image_embeds):
        prompt = f"{NEON_GREEN} Is there a PERSON in the image?{RESET_COLOR}( ONLY ANSWER WITH YES OR NOT)"
        CustomLogger.logger.info(f"> {prompt}")
        answer = self.moondream.answer_question(image_embeds, prompt, self.tokenizer).strip().upper()
        CustomLogger.logger.info(CYAN + answer + RESET_COLOR)
        return answer == "YES"

    def describe_image(self, image_embeds):
        prompt = "Describe the image in detail, try to identify Gender, Objects, Clothing etc:"
        answer = self.moondream.answer_question(image_embeds, prompt, self.tokenizer)
        return answer
