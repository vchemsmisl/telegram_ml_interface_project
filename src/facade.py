from src.model import AutoMLModelConfig, AutoMLModelEmployer
from src.database import SQLiteDatabase
from constants import DATA_PATH, DATABASE_PATH, RANDOM_STATE, TRAINING_REPORT_PATH
from sklearn.model_selection import train_test_split
import pandas
import numpy
import shutil

class ModelTrainingFacade:

    def __init__(self, filled_config):
        self.config = filled_config
        # self.bot = TgBot(self.config)
        self.database = None
        self.model = None

    # def collect_data_and_parameters(self):
    #     self.bot.request_parameters_from_user()
        # self.bot.start_infinity_polling()

    def prepare_data(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.{self.config.doc_type}'
        self.database = SQLiteDatabase(path_to_dataset)
        self.database.create_database()

        target, target_column_name = self.database.get_target()
        features, features_columns_names = self.database.get_features()

        X_train, X_val, y_train, y_val = train_test_split(
            features,
            target,
            stratify=target,
            test_size=self.config.test_proportion,
            random_state=RANDOM_STATE
        )

        train_data_array = numpy.concatenate((X_train, y_train.reshape((1, -1)).T), axis=1)
        val_data_array = numpy.concatenate((X_val, y_val.reshape((1, -1)).T), axis=1)

        train_data_df = pandas.DataFrame(train_data_array, columns=features_columns_names + target_column_name)
        val_data_df = pandas.DataFrame(val_data_array, columns=features_columns_names + target_column_name)

        return train_data_df, val_data_df

    def create_and_train_model(self, train_data, val_data):
        self.model = AutoMLModelEmployer(self.config)
        self.model.configure_model()
        self.model.train_model(train_data, val_data)
        self._training_report_to_zip()

    @staticmethod
    def _training_report_to_zip():
        shutil.make_archive(base_name=TRAINING_REPORT_PATH,
                            format='zip',
                            root_dir=TRAINING_REPORT_PATH)
