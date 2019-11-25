from entpy.base.base import EntBase
from entpy.storage.local_data_storage import LocalDataStorage

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

        return constructor(self.getName(), self.getFields())


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
