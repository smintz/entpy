import unittest
from entpy.schema.schema import (
    EntSchema,
    StringSchemaField,
    NumberSchemaField,
    EntSchemaEdge,
)

import random
import string


def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))


MYSTRING = randomString()


class IntegrationTestFactory(unittest.TestCase):
    def setUp(self, storage_engine, connection):
        self.storage_engine = storage_engine
        self.connection = connection

    def getEntLocationSchema(self):
        storage = self.storage_engine
        conn = self.connection

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
                return storage(conn, self)

        return EntLocationSchema

    def getEntPersonSchema(self):
        storage = self.storage_engine
        conn = self.connection
        EntLocationSchema = self.getEntLocationSchema()
        LocationSchema = EntLocationSchema()

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
                return storage(conn, self)

        return EntPersonSchema

    def helper(self):
        EntLocationSchema = self.getEntLocationSchema()
        LocationSchema = EntLocationSchema()
        EntLocation = LocationSchema.getEntClass()
        EntLocationMutator = LocationSchema.getMutator()
        EntLocationFactory = LocationSchema.getEntFactory()
        EntPersonSchema = self.getEntPersonSchema()
        PersonSchema = EntPersonSchema()
        EntPersonMutator = PersonSchema.getMutator()
        EntPersonFactory = PersonSchema.getEntFactory()

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
