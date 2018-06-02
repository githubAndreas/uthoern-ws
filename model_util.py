from sklearn.externals import joblib
from os import path, makedirs
from logger import Logger


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
