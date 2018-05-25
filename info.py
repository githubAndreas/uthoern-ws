class Info:

    def __init__(self, generated_on, item_range, version):
        self.__generated_on = generated_on
        self.__item_range = item_range
        self.__version = version

    def get_generatd_on(self):
        return self.__generated_on

    def get_item_range(self):
        return self.__item_range

    def get_version(self):
        return self.__version

    @staticmethod
    def from_dict(data):
        return Info(data['generated_on'], data['slice'], data['version'])
