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


class Position(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Employee(models.Model):
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/images', default='users/images/default-user.png')
    position = models.ManyToManyField(Position)
    # Social links
    facebook = models.URLField(null=True)
    twitter = models.URLField(null=True)
    github = models.URLField(null=True)
    linkedin = models.URLField(null=True)

    def __str__(self):
        return f'{self.user} : {self.company}'
