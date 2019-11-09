# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from notifications.signals import notify

from cargos_main.models import Cargo


class DateNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cargo {self.cargo} depraved, user: {self.user}, notified"


def cargo_dated_notification(sender, instance, *args, **kwargs):
    notify.send(instance, verb='was saved')


post_save.connect(cargo_dated_notification, sender=Cargo)
