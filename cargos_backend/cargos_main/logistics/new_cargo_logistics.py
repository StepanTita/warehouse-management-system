"""
Package responsible for smart and optimal storage fulfillment.
"""
from django.db.models import QuerySet

from bridge import consts
from .utility import Cargo, Cell


def add_new_cargo_unformated(cargo: dict, cells: QuerySet, storage_rows: int, storage_elevations: int,
                             storage_positions: int) -> tuple:
    """
    :param cargo:
    :param cells:
    :param storage_rows:
    :param storage_elevations:
    :param storage_positions:
    :return:
    New position of a cargo (row, elevation, position)
    """
    new_cargo = Cargo(
        float(cargo['height']),
        float(cargo['length']),
        float(cargo['width']),
        cargo['rotatable']
    )

    storage = [[[Cell(0, 0, 0) for _ in range(storage_positions + 1)] for _ in range(storage_elevations + 1)] for _ in
               range(storage_rows + 1)]  # Generate storage
    for cell in cells:
        i, j, k = cell.row, cell.elevation, cell.position
        storage[i][j][k].height, storage[i][j][k].length, storage[i][j][k].width = (
            float(cell.height),
            float(cell.length),
            float(cell.width)
        )

    new_row, new_el, new_pos = add_new_cargo(storage, new_cargo)

    return new_row, new_el, new_pos


def add_new_cargo(storage: list, new_cargo: Cargo) -> tuple:
    """
    :param storage: 3d list where each item is custom_util_classes.Cell [{row, elevation, position}, {height, length, width}...]
    :param new_cargo: Cargo with {height, length, width...}
    :return: {row, elevation, position}

    Assume {0, 0, 0} - is the best position
    """
    res_row = consts.UNSPECIFIED
    res_el = consts.UNSPECIFIED
    res_pos = consts.UNSPECIFIED
    efficiency = 0
    for i, row in enumerate(storage):
        for j, elevation in enumerate(row):
            for k, cell in enumerate(elevation):
                if fits(cell, new_cargo):
                    new_efficiency = 1 / (abs(cell.volume() - new_cargo.volume()) + i + j + k + 1)
                    if new_efficiency > efficiency:
                        res_row = i
                        res_el = j
                        res_pos = k
    return res_row, res_el, res_pos


def fits(cell: Cell, cargo: Cargo) -> bool:
    """
    :param cell:
    :param cargo:
    :return:
    True if cargo fits the cell - False otherwise
    """
    if cargo.rotatable:
        min_dim_cell = min(cell.height, cell.length, cell.width)
        return min_dim_cell >= cargo.height and min_dim_cell >= cargo.length and min_dim_cell >= cargo.width

    return cell.height >= cargo.height and (cell.length >= cargo.length and cell.width >= cargo.width or
                                            cell.width >= cargo.length and cell.length >= cargo.width)
