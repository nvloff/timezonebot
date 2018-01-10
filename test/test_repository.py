import unittest

from repository import Repository

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.repo = Repository()

    def test_default_adapter(self):
        self.assertTrue(self.repo.adapter)

    def test_load(self):
        self.assertTrue(self.repo.load)

    def test_set_get(self):
        self.repo["id"] = "value"
        self.repo["id1"] = "value1"

        self.assertEqual("value", self.repo["id"])
        self.assertEqual("value1", self.repo["id1"])

    def test_items(self):
        self.repo["id"] = "value"
        self.repo["id1"] = "value1"

        self.assertEqual([('id', 'value'), ('id1', 'value1')], list(self.repo.items()))

    def test_store(self):
        self.repo.store()
