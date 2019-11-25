class EntBase:
    def __init__(self, id, data):
        self._id = id
        self._data = data

    def getID(self):
        return self._id

    def getField(self, name):
        return self._data[name]
