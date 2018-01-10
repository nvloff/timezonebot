from abc import ABCMeta, abstractmethod

class Adapter(metaclass=ABCMeta):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def __setitem__(self, key, item):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def store(self):
        pass

