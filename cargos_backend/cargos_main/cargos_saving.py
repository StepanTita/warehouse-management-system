from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from shared_logic.database_queries import get_storage_by_pk, get_cargos_value_list, get_cell_of_storage, get_all_cells, \
    get_cell_of_cargo
from shared_logic.util_vars import UNSPECIFIED
from .custom_logic.new_cargo_logic import add_new_cargo_unformated
from .models import Storage, Cargo, Cell


def save_cargo(data):
    success = True
    storage = get_storage_by_pk(pk=data.get('storage', -1))

    cell_vals = get_cell_of_cargo(get_cargos_value_list('cell', distinct=True), storage)

    new_cell_vals = get_all_cells().difference(cell_vals)

    new_row, new_el, new_pos = add_new_cargo_unformated(
        {
            'height': data.get('height', 1),
            'length': data.get('length', 1),
            'width': data.get('width', 1),
            'rotatable': data.get('rotatable', 'No')
        },
        new_cell_vals,
        storage.rows, storage.elevations, storage.positions
    )

    if new_row == UNSPECIFIED:  # No suitable cell in this storage!
        return not success

    add_cargo_fields(new_row, new_el, new_pos, data)

    return success


def parse_date(date):
    dtd = str(date)
    try:
        dtd = datetime.strptime(dtd, '%d.%m.%Y')
    except ValueError:
        pass
    else:
        return dtd.strftime('%Y-%m-%d')
    return dtd


def parse_date_time(date):
    dta = str(date)
    try:
        dta = datetime.strptime(dta, '%d.%m.%y %H:%M:%S')
    except ValueError:
        pass
    else:
        return dta.strftime("%Y-%m-%d %H:%M:%S %Z")
    return dta


def add_cargo_fields(new_row, new_el, new_pos, data):
    new_cargo_obj = Cargo()

    new_cargo_obj.cell = get_cell_of_storage(row=new_row, elevation=new_el, pos=new_pos,
                                             storage_id=int(data['storage']))

    new_cargo_obj.date_added = parse_date_time(data.get('date_added', timezone.now()))
    new_cargo_obj.date_dated = parse_date(data.get('date_dated', timezone.now()))
    new_cargo_obj.title = data.get('title', 'Unknown')
    new_cargo_obj.description = data.get('description', '...')
    new_cargo_obj.height = data.get('height', 1)
    new_cargo_obj.width = data.get('width', 1)
    new_cargo_obj.length = data.get('length', 1)
    new_cargo_obj.rotatable = True if data.get('rotatable', 'No') == 'Yes' else False

    new_cargo_obj.save()


def add_cell_fields(row, el, pos, storage):
    new_cell = Cell()

    new_cell.row = row
    new_cell.elevation = el
    new_cell.position = pos

    new_cell.height = storage.default_height
    new_cell.length = storage.default_length
    new_cell.width = storage.default_width

    new_cell.storage = storage

    new_cell.save()


# def exclude_occupied_cells(cell_vals):
#     new_cell_vals = get_all_cells()
#     for val in cell_vals:
#         for cell_id in val:
#             new_cell_vals = new_cell_vals.exclude(pk__exact=cell_id)
#     return new_cell_vals


@receiver(post_save, sender=Storage)
def update_cells(sender, instance, **kwargs):
    rs = instance.rows
    els = instance.elevations
    pos = instance.positions

    for i in range(rs):
        for j in range(els):
            for k in range(pos):
                add_cell_fields(row=i, el=j, pos=k, storage=instance)
