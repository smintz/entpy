import sqlite3
import unittest
from entpy.storage.sql.sql_storage import SQLStorage
from e2e import IntegrationTestFactory

conn = sqlite3.connect(":memory:")


class SqliteTest(IntegrationTestFactory):
    def setUp(self):
        super(SqliteTest, self).setUp(SQLStorage, conn)

    def test_sqlite(self):
        self.helper()


if __name__ == "__main__":
    unittest.main()
