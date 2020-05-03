import datetime as dt

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Company(models.Model):
    vendor = models.CharField(max_length=200)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    data_registered = models.DateField(auto_now_add=True)
    website = models.CharField(max_length=200)


class Storage(models.Model):
    name = models.CharField(max_length=200, null=True)

    rows = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(100)])
    elevations = models.IntegerField(validators=[MinValueValidator(1),
                                                 MaxValueValidator(100)])  # y
    positions = models.IntegerField(validators=[MinValueValidator(1),
                                                MaxValueValidator(100)])  # x

    default_height = models.DecimalField(decimal_places=2, max_digits=9, default=1,
                                         validators=[MinValueValidator(1),
                                                     MaxValueValidator(100)])
    default_length = models.DecimalField(decimal_places=2, max_digits=9, default=1,
                                         validators=[MinValueValidator(1),
                                                     MaxValueValidator(100)]
                                         )
    default_width = models.DecimalField(decimal_places=2, max_digits=9, default=1,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(100)])

    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.name) + ', rs: ' + str(self.rows) + ' es: ' + str(self.elevations) + ' ps: ' + str(
            self.positions)


class Cell(models.Model):
    row = models.IntegerField()
    elevation = models.IntegerField()  # y
    position = models.IntegerField()  # x

    height = models.DecimalField(decimal_places=2, max_digits=9, default=1,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(100)])
    length = models.DecimalField(decimal_places=2, max_digits=9, default=1,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(100)]
                                 )
    width = models.DecimalField(decimal_places=2, max_digits=9, default=1, validators=[MinValueValidator(1),
                                                                                       MaxValueValidator(100)])

    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('row', 'elevation', 'position', 'storage'),)

    def __str__(self):
        return f"{Storage.objects.get(pk=self.storage.pk).name} r: {self.row} e: {self.elevation} p: {self.position}"

    def clean(self):
        super().clean()
        if Cell.objects.get(pk=self.pk):
            return
        elif self.storage.rows * self.storage.elevations * self.storage.positions >= len(
                Cell.objects.filter(storage=self.storage)):
            raise ValidationError('You cannot create more cells for this storage')


class Cargo(models.Model):
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE)

    height = models.DecimalField(decimal_places=2, max_digits=9, default=1, validators=[MinValueValidator(1),
                                                                                        MaxValueValidator(100)])
    length = models.DecimalField(decimal_places=2, max_digits=9, default=1, validators=[MinValueValidator(1),
                                                                                        MaxValueValidator(100)])
    width = models.DecimalField(decimal_places=2, max_digits=9, default=1, validators=[MinValueValidator(1),
                                                                                       MaxValueValidator(100)])

    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)

    date_added = models.DateTimeField(auto_now=True)
    date_dated = models.DateField(default=dt.datetime.now)

    rotatable = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ": " + str(self.title)

    # def clean(self):
    #     super().clean()
    #     try:
    #         parse(self.date_dated)


class Droid(models.Model):
    title = models.CharField(max_length=200, null=True)

    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{str(self.title)} - {str(self.id)}'
