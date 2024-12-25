from abc import ABC, abstractmethod
from constants import RANDOM_STATE, N_FOLDS, DATA_PATH
from lightautoml.automl.presets.tabular_presets import TabularUtilizedAutoML
from lightautoml.report.report_deco import ReportDecoUtilized
from lightautoml.tasks import Task
import numpy

class ModelConfigBase(ABC):

    def __init__(self):
        self.task_type = ''
        self.test_proportion = 0

    @abstractmethod
    def fill_task_type(self, task_type):
        pass

    @abstractmethod
    def fill_test_proportion(self, test_proportion):
        pass


class AutoMLModelConfig(ModelConfigBase):

    def __init__(self):
        super().__init__()
        self.models = []
        self.timeout = 0

    def fill_task_type(self, task_type):
        self.task_type = task_type

    def fill_test_proportion(self, test_proportion):
        self.test_proportion = test_proportion

    def fill_models(self, models):
        self.models = models

    def fill_timeout(self, timeout):
        self.timeout = timeout


class ModelEmployerBase(ABC):

    def __init__(self, model_config):
        self.model_config = model_config
        self.model = None

    @abstractmethod
    def configure_model(self):
        pass

    @abstractmethod
    def train_model(self, X_train, y_train, X_val, y_val):
        pass

    @abstractmethod
    def make_prediction(self, test_data):
        pass


class AutoMLModelEmployer(ModelEmployerBase):
    def __init__(self, model_config: AutoMLModelConfig):
        super().__init__(model_config)

    def configure_model(self):

        task = Task(self.model_config.task_type)
        report_decorator = ReportDecoUtilized(
            output_path=DATA_PATH.absolute().as_posix() + 'model_training_report'
        )

        self.model = report_decorator(
            TabularUtilizedAutoML(
                task=task,
                timeout=self.model_config.timeout,
                general_params = {'use_algos': self.model_config.models},
                reader_params={'cv': N_FOLDS}
            )
        )

    def train_model(self, X_train, y_train, X_val, y_val):

        train_data = # объединить train
        val_data = # объединить val

        roles = {'target': 'target'}
        numpy.random.seed(RANDOM_STATE)

        pred = self.model.fit_predict(
            train_data,
            roles=roles,
            valid_data=val_data,
            verbose=1
        )

    def make_prediction(self, test_data):

        predictions = self.model.predict(test_data).data.flatten().round()
        return predictions

