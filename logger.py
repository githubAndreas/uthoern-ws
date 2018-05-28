import datetime


class Logger:

    @staticmethod
    def log_info(msg: str) -> None:
        Logger.__log('INFO', msg)

    @staticmethod
    def log_error(msg: str) -> None:
        Logger.__log('ERROR', msg)

    @staticmethod
    def __log(level: str, msg: str) -> None:
        now = datetime.datetime.now()
        print(str(now) + ': [' + level + '] ' + msg)
