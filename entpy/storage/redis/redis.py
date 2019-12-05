class RedisStorage:
    def __init__(self, connection, ent_class):
        self.c = connection
        self.ent = ent_class

    def getTableName(self):
        return self.ent.getName()

    def select(self, ids):
        pipe = self.c.pipeline()
        result = dict()
        for id in ids:
            pipe.hgetall(self.getTableName() + "/" + str(id))

        r = pipe.execute()
        i = 0
        for elem in r:
            id = ids[i]
            result[id] = convert(elem)
            i = i + 1

        print(r)
        print(result)

        return result

    def nextID(self):
        return self.c.incr(self.getTableName() + "/counter")

    def create(self, data):
        id = self.nextID()
        return self.update(id, data)

    def update(self, id, data):
        self.c.hmset(self.getTableName() + "/" + str(id), data)
        return id

    def delete(self, id):
        self.hdel(id)
        return id


# https://stackoverflow.com/a/33160507
def convert(data):
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, (str, int)):
        return str(data)
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return tuple(map(convert, data))
    if isinstance(data, list):
        return list(map(convert, data))
    if isinstance(data, set):
        return set(map(convert, data))
