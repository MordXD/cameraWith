import logging
from logging import StreamHandler, FileHandler


class CustomLogger(logging.Logger):
    _instance = None

    def __new__(cls, name, level=logging.INFO):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__(name, level)
        return cls._instance

    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)

        console_handler = StreamHandler()
        file_handler = FileHandler('app.log')

        console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        self.addHandler(console_handler)
        self.addHandler(file_handler)


logger = CustomLogger('my_app')
