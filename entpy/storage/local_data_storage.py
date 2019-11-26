class LocalDataStorage:
    def __init__(self):
        self._nextID = 0
        self._data = dict()

    def select(self, ids):
        result = dict()
        for id in ids:
            result[id] = self._data.get(id)

        print("select", result)
        return result

    def create(self, data):
        id = self._nextID + 1
        self._nextID = id
        self._data[id] = data
        print("create:", self._data)
        return id

    def update(self, id, data):
        self._data[id] = data
        print("update:", self._data)
        return id

    def delete(self, id):
        self._data.pop(id, None)
        return id
