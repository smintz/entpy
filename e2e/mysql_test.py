import mysql.connector
import unittest
from entpy.storage.sql.sql import MySQLStorage
from e2e import IntegrationTestFactory
import socket

host = "mysql"
try:
    socket.gethostbyname(host)
except:
    host = "127.0.0.1"


conn = mysql.connector.connect(
    host=host, user="root", passwd="my-secret-pw", database="entpy"
)


class SqliteTest(IntegrationTestFactory):
    def setUp(self):
        super(SqliteTest, self).setUp(MySQLStorage, conn)

    def test_sqlite(self):
        self.helper()


if __name__ == "__main__":
    unittest.main()
