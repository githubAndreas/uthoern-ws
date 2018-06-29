import csv
from builtins import staticmethod
from os import path

import numpy as np

from .date_time_util import DateTimeUtil


class DataFrameUtil:
    TEAM: str = 'TeamLuebeck'

    CHALLENGE_TRACK: str = 'main'

    CONTACT_INFORMATION: str = 'andreas.huebner@stud.fh-luebeck.de'

    FILE_NAME: str = TEAM + '_mdp_submission.csv'

    URL_PREFIX: str = 'spotify:track:'

    CSV_HEADER = ['team_info', TEAM, CHALLENGE_TRACK, CONTACT_INFORMATION]

    @staticmethod
    def export_to_csv(recommentation_dict, rel_path: str) -> None:

        file_name = DataFrameUtil.__create_export_file_name()

        absolute_export_path = path.join(path.abspath(rel_path), file_name)

        with open(absolute_export_path, 'w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(DataFrameUtil.CSV_HEADER)

            for pid, recomm_array in recommentation_dict.items():
                row = np.append(np.array(str(pid)), [" " + DataFrameUtil.URL_PREFIX + s for s in recomm_array])
                writer.writerow(row)

            csv_file.close()

        return file_name

    @staticmethod
    def __create_export_file_name() -> str:
        file_name = DateTimeUtil.get_timestamp_as_string() + '_' + DataFrameUtil.FILE_NAME

        return file_name

    @staticmethod
    def drop_columns(df, selected_columns):
        cols = [c for c in selected_columns if c in df.columns.values]
        df = df.drop(columns=cols)

        return df
