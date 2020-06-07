from datetime import datetime

from django.utils import timezone

import bridge.database_queries as queries
from bridge import consts
from .logistics.new_cargo_logistics import add_new_cargo_unformated
from .models import Cargo, Cell


def save_cargo(data):
    success = True
    storage = queries.get_storage_by_pk(
        pk=data.get('storage', -1))  # If no storage specified - then -1 will be used instead

    cell_vals = queries.get_cell_of_cargo(
        queries.get_cargos_value_list('cell', distinct=True),
        storage
    )

    new_cell_vals = queries.get_all_cells_of_storage(storage).difference(cell_vals)

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

    if new_row == consts.UNSPECIFIED:  # No suitable cell in this storage!
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

    new_cargo_obj.cell = queries.get_cell_of_storage(
        row=new_row,
        elevation=new_el,
        pos=new_pos,
        storage_id=int(data['storage'])
    )

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

