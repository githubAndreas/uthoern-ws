from logger import Logger
from argparse import ArgumentParser
from os import path
import sys
from date_time_util import DateTimeUtil
from playlist_parser import PlaylistParser
from playlist_slice_converter import PlaylistSliceConverter
from model_util import ModelUtil

challenge_set_file_name = "challenge_set.json"


def __predict_model(abs_challenge_set_path: str, abs_model_path: str, model_instance_id: int) -> None:
    instance_id = DateTimeUtil.generate_timestamp_id()
    Logger.log_info("Start predict model instance '{}'".format(instance_id))

    # Load challange set
    file_collection = PlaylistParser.parse_folder(abs_challenge_set_path, challenge_set_file_name)

    slices = PlaylistSliceConverter.from_json_files(file_collection)

    # Lade columns
    unique_track_uris = ModelUtil.load_columns_from_disk(abs_model_path, model_instance_id)

    print("hello")
    # iteriere über challange set Batch

    # Erstelle panda Dataframe

    # Iteriere über columns
    # Lade model mit column name

    # Predict value

    # Schreibe Ihn zurück

    # Exportiere vorhersage in CSV für Batch


def __receive_path_argument():
    """Read path from command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("challenge_set_path", type=str, help='Path to challenge set')
    parser.add_argument("instance_id", type=int, help='Id of the instance')

    # Show --help if arguments are absent
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args.challenge_set_path, args.instance_id


if __name__ == '__main__':
    Logger.__init__()
    Logger.log_info('Start predict uthoern')

    challenge_set_path, instance_id = __receive_path_argument()

    abs_challenge_set_path = path.abspath(challenge_set_path)
    abs_model_path = path.abspath("./model_storage/{}".format(str(instance_id)))

    __predict_model(abs_challenge_set_path, abs_model_path, instance_id)

    Logger.log_info('Stop predict uthoern')
