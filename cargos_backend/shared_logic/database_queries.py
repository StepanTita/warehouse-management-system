from django.db.models import Q

from cargos_main.models import Cargo, Cell, Storage
from search import normalize_query
from shared_logic.from_choice import to_format


def create_search_queryset(data):
    search = data['search']
    storage = data['storages']
    fields = data.getlist('fields')

    queryset = Cargo.objects.all().filter(
        cell__in=Cell.objects.filter(storage_id=int(storage)))
    # category = to_category_name(int(data['category']), CATEGORY_CHOICES)

    entry_query = get_query(search, [to_format(field) for field in fields])
    found_entries = Cargo.objects.filter(entry_query).order_by("-date_added")
    return found_entries


def get_query(query_string, search_fields):
    """
        Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    :param query_string:
    :param search_fields:
    :return:
    """
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


# CARGO
def get_all_cargos(date_sort=False, date_sort_reversed=False):
    query = Cargo.objects.all()
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


# STORAGE
def get_storage_by_pk(pk=-1):
    return Storage.objects.get(pk=pk)


# CELL
def get_cell_of_storage(row, elevation, pos, storage_id):
    return Cell.objects.get(row=row,
                            elevation=elevation,
                            position=pos,
                            storage_id=storage_id)


def get_cell_of_cargo(cell_pks, storage):
    return Cell.objects.all().filter(pk__in=cell_pks, storage=storage)


def get_all_cells():
    return Cell.objects.all()
