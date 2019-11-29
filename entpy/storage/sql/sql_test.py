import unittest
import sqlite3
from sql_storage import SQLStorage
from entpy.schema.ent_schema import EntSchema, StringSchemaField


class EntTestSchema(EntSchema):
    @staticmethod
    def getName():
        return "test"


    @staticmethod
    def getFields():
        return {
            "Name": StringSchemaField('name')
        }

EntTest = EntTestSchema()


class SQLStorageTest(unittest.TestCase):
    def test_create(self):
        conn = sqlite3.connect(":memory:")
        storage = SQLStorage(conn, EntTest)

        id = storage.create({'name': 'Shahar'})
        self.assertEqual(id, 1)

        result = storage.select([1])
        self.assertEqual(result[id]['name'], "Shahar")

        id = storage.update(id, {'name': 'Lior'})
        result = storage.select([id])
        self.assertEqual(result[id]['name'], "Lior")

        storage.delete(id)
        result = storage.select([id])
        self.assertEqual(result.get(id, None), None)


if __name__ == "__main__":
    unittest.main()
