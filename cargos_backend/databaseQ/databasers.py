from cargos_main import models
from databaseQ.databaser import Databaser


class DatabaserCargo(Databaser):

    def __init__(self, *args, **kwargs):
        super(DatabaserCargo, self).__init__(*args, **kwargs)

    def all(self):
        self._query = models.Cargo.objects.all()
        return self

    def of_user(self, user):
        self._query = self._query.filter(
            cell__in=self._ctx.Cell().of_storages(
                storages=self._ctx.Storage().of_company(
                    company=self._ctx.Company().of_user(user).query()
                ).query()
            ).query()
        )
        return self

    def to_date(self, date):
        self._query = self._query.filter(date_dated__lte=date)
        return self

    def order_by(self, fields):
        self._query = self._query.order_by(fields)
        return self


class DatabaserCell(Databaser):
    def __init__(self, *args, **kwargs):
        super(DatabaserCell, self).__init__(*args, **kwargs)

    def all(self):
        self._query = models.Cell.objects.all()
        return self

    def of_storage(self, storage):
        self._query = self._query.filter(storage=storage)
        return self

    def of_storages(self, storages):
        self._query = self._query.filter(storage__in=storages)
        return self


class DatabaserStorage(Databaser):
    def __int__(self, *args, **kwargs):
        super(DatabaserStorage, self).__init__(*args, **kwargs)

    def all(self):
        self._query = models.Storage.objects.all()
        return self

    def of_user(self, user):
        self._query = self._query.filter(company__employee__user=user)
        return self

    def of_company(self, company):
        self._query = self._query.filter(company=company)
        return self


class DatabaserCompany(Databaser):
    def __int__(self, *args, **kwargs):
        super(DatabaserCompany, self).__init__(*args, **kwargs)

    def all(self):
        self._query = models.Company.objects.all()
        return self

    def of_user(self, user):
        self._query = self._query.get(employee__user=user)
        return self
