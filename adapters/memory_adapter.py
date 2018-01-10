from adapters.adapter import Adapter

class MemoryAdapter(Adapter):
    """A Dummy storage adapter that does stores the data in
    in-memory dict and doesn't persist to disk.

    Used for testing
    """
    def load(self):
        self.data = {}

    def __setitem__(self, key, item):
        self.data[key] = item

    def __getitem__(self, key):
        return self.data[key]

    def items(self):
        return self.data.items()

    def store(self):
        pass
