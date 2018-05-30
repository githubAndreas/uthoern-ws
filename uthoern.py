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

    ranging_df = RangingMatrixFactory.create_data_frame(slices)

    template_ranging_matrix = RangingMatrixFactory.create_template_ranging_matrix(ranging_df)


    Logger.log_info('Stop uthoern')
