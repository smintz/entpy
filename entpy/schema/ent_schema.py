from entpy.base.base import EntBase
from entpy.storage.local_data_storage import LocalDataStorage
from mutator import EntMutationData, EntMutationView, EntMutationBuilder


class EntSchema:
    def __init__(self):
        # TODO: implement checkers
        self._test = "abc"

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
    def getStorage():
        return LocalDataStorage()

    def getEntClass(self):
        class constructor(EntBase):
            pass

        fields = self.getFields()
        for name, field in fields.iteritems():

            def func(self):
                return field.coerce(self.getField(name))

            setattr(constructor, "get" + name, func)

        edges = self.getEdges()
        for name, edge in edges.iteritems():

            def func(s):
                id = self.getField(edge.field)
                return edge.schema.getEntFactory().gen(id)

            setattr(constructor, "gen" + name, func)

        return constructor

    def getEntFactory(self):
        storage = self.getStorage()
        Ent = self.getEntClass()
        fields = self.getFields()

        def func(ids):
            items = storage.select(ids)
            entities = dict()
            for key in items:
                if not items[key]:
                    continue
                rawData = dict()
                for name in fields:
                    field = fields[name]
                    rawData[name] = items[key][field.storage_key]
                entities[key] = Ent(key, rawData)

        return func

    def getMutationBuilderClass(self):
        class constructor(EntMutationBuilder):
            pass

        fields = self.getFields()
        for name in fields.keys():
            field = fields[name]

            def func(self, value):
                return self.setField(name, field.assertx(value))

            setattr(constructor, "set" + name, func)

        return constructor

    def getMutationViewClass(self):
        class constructor(EntMutationView):
            pass

        fields = self.getFields()
        for name in fields.keys():

            def func(self):
                return self.getOldField(name)

            setattr(constructor, "getOld" + name, func)

            def func(self):
                return self.getNewField(name)

            setattr(constructor, "getNew" + name, func)

            def func(self):
                return self.getNewOrOldField(name)

            setattr(constructor, "getNewOrOld" + name, func)
        return constructor


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

    def assertx(value):
        # TODO: validate string
        return value


class NumberSchemaField(EntSchemaField):
    @staticmethod
    def coerce(value):
        # TODO: cast as string
        return value

    def assertx(value):
        # TODO: validate string
        return value


class EntSchemaEdge:
    def __init__(self, field, schema):
        self.field = field
        self.schema = schema
