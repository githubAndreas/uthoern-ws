from album import Album
from artists import Artists


class Track:

    def __init__(self, name, uri, pos, artist, album, duration):
        self.__name = name
        self.__uri = uri
        self.__pos = pos
        self.__artist = artist
        self.__album = album
        self.__duration = duration

    def get_name(self):
        return self.__name

    def get_uri(self):
        return self.__uri

    def get_pos(self):
        return self.__pos

    def get_artist(self):
        return self.__artist

    def get_album(self):
        return self.__album

    def get_duration(self):
        return self.__duration

    @staticmethod
    def from_dict(data):
        album = Album.from_dict(data)
        artist = Artists.from_dict(data)

        return Track(data['track_name'], data['track_uri'], data['pos'], artist, album, data['duration_ms'])
