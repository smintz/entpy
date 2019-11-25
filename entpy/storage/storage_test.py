import unittest
from local_data_storage import LocalDataStorage


class LocalDataStorageTest(unittest.TestCase):
    def test_create(self):
        storage = LocalDataStorage()

        id = storage.create("hello world")
        self.assertEqual(id, 1)

        result = storage.select([id])
        self.assertEqual(result[id], "hello world")

        id = storage.update(id, "hello world!")
        result = storage.select([id])
        self.assertEqual(result[id], "hello world!")

        storage.delete(id)
        result = storage.select([id])
        self.assertEqual(result.get(id, None), None)


if __name__ == "__main__":
    unittest.main()
