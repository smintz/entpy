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
        location_schema = EntLocationSchema()
        EntLocation = location_schema.getEntClass()
        EntLocationMutator = location_schema.getMutator()
        EntLocationFactory = location_schema.getEntFactory()

        tlv = EntLocationMutator.create()
        tlv.setCity("Tel Aviv")
        tlv.setCountry("Israel")  # .save()
        result = tlv.save()

        self.assertEqual(result.getCountry(), "Israel")
        self.assertEqual(result.getCity(), "Tel Aviv")

        u = EntLocationMutator.update(result)

        u.setCity("Holon")
        result = u.save()
        self.assertEqual(result.getCity(), "Holon")

        read = EntLocationFactory.gen(1)
        self.assertEqual(read.getCity(), "Holon")


if __name__ == "__main__":
    unittest.main()
