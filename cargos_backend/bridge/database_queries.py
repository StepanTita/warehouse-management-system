from itertools import chain

from cargos_main.models import Cargo, Cell, Storage, Company, Categorization, Category
from users.models import DateNotifications, Employee


# CARGO
def get_all_cargos(company, date_sort=False, date_sort_reversed=False):
    # if company is None:
    #     query = Cargo.objects.all()
    # else:
    #     query = Cargo.objects.filter(company=company)

    query = Cargo.objects.all().filter(
        cell__in=Cell.objects.filter(
            storage__in=Storage.objects.all().filter(company=company)
        ))

    if date_sort_reversed:
        query = query.order_by("-date_added")
    elif date_sort:
        query = query.order_by("date_added")
    return query


def get_cargos_value_list(field, distinct=False):
    query = Cargo.objects.filter().values_list(field)
    if distinct:
        query = query.distinct()
    return query


def get_cargos_todate(company, date):
    return get_all_cargos(company=company).filter(date_dated__lte=date)


def get_cargo_by_pk(pk):
    return Cargo.objects.get(pk=pk)


def get_all_cargos_of_cell(cell):
    return Cargo.objects.all(cell=cell)


# STORAGE
def get_storage_by_pk(pk=-1):
    return Storage.objects.get(pk=pk)


def get_all_storages(company):
    return Storage.objects.all().filter(company=company)


def get_storages_for_company(company):
    return Storage.objects.filter(company=company)


# CELL
def get_cell_of_storage(row, elevation, pos, storage_id):
    return Cell.objects.get(row=row,
                            elevation=elevation,
                            position=pos,
                            storage_id=storage_id)


def get_cell_of_cargo(cell_pks, storage):
    return Cell.objects.all().filter(pk__in=cell_pks, storage__exact=storage)


def get_all_cells():
    return Cell.objects.all()


def get_all_cells_of_storage(storage):
    return Cell.objects.all().filter(storage=storage)


# NOTIFICATION
def get_notifications_unread_first(user, reversed=True):
    sign = '-' if reversed else ''
    notifs = user.notifications.all().filter(cargo__in=get_all_cargos(company=get_company(user)))  # FIXME if not right
    unread = notifs.unread().order_by(f'{sign}timestamp')
    read = notifs.read().order_by(f'{sign}timestamp')
    total = (unread, read)
    result = list(chain(*total))
    return result


def get_dated_for_user(cargos_dated, user):
    for cargo in cargos_dated:
        DateNotifications.objects.get_or_create(
            user=user,
            cargo=cargo
        )
    return DateNotifications.objects.filter(viewed=False, user=user)


def get_all_notifications(user):
    return user.notifications.all().filter(cargo__in=get_all_cargos(company=get_company(user)))


# COMPANY
def get_company(user):
    return Company.objects.get(pk=Employee.objects.get(user_id=user).company.pk)


def get_all_companies():
    return Company.objects.all()


def get_employees(company):
    return Employee.objects.filter(company=company)


def get_categories(company):
    return Categorization.objects.filter(company=company)


def get_all_categories():
    return Category.objects.all()
