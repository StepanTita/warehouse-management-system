from django.db.models.signals import post_save
from django.dispatch import receiver

from cargos_main.cargos_saving import add_cell_fields
from cargos_main.models import Storage, Cell


@receiver(post_save, sender=Storage)
def update_cells(sender, instance, *args, **kwargs):
    rs = instance.rows
    els = instance.elevations
    pos = instance.positions

    for i in range(rs):
        for j in range(els):
            for k in range(pos):
                if Cell.objects.all().filter(row=i, elevation=j, position=k, storage=instance).first() is None:
                    add_cell_fields(row=i, el=j, pos=k, storage=instance)
