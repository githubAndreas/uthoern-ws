import json
from playlist_slice import PlaylistSlice
from logger import Logger


class PlaylistSliceConverter:

    def from_json_files(files):
        Logger.log_info('Start converting ' + str(len(files)) + ' playlist files from json to object')
        slices = []
        for file in files:
            with open(file, 'r') as file_content:
                data = json.load(file_content)
                playlist_slice = PlaylistSlice.from_dict(data);
                slices.append(playlist_slice)
                Logger.log_info('Slice[' + playlist_slice.get_info().get_item_range() + '] successfully converted')

        Logger.log_info(str(len(slices)) + ' slices successfully converted to objects')
        return slices
