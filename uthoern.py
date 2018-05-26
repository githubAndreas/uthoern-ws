from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from logger import Logger

if __name__ == '__main__':
    Logger.log_info('Start uthoern')
    files = PlaylistParser.parse_folder('E:/Development/uthoern/test')

    slices = PlaylistSliceConverter.from_json_files(files)
    Logger.log_info('Stop uthoern')
