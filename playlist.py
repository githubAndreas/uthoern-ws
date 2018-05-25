from track import Track


class Playlist:

    def __init__(self, name, collaborative, pid, modified_at, num_tracks, num_albums, num_followers, tracks, num_edits,
                 duration_ms, num_artists):
        self.__name = name
        self.__collaborative = collaborative
        self.__pid = pid
        self.__modified_at = modified_at
        self.__num_tracks = num_tracks
        self.__num_albums = num_albums
        self.__num_followers = num_followers
        self.__tracks = tracks
        self.__num_edits = num_edits
        self.__duration_ms = duration_ms
        self.__num_artists = num_artists

    def get_name(self):
        return self.__name;

    def get_collaborative(self):
        return self.__collaborative

    def get_pid(self):
        return self.__pid

    def get_modified_at(self):
        return self.__modified_at

    def get_num_tracks(self):
        return self.__num_tracks

    def get_num_albums(self):
        return self.__num_albums

    def get_num_followers(self):
        return self.__num_followers

    def get_tracks(self):
        return self.__tracks

    def get_num_edits(self):
        return self.__num_edits

    def get_duration_ms(self):
        return self.__duration_ms

    def get_num_artists(self):
        return self.__num_artists

    @staticmethod
    def from_dict(data):
        tracks = []
        for item in data['tracks']:
            track = Track.from_dict(item)
            tracks.append(track)

        return Playlist(data['name'], data['collaborative'], data['pid'], data['modified_at'], data['num_tracks'],
                        data['num_albums'], data['num_followers'], tracks, data['num_edits'],
                        data['duration_ms'], data['num_artists'])
