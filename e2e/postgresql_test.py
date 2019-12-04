import unittest
import psycopg2
import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


from entpy.schema.ent_schema import (
    EntSchema,
    StringSchemaField,
    NumberSchemaField,
    EntSchemaEdge,
)
from entpy.storage.sql.sql_storage import PostgreSQLStorage


MYSTRING = randomString()
conn = psycopg2.connect(
    host="postgres", user="postgres", password="my-secret-pw", database="entpy"
)


class EntLocationSchema(EntSchema):
    @staticmethod
    def getName():
        return "location_" + MYSTRING

    @staticmethod
    def getFields():
        return {
            "City": StringSchemaField("city"),
            "Country": StringSchemaField("country"),
        }

    def setStorage(self):
        return PostgreSQLStorage(conn, self)


LocationSchema = EntLocationSchema()
EntLocation = LocationSchema.getEntClass()
EntLocationMutator = LocationSchema.getMutator()
EntLocationFactory = LocationSchema.getEntFactory()


class EntPersonSchema(EntSchema):
    @staticmethod
    def getName():
        return "people_" + MYSTRING

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

    def setStorage(self):
        return PostgreSQLStorage(conn, self)


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
        lior = (
            EntPersonMutator.create()
            .setName("Lior")
            .setAge(30)
            .setLocationID(result.getID())
            .save()
        )
        self.assertEqual(lior.getID(), 2)
        self.assertEqual(smintz.getName(), "Shahar")
        self.assertEqual(smintz.genLocation().getCountry(), result.getCountry())


if __name__ == "__main__":
    unittest.main()
