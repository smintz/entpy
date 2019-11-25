import unittest
from ent_loader import EntLoader
from entpy.storage.local_data_storage import LocalDataStorage


class EntLoaderTest(unittest.TestCase):
    def test_run(self):
        storage = LocalDataStorage()
        loader = EntLoader(storage)

        obj = {"name": "Lior"}
        id = storage.create(obj)

        result = loader.gen(id)
        self.assertEqual(result, obj)


if __name__ == "__main__":
    unittest.main()
