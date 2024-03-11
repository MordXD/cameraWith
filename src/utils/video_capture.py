
import time
import cv2
import os
from src.utils import CustomLogger


class VideoCapture:
    def __init__(self, stream_url, output_dir, capture_duration=5):
        self.stream_url = stream_url
        self.output_dir = output_dir
        self.capture_duration = capture_duration

    def start_video_capture(self):
        cap = cv2.VideoCapture(self.stream_url)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1270)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        if not cap.isOpened():
            CustomLogger.logger.error("Cannot open stream for video capture")
            return None

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        fourcc = cv2.VideoWriter_fourcc(*'H264')
        output_filename = f'captured_{int(time.time())}.mp4'
        output_path = os.path.join(self.output_dir, output_filename)
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))

        start_time = time.time()
        CustomLogger.logger.info("Starting video capture...")

        while time.time() - start_time < self.capture_duration:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

        return output_path
