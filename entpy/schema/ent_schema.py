from entpy.base.base import EntBase
from entpy.loader.ent_loader import EntLoader
from entpy.storage.local_data_storage import LocalDataStorage
from mutator import (
    EntMutationData,
    EntMutationView,
    EntMutationBuilder,
    CREATE,
    UPDATE,
    DELETE,
)


class EntSchema:
    def __init__(self):
        # TODO: implement checkers
        self._test = "abc"
        self._storage = self.getStorage()

    @staticmethod
    def getName():
        raise NotImpelementedError()

    @staticmethod
    def getFields():
        return {}

    @staticmethod
    def getEdges():
        return {}

    @staticmethod
    def setStorage():
        return LocalDataStorage()

    def getStorage(self):
        if hasattr(self, "_storage"):
            return self._storage
        else:
            self._storage = self.setStorage()
        return self._storage

    def getEntClass(self):
        class EntConstructor(EntBase):
            pass

        fields = self.getFields()
        for name in fields.keys():
            field = fields[name]

            def func(self):
                return field.coerce(self.getField(name))

            setattr(EntConstructor, "get" + name, func)

        edges = self.getEdges()
        for name in edges.keys():
            edge = edges[name]

            def func(s):
                id = self.getField(edge.field)
                return edge.schema.getEntFactory().gen(id)

            setattr(EntConstructor, "gen" + name, func)

        return EntConstructor

    def getEntFactory(self):
        storage = self.getStorage()
        Ent = self.getEntClass()
        fields = self.getFields()

        def func(key, item):
            rawData = dict()
            for name in fields:
                field = fields[name]
                rawData[name] = item[field.storage_key]
            return Ent(key, rawData)

        loader = EntLoader(storage, func)

        return loader

    def getMutationBuilderClass(self):
        class EntBuilderConstructor(EntMutationBuilder):
            pass

        fields = self.getFields()
        for name in fields.keys():
            field = fields[name]

            def func(self, value):
                self.setField(name, field.assertx(value))
                return self

            setattr(EntBuilderConstructor, "set" + name, func)

        print("EntBuilderConstructor", EntBuilderConstructor.__dict__)
        return EntBuilderConstructor

    def getMutationViewClass(self):
        class EntViewConstructor(EntMutationView):
            pass

        fields = self.getFields()
        for name in fields.keys():

            def func(self):
                return self.getOldField(name)

            setattr(EntViewConstructor, "getOld" + name, func)

            def func(self):
                return self.getNewField(name)

            setattr(EntViewConstructor, "getNew" + name, func)

            def func(self):
                return self.getNewOrOldField(name)

            setattr(EntViewConstructor, "getNewOrOld" + name, func)
        return EntViewConstructor

    def getMutator(self):
        schema = self
        Ent = schema.getEntClass()
        Builder = schema.getMutationBuilderClass()

        class mutator:
            @staticmethod
            def create():
                _data = dict()
                for field in schema.getFields().keys():
                    _data[field] = None
                data = EntMutationData(Ent(0, _data))
                return Builder(schema, CREATE, data)

            @staticmethod
            def update(entity):
                data = EntMutationData(entity)
                return Builder(schema, UPDATE, data)

            def delete(entity):
                data = EntMutationData(entity)
                return Builder(schema, DELETE, data)

        return mutator


class EntSchemaField:
    def __init__(self, key):
        self.storage_key = key

    @staticmethod
    def coerce(value):
        raise NotImpelementedError()

    @staticmethod
    def assertx(value):
        raise NotImpelementedError()


class StringSchemaField(EntSchemaField):
    @staticmethod
    def coerce(value):
        # TODO: cast as string
        return value

    @staticmethod
    def assertx(value):
        # TODO: validate string
        return value


class NumberSchemaField(EntSchemaField):
    @staticmethod
    def coerce(value):
        # TODO: cast as string
        return value

    @staticmethod
    def assertx(value):
        # TODO: validate string
        return value


class EntSchemaEdge:
    def __init__(self, field, schema):
        self.field = field
        self.schema = schema
