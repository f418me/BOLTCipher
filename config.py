import os
import logging
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.LOG_LEVEL = os.getenv('LOG_LEVEL')

        log_level = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR,
                     'CRITICAL': logging.CRITICAL}

        self.PAGE_TITLE = os.getenv('PAGE_TITLE')
        self.LOG_LEVEL_INT = log_level.get(self.LOG_LEVEL)
        self.PAGE_INFO = os.getenv('PAGE_INFO')
        self.CONTENT_PRICE = os.getenv('CONTENT_PRICE')