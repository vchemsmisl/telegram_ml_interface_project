import sqlite3
from sqlite3 import Error
import pandas
import numpy
from pathlib import Path
from constants import DATABASE_PATH

class ConnectionToDatabaseError(Exception):
    """Raised when the connection to SQLite database fails"""
    pass

class SQLiteConnector:

    def __init__(self):
        self.database_path = DATABASE_PATH
        self.connection = self.create_connection()

    def create_connection(self):

        try:
            connection = sqlite3.connect(self.database_path)
        except Error as e:
            raise ConnectionToDatabaseError(f"The error '{e}' occurred")

        return connection

    def execute_query(self, query):
        cursor = self.connection.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            try:
                names = [description[0] for description in cursor.description]
                return result, names
            except TypeError:
                return

        except Error as e:
            raise ConnectionToDatabaseError(f"The error '{e}' occurred")


class SQLiteDatabase:

    def __init__(self, dataset_path):
        self.connector = SQLiteConnector()
        self.dataset_path = dataset_path
        self.database_name = 'database_for_training'

    def create_database(self):
        dataframe = pandas.read_csv(self.dataset_path).drop('Unnamed: 0', axis=1)

        dataframe.to_sql(name=self.database_name,
                         con=self.connector.connection,
                         if_exists='replace')

        # try:
        #     dataframe.to_sql(name=self.database_name,
        #                      con=self.connector.connection,
        #                      if_exists='replace')
        # except ValueError:
        #     Path(DATABASE_PATH).unlink()
        #     dataframe.to_sql(name=self.database_name,
        #                      con=self.connector.connection)

    @staticmethod
    def _get_raw_target_generator(raw_target):
        for val in raw_target:
            yield val[0]

    @staticmethod
    def _get_raw_features_generator(raw_target):
        for val in raw_target:
            yield list(val)

    @staticmethod
    def _numpy_array_creation_from_raw(iter_function):

        array = []
        while True:
            try:
                array.append(next(iter_function))
            except StopIteration:
                break

        return numpy.array(array)

    def get_target(self):

        get_target_query = f"SELECT target FROM {self.database_name}"
        raw_target, target_column_name = self.connector.execute_query(get_target_query)
        iter_get_target_generator = iter(self._get_raw_target_generator(raw_target))

        return self._numpy_array_creation_from_raw(iter_get_target_generator), target_column_name

    def get_features(self):
        drop_target_query = f"ALTER TABLE {self.database_name} DROP COLUMN target"
        self.connector.execute_query(drop_target_query)

        get_features_query = f"SELECT * FROM {self.database_name}"
        raw_features, features_columns_names = self.connector.execute_query(get_features_query)
        iter_get_features_generator = iter(self._get_raw_features_generator(raw_features))

        return self._numpy_array_creation_from_raw(iter_get_features_generator), features_columns_names

    def add_predictions_column(self, predictions):
        pass

    def return_dataset(self):
        pass
