import unittest
import tempfile

from repository import Repository
from adapters.legacy_adapter import LegacyAdapter

class TestRepositoryLegacy(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile()
        self.repo = Repository(LegacyAdapter(self.temp_file.name))

    def tearDown(self):
        self.temp_file.close()

    def test_set_get(self):
        self.repo["id"] = "value"
        self.repo["id1"] = "value1"

        self.assertEqual("value", self.repo["id"])
        self.assertEqual("value1", self.repo["id1"])

    def test_items(self):
        self.repo["id"] = "value"
        self.repo["id1"] = "value1"

        self.assertEqual([('id', 'value'), ('id1', 'value1')], list(self.repo.items()))

    def test_persistance(self):
        self.repo["id"] = "value"
        self.repo["id1"] = "value1"

        self.repo.store()

        new_repo = Repository(LegacyAdapter(self.temp_file.name))

        self.assertEqual([('id', 'value'), ('id1', 'value1')], list(new_repo.items()))


        self.assertEqual("value", new_repo["id"])
        self.assertEqual("value1", new_repo["id1"])
