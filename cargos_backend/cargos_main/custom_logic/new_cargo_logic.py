"""
Package responsible for smart and optimal storage fulfillment.
"""
from .util_classes import Cargo, Cell


def add_new_cargo_unformated(cargo, cells, storage_rows, storage_elevations, storage_positions):
    new_cargo = Cargo(cargo['height'], cargo['length'], cargo['width'], cargo['rotatable'])
    storage = [[[Cell for _ in range(storage_positions + 1)] for _ in range(storage_elevations + 1)] for _ in range(storage_rows + 1)]

    for cell in cells:
        i, j, k = cell['row'], cell['elevation'], cell['position']
        storage[i][j][k] = Cell(cell['height'], cell['length'], cell['width'], cell['is_free'])

    add_new_cargo(storage, new_cargo)


def add_new_cargo(storage, new_cargo):
    """
    :param storage: 3d list where each item is custom_util_classes.Cell [{row, elevation, position}, {height, length, width}...]
    :param new_cargo: Cargo with {height, length, width...}
    :return: {row, elevation, position}

    Assume {0, 0, 0} - is the best position
    """
    res_row = -1
    res_el = -1
    res_pos = -1
    efficiency = 0
    for i, row in enumerate(storage):
        for j, elevation in enumerate(row):
            for k, cell in enumerate(elevation):
                if cell.is_free and fits(cell, new_cargo):
                    new_efficiency = 1 / (abs(cell.volume() - new_cargo.volume()) + i + j + k + 1)
                    if new_efficiency > efficiency:
                        res_row = i
                        res_el = j
                        res_pos = k
    return res_row, res_el, res_pos, res_row != -1


def fits(cell: Cell, cargo: Cargo):
    if cargo.rotatable:
        min_dim_cell = min(cell.height, cell.length, cell.width)
        return min_dim_cell >= cargo.height and min_dim_cell >= cargo.length and min_dim_cell >= cargo.width

    return cell.height >= cargo.height and (cell.length >= cargo.length and cell.width >= cargo.width or
                                            cell.width >= cargo.length and cell.length >= cargo.width)