from abc import ABC, abstractmethod

class ModelConfig:

    def __init__(self):
        self.task_type = None
        self.test_proportion = None

class ModelEmployerBase(ABC):
    pass

class AutoMLModelEmployer(ModelEmployerBase):
    pass