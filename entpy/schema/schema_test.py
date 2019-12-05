import unittest

from entpy.schema.schema import EntSchema, StringSchemaField, NumberSchemaField, EntSchemaEdge


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


LocationSchema = EntLocationSchema()
EntLocation = LocationSchema.getEntClass()
EntLocationMutator = LocationSchema.getMutator()
EntLocationFactory = LocationSchema.getEntFactory()


class EntPersonSchema(EntSchema):
    @staticmethod
    def getName():
        return "person"

    @staticmethod
    def getFields():
        return {
            "Name": StringSchemaField("name"),
            "Age": NumberSchemaField("age"),
            "LocationID": NumberSchemaField("location_id"),
        }

    @staticmethod
    def getEdges():
        return {"Location": EntSchemaEdge("LocationID", LocationSchema)}


PersonSchema = EntPersonSchema()
EntPersonMutator = PersonSchema.getMutator()
EntPersonFactory = PersonSchema.getEntFactory()


class EntSchemaTest(unittest.TestCase):
    def test_schema(self):

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

        smintz = (
            EntPersonMutator.create()
            .setName("Shahar")
            .setAge(35)
            .setLocationID(result.getID())
            .save()
        )
        self.assertEqual(smintz.getName(), "Shahar")
        self.assertEqual(smintz.genLocation().getCountry(), result.getCountry())


if __name__ == "__main__":
    unittest.main()
