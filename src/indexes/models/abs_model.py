from abc import ABC, abstractmethod

class AbstractModel(ABC):
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def train(self, keys, positions):
        pass

    @abstractmethod
    def __call__(self, keys):
        pass

    @abstractmethod
    def get_max_abs_err(self):
        pass

    @abstractmethod
    def get_mean_abs_err(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def save(self, path):
        pass
