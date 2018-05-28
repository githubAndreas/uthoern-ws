from typing import Dict


class Info:

    def __init__(self, generated_on: str, item_range: str, version: str):
        self.__generated_on = generated_on
        self.__item_range = item_range
        self.__version = version

    def get_generatd_on(self) -> str:
        return self.__generated_on

    def get_item_range(self) -> str:
        return self.__item_range

    def get_version(self) -> str:
        return self.__version

    @staticmethod
    def from_dict(data: Dict) -> 'Info':
        return Info(data['generated_on'], data['slice'], data['version'])
