import unittest
from src.model import AutoMLModelEmployer, EmptyConfigError, AutoMLModelConfig
from src.facade import ModelTrainingFacade, WrongTypeOfVariablesError, EmptyDataFrameError
from src.database import SQLiteDatabase, NotIteratorError
from constants import DATA_PATH
import pandas


class AutoMLModelEmployerTests(unittest.TestCase):

    def test_init_rejects_unfilled_config(self):
        config = AutoMLModelConfig()
        with self.assertRaises(EmptyConfigError):
            _ = AutoMLModelEmployer(config)


class ModelTrainingFacadeTests(unittest.TestCase):

    def test_init_rejects_unfilled_config(self):
        config = AutoMLModelConfig()
        with self.assertRaises(EmptyConfigError):
            _ = ModelTrainingFacade(config)

    def test_create_and_train_model_rejects_variables_of_wrong_type(self):
        config = AutoMLModelConfig()
        config.test_proportion = 0.3
        config.doc_type = 'csv'
        config.models = ['auto']
        config.task_type = 'binary'
        config.timeout = 90

        facade = ModelTrainingFacade(config)
        train_data = ['1', '2', '3']
        val_data = None

        with self.assertRaises(WrongTypeOfVariablesError):
            facade.create_and_train_model(train_data, val_data)

    def test_create_and_train_model_rejects_empty_dataframes(self):
        config = AutoMLModelConfig()
        config.test_proportion = 0.3
        config.doc_type = 'csv'
        config.models = ['auto']
        config.task_type = 'binary'
        config.timeout = 90

        facade = ModelTrainingFacade(config)
        train_data = pandas.DataFrame()
        val_data = pandas.DataFrame()

        with self.assertRaises(EmptyDataFrameError):
            facade.create_and_train_model(train_data, val_data)


class SQLiteDatabaseTests(unittest.TestCase):

    def test_get_raw_target_generator_yields_correct_data(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.csv'
        database = SQLiteDatabase(path_to_dataset)

        array = [(1, ), (2, ), (3, ), (4, )]
        yield_value = next(database._get_raw_target_generator(array))

        self.assertEqual(1, yield_value)

    def test_get_raw_target_generator_rejects_incorrect_data(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.csv'
        database = SQLiteDatabase(path_to_dataset)

        array = [1, 2, 3, 4]
        with self.assertRaises(TypeError):
            _ = next(database._get_raw_target_generator(array))

    def test_get_raw_features_generator_yields_correct_data(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.csv'
        database = SQLiteDatabase(path_to_dataset)

        array = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6)]
        yield_value = next(database._get_raw_features_generator(array))

        self.assertEqual([1, 2, 3], yield_value)

    def test_get_raw_features_generator_rejects_incorrect_data(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.csv'
        database = SQLiteDatabase(path_to_dataset)

        array = [1, 2, 3, 4]
        with self.assertRaises(TypeError):
            _ = next(database._get_raw_features_generator(array))

    def test_numpy_array_creation_from_raw_accepts_only_iterators(self):
        path_to_dataset = f'{DATA_PATH.absolute().as_posix()}/data_for_training.csv'
        database = SQLiteDatabase(path_to_dataset)

        func = lambda x: x
        with self.assertRaises(NotIteratorError):
            _ = database._numpy_array_creation_from_raw(func)


if __name__ == '__main__':
    unittest.main()
