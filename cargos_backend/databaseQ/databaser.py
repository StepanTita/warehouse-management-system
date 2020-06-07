class Databaser:
    """
        Always start with 'all', and end with 'query'
    """

    def __init__(self, *args, **kwargs):
        self._ctx = None
        self._query = None

    def set_context(self, ctx) -> None:
        self._ctx = ctx

    def all(self):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

    def of_user(self, user):
        raise NotImplementedError

    def query(self):
        return self._query
