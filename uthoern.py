from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from logger import Logger
from track_filter import TrackFilter
from playlist_util import PlaylistUtil

if __name__ == '__main__':
    Logger.log_info('Start uthoern')
    files = PlaylistParser.parse_folder('E:/Development/uthoern/test')

    slices = PlaylistSliceConverter.from_json_files(files)

    unique_tracks = TrackFilter.unique_from_playlist_slices(slices)
    total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

    Logger.log_info('Stop uthoern')
