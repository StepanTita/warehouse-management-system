from bridge.from_choice import to_view_choice
from cargos_main.models import Cargo

CATEGORY_CHOICES = (
    (1, "Cargos"),
    (2, "Cells"),
    (3, "Storages")
)

fields = Cargo._meta.get_fields()
fields_choices = [(i + 1, val) for i, val in enumerate(fields)][1:]
fields_choices = [field for field in fields_choices if field[0] not in (2, 4)]
FIELDS_CHOICES = tuple(map(lambda x: to_view_choice(x), fields_choices))
