import logging
import sys


class Logger:

    @classmethod
    def __init__(cls):
        cls.__logger = logging.getLogger()
        cls.__logger.setLevel(level=logging.INFO)
        fh = logging.FileHandler('uthoern.log')
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        cls.__logger.addHandler(fh)
        cls.__logger.addHandler(ch)

    @classmethod
    def log_info(cls, msg: str) -> None:
        cls.__logger.info(msg)

    @classmethod
    def log_error(cls, msg: str) -> None:
        cls.__logger.error(msg)
