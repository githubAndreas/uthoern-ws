import datetime


class Logger:

    @staticmethod
    def log_info(msg):
        Logger.__log('INFO', msg)

    @staticmethod
    def log_error(msg):
        Logger.__log('ERROR', msg)

    @staticmethod
    def __log(level, msg):
        now = datetime.datetime.now()
        print(str(now) + ': [' + level + '] ' + msg)
