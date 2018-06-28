import datetime


class DateTimeUtil:

    @staticmethod
    def get_timestamp_as_string() -> str:
        return datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S_%f");

    @staticmethod
    def generate_timestamp_id() -> str:
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f");
