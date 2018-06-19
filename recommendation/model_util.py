from sklearn.externals import joblib
from os import path, makedirs
from logger import Logger
import csv


class ModelUtil:
    MODEL_STORAGE = 'model_storage'

    FILE_TYPE = 'pkl'

    @staticmethod
    def save_to_disk(model, instance_id: str, model_type: str, column: str):
        Logger.log_info('Start saving model to disk')
        file_name = '{}_{}_{}.{}'.format(instance_id, model_type, column,
                                         ModelUtil.FILE_TYPE)

        instance_folder = path.join(path.abspath(ModelUtil.MODEL_STORAGE), instance_id)
        if not path.exists(instance_folder):
            makedirs(instance_folder)

        absolute_export_path = path.join(instance_folder, file_name)
        Logger.log_info("Path: '{}'".format(absolute_export_path))

        joblib.dump(model, absolute_export_path)
        Logger.log_info('Save model to disk successfully finished')

    @staticmethod
    def load_from_disk(instance_id: int, model_type: str, column: str):
        file_name = '{}_{}_{}.{}'.format(instance_id, model_type, column,
                                         ModelUtil.FILE_TYPE)

        instance_folder = path.join(path.abspath(ModelUtil.MODEL_STORAGE), str(instance_id))

        absolute_export_path = path.join(instance_folder, file_name)

        return joblib.load(absolute_export_path)

    @staticmethod
    def load_dict_from_disk(instance_id: int, model_type: str, unique_track_uris):
        Logger.log_info("Start loading models")
        model_dict = {}
        for column in unique_track_uris:
            file_name = '{}_{}_{}.{}'.format(instance_id, model_type, column,
                                             ModelUtil.FILE_TYPE)

            instance_folder = path.join(path.abspath(ModelUtil.MODEL_STORAGE), str(instance_id))

            absolute_export_path = path.join(instance_folder, file_name)

            model_dict[column] = joblib.load(absolute_export_path)

        Logger.log_info("Finishing loading models")
        return model_dict

    @staticmethod
    def save_columns_to_disk(unique_track_uris, instance_id) -> None:
        Logger.log_info("Start saving row columns to {}".format(instance_id))

        instance_folder = path.join(path.abspath(ModelUtil.MODEL_STORAGE), instance_id)
        if not path.exists(instance_folder):
            makedirs(instance_folder)

        absolute_export_path = path.join(instance_folder, '{}_columns.csv'.format(instance_id))

        with open(absolute_export_path, 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in unique_track_uris.items():
                writer.writerow([value, key])

        Logger.log_info("Finishing saving row columns")

    @staticmethod
    def load_columns_from_disk(norm_model_path: str, instance_id: int):
        unique_track_uris = {}
        absolute_file_path = path.join(norm_model_path, '{}_columns.csv'.format(instance_id))
        reader = csv.reader(open(absolute_file_path, 'r'))
        for row in reader:
            if len(row) == 2:
                value, key = row
                unique_track_uris[key] = value

        return unique_track_uris
