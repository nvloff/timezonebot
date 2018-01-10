from adapters.memory_adapter import MemoryAdapter

class Repository:
    """A simple Repository pattern that supports adapters"""
    def __init__(self, adapter = MemoryAdapter()):
        self.adapter = adapter
        self.adapter.load()

    def load(self):
        self.adapter.load

    def __setitem__(self, key, item):
        self.adapter[key] = item

    def __getitem__(self, key):
        return self.adapter[key]

    def items(self):
        return self.adapter.items()

    def store(self):
        self.adapter.store()



