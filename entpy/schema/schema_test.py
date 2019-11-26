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

        tlv = EntLocationMutator.create()
        print("EntLocationMutator", EntLocationMutator.__dict__)
        print("tlv", tlv.__dict__)
        print("tlv.setCity   ", tlv.setCity)
        print("tlv.setCountry", tlv.setCountry)
        tlv.setCity("Tel Aviv")
        tlv.setCountry("Israel")  # .save()
        result = tlv.save()
        print(result.__dict__)

        u = EntLocationMutator.update(result)
        u.setCity("Tel Aviv")
        result = u.save()

        self.assertEqual(result.getCountry(), "Israel")
        self.assertEqual(result.getCity(), "Tel Aviv")


if __name__ == "__main__":
    unittest.main()
