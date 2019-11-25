import unittest

from ent_schema import EntSchema, StringSchemaField, NumberSchemaField, EntSchemaEdge

class EntLocationSchema(EntSchema):
    @staticmethod
    def getFields():
        return {
            "City": StringSchemaField("city"),
            "Country": StringSchemaField("country"),
        }

class EntSchemaTest(unittest.TestCase):

    def test_schema(self):
        location = EntLocationSchema().getEntClass()
        result = location.getCity()
        self.assertEqual(result, "abc")
        self.assertEqual(1,2)

if __name__ == '__main__':
    unittest.main()
