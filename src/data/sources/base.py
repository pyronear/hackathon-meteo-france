from abc import ABC, abstractmethod


class BaseSource(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def save(self):
        pass
