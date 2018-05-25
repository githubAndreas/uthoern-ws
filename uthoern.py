from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter

if __name__ == '__main__':
    files = PlaylistParser.parse_folder('E:/Development/uthoern/test')

    slices = PlaylistSliceConverter.from_json_files(files)
