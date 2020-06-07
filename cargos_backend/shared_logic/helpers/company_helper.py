from shared_logic.database_queries import get_storages_for_company, get_employees
from shared_logic.helpers.storage_helper import count_cargos_for_storage


def count_cargos_for_company(company):
    storages = get_storages_for_company(company)

    total_count = 0
    for storage in storages:
        total_count += count_cargos_for_storage(storage)

    return total_count


def count_employees_for_company(company):
    return len(get_employees(company))
