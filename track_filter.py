from logger import Logger
from typing import List, Dict
from playlist_slice import PlaylistSlice


class TrackFilter:

    @staticmethod
    def unique_track_uris_from_playlist_slices(playlist_slices: List[PlaylistSlice]) -> Dict[str, int]:
        Logger.log_info('Start collecting unique title urls')

        unique_track_urls = {}
        index_counter = 0;
        track_counter = 0;

        for p_slice in playlist_slices:
            for playlist in p_slice.get_playlist_collection():
                for track in playlist.get_tracks():
                    url = track.get_simplified_uri()
                    track_counter = track_counter + 1;

                    if url not in unique_track_urls:
                        unique_track_urls[url] = index_counter
                        index_counter = index_counter + 1

            Logger.log_info('Slice[' + p_slice.get_info().get_item_range() + '] track urls successfully collected')

        Logger.log_info(
            'Totally  unique uris: ' + str(len(unique_track_urls)) + ' from total uris:' + str(track_counter) + ' founded')

        return unique_track_urls
