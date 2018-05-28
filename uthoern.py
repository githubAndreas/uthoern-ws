from logger import Logger
from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from playlist_util import PlaylistUtil
from track_filter import TrackFilter
from ranging_matrix_factory import RangingMatrixFactory

if __name__ == '__main__':
    Logger.log_info('Start uthoern')
    file_collection = PlaylistParser.parse_folder('E:/Development/uthoern/test')
    # files = PlaylistParser.parse_folder('E:/Development/_data/mpd.v1/data')

    slices = PlaylistSliceConverter.from_json_files(file_collection)

    unique_track_uris = TrackFilter.unique_track_uris_from_playlist_slices(slices)
    total_number_of_playlist = PlaylistUtil.count_playlists_of_slices(slices)

    ranging_matrix = RangingMatrixFactory.create_nparray_matrix(total_number_of_playlist, len(unique_track_uris),
                                                                slices, unique_track_uris)

    Logger.log_info('Stop uthoern')
