from databaseQ.databasers import *
from databaseQ.searcher import Searcher


class Context:
    _instance = None

    def __init__(self,
                 databaser_cargo: DatabaserCargo,
                 databaser_cell: DatabaserCell,
                 databaser_storage: DatabaserStorage,
                 databaser_company: DatabaserCompany,
                 searcher: Searcher
                 ):
        self._cargo = databaser_cargo
        self._cell = databaser_cell
        self._storage = databaser_storage
        self._company = databaser_company
        self._searcher = searcher
        Context._instance = self

    def Cargo(self) -> DatabaserCargo:
        return self._cargo.all()

    def Cell(self) -> DatabaserCell:
        return self._cell.all()

    def Storage(self) -> DatabaserStorage:
        return self._storage.all()

    def Company(self) -> DatabaserCompany:
        return self._company.all()

    def Search(self, search, storage, fields):
        return self._searcher.queryset(search, storage, fields)

    @staticmethod
    def get(request):
        if Context._instance is None:
            return create_context(request.user)
        return Context._instance


def create_context(user):
    if user.is_authenticated:
        ctx = Context(
            databaser_cargo=DatabaserCargo(),
            databaser_cell=DatabaserCell(),
            databaser_storage=DatabaserStorage(),
            databaser_company=DatabaserCompany(),
            searcher=Searcher()
        )
        ctx._cargo.set_context(ctx)
        ctx._cell.set_context(ctx)
        ctx._storage.set_context(ctx)
        ctx._company.set_context(ctx)
        ctx._searcher.set_context(ctx)
        return ctx
    return None
