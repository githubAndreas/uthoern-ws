from typing import Dict


class Info:

    def __init__(self, item_range: str):
        self.__item_range = item_range

    def get_item_range(self) -> str:
        return self.__item_range

    @staticmethod
    def from_dict(data: Dict) -> 'Info':
        return Info(data['slice'])
