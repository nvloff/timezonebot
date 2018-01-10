from adapters.memory_adapter import MemoryAdapter

class Repository:
    """A simple Repository pattern that supports adapters"""

    # by default we attach the memory adapter that has no persistance
    def __init__(self, adapter = MemoryAdapter()):
        self.adapter = adapter
        self.adapter.load()


    # simply proxy to the adapter
    def load(self):
        self.adapter.load()

    # __setitem__ is a special method that allows [key]=val to work on objects
    def __setitem__(self, key, item):
        self.adapter[key] = item

    # __getitem__ is a special method that allows [key] to return a value
    def __getitem__(self, key):
        return self.adapter[key]

    # proxy to the adapter
    def items(self):
        return self.adapter.items()

    # proxy to the adapter
    def store(self):
        self.adapter.store()



