class Album:

    def __init__(self, name, uri):
        self.__name = name
        self.__uri = uri

    def get_name(self):
        return self.__name

    def get_uri(self):
        return self.__uri

    @staticmethod
    def from_dict(data):
        return Album(data['album_name'], data['album_uri'])
