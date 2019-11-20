from cargos_main.models import Cargo
from shared_logic.from_choice import to_view_choice

CATEGORY_CHOICES = (
    (1, "Cargos"),
    (2, "Cells"),
    (3, "Storages")
)

fields_choices = tuple([(i + 1, val) for i, val in enumerate(Cargo._meta.get_fields())])[1:]
FIELDS_CHOICES = tuple(map(lambda x: to_view_choice(x), fields_choices))
