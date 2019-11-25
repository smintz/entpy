import unittest

from ent_schema import EntSchema, StringSchemaField, NumberSchemaField, EntSchemaEdge


class EntLocationSchema(EntSchema):
    @staticmethod
    def getName():
        return "location"

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


if __name__ == "__main__":
    unittest.main()
