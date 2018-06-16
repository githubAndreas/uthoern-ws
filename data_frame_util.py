import pandas as pd
import csv
from os import path
from date_time_util import DateTimeUtil
import numpy as np


class DataFrameUtil:
    TEAM: str = 'TeamLuebeck'

    CHALLENGE_TRACK: str = 'main'

    CONTACT_INFORMATION: str = 'andreas.huebner@stud.fh-luebeck.de'

    FILE_NAME: str = TEAM + '_mdp_submission.csv'

    URL_PREFIX: str = 'spotify:track:'

    CSV_HEADER = ['team_info', TEAM, CHALLENGE_TRACK, CONTACT_INFORMATION]

    @staticmethod
    def export_to_csv(recommentation_dict, rel_path: str) -> None:
        absolute_export_path = path.abspath(rel_path)
        file_name = DataFrameUtil.__create_export_file_name(absolute_export_path)

        with open(file_name, 'w+') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(DataFrameUtil.CSV_HEADER)

            for pid, recomm_array in recommentation_dict.items():
                row = np.append(np.array(str(pid)), [" " + DataFrameUtil.URL_PREFIX + s for s in recomm_array])
                writer.writerow(row)

            csv_file.close()

    @staticmethod
    def __create_export_file_name(absolute_export_path: str) -> str:
        file_name = DateTimeUtil.get_timestamp_as_string() + '_' + DataFrameUtil.FILE_NAME

        return path.join(absolute_export_path, file_name)
