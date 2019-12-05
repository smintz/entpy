import psycopg2
import unittest
from entpy.storage.sql.sql_storage import PostgreSQLStorage
from e2e import IntegrationTestFactory
import socket

host = "postgres"
try:
    socket.gethostbyname(host)
except:
    host = "127.0.0.1"


conn = psycopg2.connect(host=host, user="postgres", password="my-secret-pw")


class SqliteTest(IntegrationTestFactory):
    def setUp(self):
        super(SqliteTest, self).setUp(PostgreSQLStorage, conn)

    def test_sqlite(self):
        self.helper()


if __name__ == "__main__":
    unittest.main()
