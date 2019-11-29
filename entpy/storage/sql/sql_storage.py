class SQLStorage:
    def __init__(self, conn, ent_class):
        self.conn = conn
        self.c = conn.cursor()
        self.ent = ent_class
        self.migrateTable()

    def migrateTable(self):
        keys = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        fields = self.ent.getFields()
        for field_name in self.ent.getFields().keys():
            field = fields[field_name]
            keys.append(field.storage_key + " VARCHAR(255)")
        query = """\
CREATE TABLE IF NOT EXISTS {table}  ({keys})
""".format(
            table=self.getTableName(), keys=", ".join(keys)
        )

        self.c.execute(query)

    def getTableName(self):
        return self.ent.getName()

    def select(self, keys):
        print("select", self.getTableName(), keys)
        result = dict()
        field_keys = ["id"]
        fields = self.ent.getFields()
        for name in fields:
            field_keys.append(fields[name].storage_key)

        placeholder = "?"
        placeholders = ", ".join(placeholder * len(keys))
        query = "SELECT %s FROM %s WHERE id IN (%s)" % (
            ", ".join(field_keys),
            self.getTableName(),
            placeholders,
        )
        self.c.execute(query, keys)
        r = self.c.fetchall()


        for record in r:
            record_id = record[0]
            record_dict = dict()
            i = 0
            for f in field_keys:
                record_dict[f] = record[i]
                i = i + 1
            result[record_id] = record_dict

        return result

    def create(self, data):
        print("create", self.getTableName(), data)

        placeholder = "?"
        placeholders = ", ".join(placeholder * len(data.values()))
        query = "INSERT INTO {table} ({keys}) VALUES ({values})".format(
            table=self.getTableName(), keys=", ".join(data.keys()), values=placeholders
        )
        self.c.execute(query, list(data.values()))
        return self.c.lastrowid

    def update(self, key, data):
        print("update", self.getTableName(), key, data)

        placeholders = []
        values = []
        for k in data.keys():
            placeholders.append(k + " = ?")
            values.append(data[k])

        query = "UPDATE {table} SET {placeholders} WHERE id = ?".format(
            table=self.getTableName(), placeholders=", ".join(placeholders)
        )

        values.append(key)
        self.c.execute(query, values)
        return key

    def delete(self, key):
        print("delete", self.getTableName(), key)
        self.c.execute("DELETE FROM %s WHERE id = ?" % self.getTableName(), [key])
        return key
