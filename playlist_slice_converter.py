import json
from playlist_slice import PlaylistSlice


class PlaylistSliceConverter:

    def from_json_files(files):
        slices = []
        for file in files:
            with open(file, 'r') as file_content:
                data = json.load(file_content)
                playlist_slice = PlaylistSlice.from_dict(data);
                slices.append(playlist_slice)

        return slices
