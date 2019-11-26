CREATE = 0
UPDATE = 1
DELETE = 2


class EntMutationData:
    def __init__(self, entity):
        self._entity = entity
        self._fields = dict()

    def getEntity(self):
        return self._entity

    def setField(self, name, value):
        self._fields[name] = value

    def hasField(self, name):
        return name in self._fields.keys()

    def getField(self, name):
        return self._fields[name]

    def getAvailableFields(self):
        return self._fields.keys()


class EntMutationBuilder:
    def __init__(self, schema, operation, data):
        self._schema = schema
        self._operation = operation
        self._data = data

    def setField(self, name, value):
        print("EntMutationBuilder.setField", name, value)
        self._data.setField(name, value)
        return self

    def save(self):
        schema = self._schema
        View = schema.getMutationViewClass()
        view = View(self._data)

        # TODO: triggers, validators and observers

        fields = schema.getFields()
        rawData = dict()

        for name in fields.keys():
            field = fields[name]
            rawData[field.storage_key] = view.getNewOrOldField(name)

        storage = schema.getStorage()
        entity = self._data.getEntity()

        if self._operation == CREATE:
            write = storage.create(rawData)
        if self._operation == UPDATE:
            write = storage.update(entity.getID(), rawData)
        if self._operation == DELETE:
            write = storage.delete(entity.getID())

        factory = schema.getEntFactory()
        result = factory.gen(write)
        return result


class EntMutationView:
    def __init__(self, data):
        self._data = data

    def getID(self):
        return self._data.getEntity().getID()

    def getOldField(self, name):
        # return getattr(self._data.getEntity(), "get" + name)()
        return self._data.getEntity().getField(name)

    def getNewField(self, name):
        if self._data.hasField(name):
            return self._data.getField(name)
        return None

    def getNewOrOldField(self, name):
        new = self.getNewField(name)
        if new != None:
            return new
        return self.getOldField(name)
