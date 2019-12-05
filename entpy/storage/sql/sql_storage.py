from entpy.schema.ent_schema import NumberSchemaField, StringSchemaField


class SQLStorage:
    def __init__(self, conn, ent_class):
        self.conn = conn
        self.c = conn.cursor()
        self.ent = ent_class
        self.migrateTable()

    @staticmethod
    def getRecordIDName():
        return "ent_id"

    @staticmethod
    def getRecordIDDefinition():
        return "INTEGER PRIMARY KEY AUTOINCREMENT"

    @staticmethod
    def stringFieldDef():
        return "VARCHAR"

    @staticmethod
    def numberFieldDef():
        return "INTEGER"

    @staticmethod
    def placeholder():
        return "?"

    def getColumnDefinitionForField(self, field):
        if isinstance(field, NumberSchemaField):
            return self.numberFieldDef()
        if isinstance(field, StringSchemaField):
            return self.stringFieldDef()
        raise ValueError("field is not a known EntSchemaField")

    def migrateTable(self):
        keys = [self.getRecordIDName() + " " + self.getRecordIDDefinition()]
        fields = self.ent.getFields()
        for field_name in self.ent.getFields().keys():
            field = fields[field_name]
            keys.append(
                field.storage_key + " " + self.getColumnDefinitionForField(field)
            )
        query = """\
CREATE TABLE IF NOT EXISTS {table}  ({keys})
""".format(
            table=self.getTableName(), keys=", ".join(keys)
        )

        self.c.execute(query)
        self.conn.commit()

    def getTableName(self):
        return self.ent.getName()

    def select(self, keys):
        print("select", self.getTableName(), keys)
        result = dict()
        field_keys = [self.getRecordIDName()]
        fields = self.ent.getFields()
        for name in fields:
            field_keys.append(fields[name].storage_key)

        placeholders = ", ".join([self.placeholder()] * len(keys))
        query = "SELECT %s FROM %s WHERE %s IN (%s)" % (
            ", ".join(field_keys),
            self.getTableName(),
            self.getRecordIDName(),
            placeholders,
        )
        print(query, keys)
        self.c.execute(query, keys)
        r = self.c.fetchall()

        print(r)
        for record in r:
            record_id = record[0]
            record_dict = dict()
            i = 0
            for f in field_keys:
                record_dict[f] = record[i]
                i = i + 1
            result[record_id] = record_dict

        return result

    @staticmethod
    def createQuery():
        return "INSERT INTO {table} ({keys}) VALUES ({values})"

    def lastrowid(self):
        return self.c.lastrowid

    def create(self, data):
        print("create", self.getTableName(), data)

        placeholders = ", ".join([self.placeholder()] * len(data.values()))
        query = self.createQuery().format(
            table=self.getTableName(),
            keys=", ".join(data.keys()),
            values=placeholders,
            record_id=self.getRecordIDName(),
        )
        print(query)
        self.c.execute(query, list(data.values()))
        lastrowid = self.lastrowid()
        self.conn.commit()
        return lastrowid

    def update(self, key, data):
        print("update", self.getTableName(), key, data)

        placeholders = []
        values = []
        for k in data.keys():
            placeholders.append(k + " = " + self.placeholder())
            values.append(data[k])

        query = "UPDATE {table} SET {placeholders} WHERE {record_id} = {placeholder}".format(
            table=self.getTableName(),
            record_id=self.getRecordIDName(),
            placeholders=", ".join(placeholders),
            placeholder=self.placeholder(),
        )

        values.append(key)
        self.c.execute(query, values)
        self.conn.commit()
        return key

    def delete(self, key):
        print("delete", self.getTableName(), key)
        self.c.execute(
            "DELETE FROM {table_name} WHERE {record_id} = ?".format(
                table_name=self.getTableName(), record_id=self.getRecordIDName()
            ),
            [key],
        )
        self.conn.commit()
        return key


class MySQLStorage(SQLStorage):
    def getRecordIDDefinition(self):
        return "INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (%s)" % self.getRecordIDName()

    @staticmethod
    def placeholder():
        return "%s"

    @staticmethod
    def stringFieldDef():
        return "TEXT"


class PostgreSQLStorage(SQLStorage):
    def getRecordIDDefinition(self):
        return "SERIAL PRIMARY KEY"

    @staticmethod
    def placeholder():
        return "%s"

    @staticmethod
    def createQuery():
        return "INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING {record_id}"

    def lastrowid(self):
        return self.c.fetchone()[0]
