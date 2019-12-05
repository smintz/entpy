from pymongo import MongoClient
import unittest
from entpy.storage.mongo.mongo import MongoStorage
from e2e import IntegrationTestFactory
import socket

host = "mongo"
try:
    socket.gethostbyname(host)
except:
    host = "127.0.0.1"


client = MongoClient(host, 27017)
db = client.test_database


class MongoTest(IntegrationTestFactory):
    def setUp(self):
        super(MongoTest, self).setUp(MongoStorage, db)

    def test_mongo(self):
        self.helper()


if __name__ == "__main__":
    unittest.main()
