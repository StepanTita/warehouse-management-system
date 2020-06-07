from bridge.database_queries import get_all_cells_of_storage, get_all_cargos_of_cell


def count_cargos_for_storage(storage):
    cells = get_all_cells_of_storage(storage)

    count_cargos = 0
    for cell in cells:
        count_cargos += len(get_all_cargos_of_cell(cell))
    return count_cargos
