from abc import ABCMeta, abstractmethod

# This is a metaclass
#
# Pretty much means that it just defines methods we want specific implemenations
# to have, without actually implementing anything.
#
# A simple description of what an Adapter can do, without doing anything
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

