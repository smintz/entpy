class EntLoader:
    def __init__(self, source):
        self._source = source
        self._cached = dict()
        self._pending = list()
        self._timeout = None

    def gen(self, id):
        if not self._cached.get(id, False):
            self._pending.append(id)

        if self._timeout is None:
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

        return self._cached

    def clear(self, id):
        self._cached.pop(id, None)
