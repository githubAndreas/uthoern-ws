from logger import Logger
from argparse import ArgumentParser
from os import path
import sys
 

def __predict_model(norm_model_path: str, norm_challenge_set_path: str) -> None:
    pass


def __receive_path_argument():
    """Read path from command line arguments"""
    parser = ArgumentParser()
    parser.add_argument("model_path", type=str, help='Path to models')
    parser.add_argument("challenge_set_path", type=int, help='Path to challenge set')

    # Show --help if arguments are absent
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args.model_path, args.challenge_set_path


if __name__ == '__main__':
    Logger.__init__()
    Logger.log_info('Start predict uthoern')

    model_path, challenge_set_path = __receive_path_argument()

    norm_model_path = path.normpath(model_path)
    norm_challenge_set_path = path.normpath(challenge_set_path)

    __predict_model(norm_model_path, norm_challenge_set_path)

    Logger.log_info('Stop predict uthoern')
