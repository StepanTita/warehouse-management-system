# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from cargos_main.models import Cargo, Company


class DateNotifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cargo {self.cargo} depraved, user: {self.user}, notified"


class UserInCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
