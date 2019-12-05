from bson import ObjectId


class MongoStorage:
    def __init__(self, db, ent_class):
        self.ent = ent_class
        self.db = db
        self.c = self.db[self.getTableName()]

    def getTableName(self):
        return self.ent.getName()

    def select(self, ids):
        print("ids", ids)
        keys = [ObjectId(key) for key in ids]
        print("keys", keys)
        result = dict()
        for doc in self.c.find({"_id": {"$all": keys}}):
            print("doc", doc)
            id_ = doc["_id"]
            result[id_] = doc
        return result

    def create(self, data):
        result = self.c.insert_one(data).inserted_id
        print(result)
        return result

    def update(self, id, data):
        self.c.update_one({"_id": id}, {"$set": data})
        return id

    def delete(self, id):
        self.c.delete_one({"_id": id})
        return id
