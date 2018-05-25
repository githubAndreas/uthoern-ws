import os
import re
import sys


class PlaylistParser:

    @staticmethod
    def parse_folder(absolute_folder_path):
        normalized_path = os.path.normpath(absolute_folder_path)
        PlaylistParser._check_folder_exists(normalized_path)

        file_names = os.listdir(normalized_path)

        files = []
        for file_name in file_names:
            if re.match('mpd\.slice\.\d+\-\d+\.json', file_name):
                absolute_file_name = os.path.join(normalized_path, file_name)
                files.append(absolute_file_name)

        return files

    @staticmethod
    def _check_folder_exists(normalized_path):
        if not os.path.exists(normalized_path):
            print("Error: Path not found: " + normalized_path)
            sys.exit(1)
