
class EntLoader:

    def __init__(self, source):
        self._source = source
        self._cached = dict()
        self._pending = list()
        self._timeout = None

    def gen(self, id):
        if self._cached.get(id, False):
            self._pending.push(id)

        if not self._timeout:
            self._timeout = 3  # TODO: implement timeout
            self._load()
            self._timeout = None

        return self._cached[id]

    def _load(self):
        pending = self._pending
        self._pending = list()

        result = self._source.select(pending)
        for id in pending:
            if result.get(id, False):
                self._cached[id] = result[id]


    def clear(self, id):
        self._cached.pop(id, None)
